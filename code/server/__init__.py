"""The Mynt server module."""
# TODO: should IP be localhost?
# TODO: discard messages that are too old
# - a new co-routine to prevent people spamming with different UIDs
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

DELIMITER = b" | "  # delimiter between messages sent from the client
MAX_QUEUE_SIZE = 10  # number of items in a single queue


@dataclass
class Message:
    """A class for working with messages on the Mynt server."""

    uid: str  # from which device
    command: str  # which command
    delivered: int  # when delivered

    def __lt__(self, other):
        return self.delivered < other.delivered


def ensure_queue(mid, uid):
    """Ensure that a queue with the given Mynt ID and UID exists."""
    if mid not in queues:
        queues[mid] = {}

    if not uid in queues[mid]:
        queues[mid][uid] = asyncio.PriorityQueue(MAX_QUEUE_SIZE)


async def handler(reader, writer):
    """A client handler."""
    uid, other = (await reader.readline()).strip().split(DELIMITER, 1)

    # simplify code - debug, logging
    d = lambda x: x.decode()
    log = logging.info

    log(f"{d(uid)} | connected.")

    # if we can split some more, the client is sending data
    if DELIMITER in other:
        log(f"{d(uid)} | parsing message.")

        mid, command = other.split(DELIMITER, 1)
        message = Message(uid, command, time())

        log(f"{d(uid)} | {d(mid)} | sent command '{d(command)}'.")

        # forbid more than 2 devices under one Mynt ID
        if mid in queues and uid not in queues[mid] and len(queues[mid]) != 2:
            writer.close()
            await writer.wait_closed()
            log(f"{d(uid)} | {d(mid)} | too many devices, connection closed.")
            return

        ensure_queue(mid, uid)

        # if the queue is full, discard older messages
        if queues[mid][uid].full():
            queues[mid][uid].get_nowait()

        queues[mid][uid].put_nowait(message)
        log(f"{d(uid)} | {d(mid)} | command added.")

    # if not, send some data to the client
    else:
        mid = other

        log(f"{d(uid)} | {d(mid)} | checking queues.")

        for other_uid in queues[mid]:
            if other_uid != uid:
                command = (await queues[mid][other_uid].get()).command
                log(f"{d(uid)} | {d(mid)} | queue found, sending command {d(command)}.")

                writer.write(command)
                await writer.drain()
                break
        else:
            writer.close()
            await writer.wait_closed()
            log(f"{d(uid)} | {d(mid)} | queue not found, connection closed.")
            return

    writer.close()
    await writer.wait_closed()


coro = asyncio.start_server(handler, "localhost", 9106)
loop = asyncio.get_event_loop()
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
