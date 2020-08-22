#!/usr/bin/env python3
from typing import *
import asyncio

queues: Dict[str, asyncio.Queue] = {}


def ensure_queue_exists(mynt_id):
    if mynt_id not in queues:
        queues[mynt_id] = asyncio.Queue()


async def get_identifiers(reader) -> Tuple[str, str]:
    """Get the client's UID and its mint ID"""
    return (await reader.readline(), await reader.readline())


async def res_handler(reader, writer):
    """A handler for writing to the client."""
    uid, mynt_id = await get_identifiers(reader)
    ensure_queue_exists(mynt_id)

    while True:
        request = await queues[mynt_id].get()

        writer.write(request)
        await writer.drain()


async def req_handler(reader, writer):
    """A handler for reading from the client."""
    uid, mynt_id = await get_identifiers(reader)
    ensure_queue_exists(mynt_id)

    while True:
        result = await reader.readline()

        if len(result) != 0:
            queues[mynt_id].put_nowait(result)

        if reader.at_eof():
            return


req_coro = asyncio.start_server(req_handler, "localhost", 9106)
res_coro = asyncio.start_server(res_handler, "localhost", 9107)

loop = asyncio.get_event_loop()

req_server = loop.run_until_complete(req_coro)
res_server = loop.run_until_complete(res_coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    req_server.close()
    res_server.close()
    loop.run_until_complete(req_server.wait_closed())
    loop.run_until_complete(res_server.wait_closed())
    loop.close()
