"""A module for communicating with the Mynt server."""
import asyncio

from typing import *
from uuid import getnode as get_mac


class Client:
    """A class for talking to the Mynt server (as a client)."""

    # constants
    MAX_MESSAGE_SIZE = 1024  # TODO: read from some config file
    ADDRESS = ("localhost", 9106)  # TODO: IP

    def __init__(self, mynt_id: str, uid: Optional[str] = None):
        self.mynt_id = mynt_id
        self.uid = uid or hex(get_mac())

    def connect(function):
        """a decorator for connecting to the server using a socket, doing stuff and
        then closing the socket."""

        async def wrapper(self, *args, **kwargs):
            reader, writer = await asyncio.open_connection(*self.ADDRESS)

            result = await function(self, reader, writer, *args, **kwargs)

            writer.close()
            await writer.wait_closed()

            return result

        return wrapper

    @connect
    async def send(self, reader, writer, data: str):
        """A function for sending data to the Mynt server."""
        writer.write(f"{self.uid} | {self.mynt_id} | {data}\n".encode("utf-8"))
        await writer.drain()

    @connect
    async def receive(self, reader, writer):
        """A function for receiving data from the Mynt server."""
        writer.write(f"{self.uid} | {self.mynt_id}\n".encode("utf-8"))
        await writer.drain()

        return (await reader.read(self.MAX_MESSAGE_SIZE)).decode("utf-8")


# try to talk between the two clients (when the server is running)
if __name__ == "__main__":
    c1 = Client("m1", "c1")
    c2 = Client("m1", "c2")

    loop = asyncio.get_event_loop()

    tasks = [
        c1.send("test"),
        c2.receive(),
    ]

    a, b = loop.run_until_complete(asyncio.gather(*tasks))
    print(a, b)

    loop.close()
