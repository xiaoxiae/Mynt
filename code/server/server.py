#!/usr/bin/env python3
# TODO: should IP be localhost?
# TODO: add debug messages
# TODO: discard messages that are too old / there is too many of them in a queue
# - both could neatly be handled when the client is adding stuff to the queue
from typing import *
import asyncio

queues: Dict[str, asyncio.Queue] = {}
DELIMITER = b" | "


def ensure_queue(mynt_id):
    if mynt_id not in queues:
        queues[mynt_id] = asyncio.Queue()


async def handler(reader, writer):
    """A client handler. The details of the protocol are covered in DOCUMENTATION.md."""
    uid, other = (await reader.readline()).strip().split(DELIMITER, 1)

    # if we can split some more, the client is sending data
    if DELIMITER in other:
        mynt_id, command = other.split(DELIMITER, 1)

        ensure_queue(mynt_id)
        await queues[mynt_id].put((uid, command))

    # if not, send some data to the client
    else:
        mynt_id = other

        # wait for some actual data to send
        while True:
            ensure_queue(mynt_id)
            other_uid, command = await queues[mynt_id].get()

            # if the command is from the same UID, place it back (immediately)
            if uid == other_uid:
                queues[mynt_id].put_nowait((other_uid, command))
            else:
                # clear empty queues
                if queues[mynt_id].empty():
                    del queues[mynt_id]

                writer.write(command)
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
