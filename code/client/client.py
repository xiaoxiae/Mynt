"""A module for communicating with Mynt's server."""
import asyncio

from typing import *
from uuid import getnode as get_mac


class Client:
    MAX_MESSAGE_SIZE = 1024  # TODO: read from some config file
    ADDRESS = ("localhost", 9106)  # TODO: IP

    def __init__(self, mynt_id: str, uid: Optional[str] = None):
        self.mynt_id = mynt_id
        self.uid = uid or hex(get_mac())

    async def __connect(self):
        """Start a connection with the server."""
        return await asyncio.open_connection(*self.ADDRESS)

    async def __close(self, writer):
        """Close the connection to the server."""
        writer.close()
        await writer.wait_closed()

    async def send(self, data: str):
        """A function for sending data to the Mynt server."""
        _, writer = await self.__connect()

        writer.write(f"{self.uid} | {self.mynt_id} | {data}\n".encode())
        await writer.drain()

        await self.__close(writer)

    async def receive(self):
        """A function for receiving data from the Mynt server."""
        reader, writer = await self.__connect()

        writer.write(f"{self.uid} | {self.mynt_id}\n".encode())
        await writer.drain()

        result = (await reader.read(self.MAX_MESSAGE_SIZE)).decode()
        await self.__close(writer)
        return result


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
