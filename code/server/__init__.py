"""The Mynt server module."""
# TODO: should IP be localhost?
# TODO: discard messages that are too old
# - a new co-routine to prevent people spamming with different UIDs
# TODO: non-async PriorityQueue?
# - it not using async methods in the current implementation...
import asyncio
import logging
from dataclasses import dataclass
from time import time
from typing import *

logging.basicConfig(
    filename="server.log",
    format="%(asctime)s | %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.DEBUG,
)

# a queue for Mynt ID groups
queues: Dict[str, Dict[str, asyncio.PriorityQueue]] = {}

SEPARATOR = b" | "  # separator between messages sent from the client
MAX_QUEUE_SIZE = 10  # number of items in a single queue


@dataclass
class Message:
    """A class for working with messages on the Mynt server."""

    uid: str  # from which device
    command: str  # which command
    delivered: int  # when delivered

    def __lt__(self, other):
        return self.delivered < other.delivered


def log(*args: Union[str, bytes], sep=" | "):
    """Log items separated by a separator. If some of the parts are bytes, decode them
    to strings."""
    logging.info(sep.join(a.decode() if isinstance(a, bytes) else a for a in args))


def ensure_queue(mid, uid):
    """Ensure that a queue with the given Mynt ID and UID exists."""
    if mid not in queues:
        queues[mid] = {}

    if not uid in queues[mid]:
        queues[mid][uid] = asyncio.PriorityQueue(MAX_QUEUE_SIZE)


async def close_with_message(writer, message: List[Union[str, bytes]]):
    """Close the connection via a writer using the provided message."""
    log(*message)
    writer.close()
    await writer.wait_closed()


async def handler(reader, writer):
    """A client handler."""
    uid, other = (await reader.readline()).strip().split(SEPARATOR, 1)

    log(uid, "connected.")

    # if we can split some more, the client is sending data
    if SEPARATOR in other:
        log(uid, "parsing message.")

        mid, command = other.split(SEPARATOR, 1)
        message = Message(uid, command, time())

        log(uid, mid, f"sent command '{command.decode()}'.")

        # forbid more than 2 devices under one Mynt ID
        if mid in queues and uid not in queues[mid] and len(queues[mid]) != 2:
            await close_with_message(writer, [uid, mid, "too many devices, closing."])
            return

        ensure_queue(mid, uid)

        # if the queue is full, discard older messages
        if queues[mid][uid].full():
            queues[mid][uid].get_nowait()

        queues[mid][uid].put_nowait(message)
        log(uid, mid, "command added.")

    # if not, send some data to the client
    else:
        mid = other

        log(uid, mid, "checking queues.")

        if mid not in queues:
            await close_with_message(writer, [uid, mid, "no such mid queue group."])
            return

        for other_uid in queues[mid]:
            if other_uid != uid:
                if queues[mid][other_uid].empty():
                    await close_with_message(writer, [uid, mid, "pair queue empty."])
                    return

                command = queues[mid][other_uid].get_nowait().command
                log(uid, mid, f"queue found, sending command '{command.decode()}'.")

                writer.write(command)
                await writer.drain()
                break
        else:
            await close_with_message(writer, [uid, mid, "queue not found, closing."])
            return

    await close_with_message(writer, [uid, mid, "connection closing."])


coro = asyncio.start_server(handler, "localhost", 9106)
loop = asyncio.get_event_loop()
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
