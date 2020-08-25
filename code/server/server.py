#!/usr/bin/env python3
# TODO: should IP be localhost?
# TODO: add debug messages
# TODO: discard messages that are too old
# - a new co-routine to prevent people spamming with different UIDs
from typing import *
import asyncio
from time import time
from dataclasses import dataclass

queues: Dict[str, asyncio.PriorityQueue] = {}

DELIMITER = b" | "  # delimiter between messages sent from the client
MAX_QUEUE_SIZE = 10  # number of items in a single queue


@dataclass
class Message:
    uid: str  # from which device
    command: str  # which command
    delivered: int  # when delivered

    def __lt__(self, other):
        return self.delivered < other.delivered


def ensure_queue(mid):
    """Ensure that a queue with the given Mynt ID exists."""
    if mid not in queues:
        queues[mid] = asyncio.PriorityQueue(MAX_QUEUE_SIZE)


async def handler(reader, writer):
    """A client handler. The details of the protocol are covered in DOCUMENTATION.md."""
    uid, other = (await reader.readline()).strip().split(DELIMITER, 1)

    # if we can split some more, the client is sending data
    if DELIMITER in other:
        mid, command = other.split(DELIMITER, 1)
        message = Message(uid, command, time())

        ensure_queue(mid)

        # if the queue is full, discard older messages
        if queues[mid].full():
            queues[mid].get_nowait()

        queues[mid].put_nowait(message)

    # if not, send some data to the client
    else:
        mid = other

        # wait for some actual data to send
        while True:
            ensure_queue(mid)
            message = await queues[mid].get()

            # if the command is from the same UID, place it back immediately
            if uid == message.uid:
                queues[mid].put_nowait(message)
            else:
                # clear empty queues
                if queues[mid].empty():
                    del queues[mid]

                writer.write(message.command)
                await writer.drain()
                break

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
