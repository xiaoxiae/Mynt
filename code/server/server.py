#!/usr/bin/env python3
# TODO: should IP be localhost?
# TODO: add debug messages and logging
# TODO: discard messages that are too old
# - a new co-routine to prevent people spamming with different UIDs
from typing import *
import asyncio
from time import time
from dataclasses import dataclass

import logging

logging.basicConfig(filename="server.log", level=logging.DEBUG)

# a queue for Mynt ID groups
queues: Dict[str, Dict[str, asyncio.PriorityQueue]] = {}

DELIMITER = b" | "  # delimiter between messages sent from the client
MAX_QUEUE_SIZE = 10  # number of items in a single queue


@dataclass
class Message:
    uid: str  # from which device
    command: str  # which command
    delivered: int  # when delivered

    def __lt__(self, other):
        return self.delivered < other.delivered


def ensure_queue(mid, uid):
    """Ensure that a queue with the given Mynt ID and UID exists. Only do so if there
    wouldn't be more than 2 queues in the given group. Return True if the queue was
    created successfully, else return False."""
    if mid not in queues:
        queues[mid] = {}

    if not uid in queues[mid]:
        queues[mid][uid] = asyncio.PriorityQueue(MAX_QUEUE_SIZE)


async def handler(reader, writer):
    """A client handler."""
    uid, other = (await reader.readline()).strip().split(DELIMITER, 1)

    # if we can split some more, the client is sending data
    if DELIMITER in other:
        mid, command = other.split(DELIMITER, 1)
        message = Message(uid, command, time())

        # forbid more than 2 devices under one Mynt ID
        if mid in queues and len(queues[mid]) != 2:
            writer.close()
            await writer.wait_closed()

        ensure_queue(mid, uid)

        # if the queue is full, discard older messages
        if queues[mid][uid].full():
            queues[mid][uid].get_nowait()

        queues[mid][uid].put_nowait(message)

    # if not, send some data to the client
    else:
        mid = other

        for other_uid in queues[mid]:
            if other_uid != uid:
                message = await queues[mid][other_uid].get()

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
