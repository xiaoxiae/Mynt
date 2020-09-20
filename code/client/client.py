"""A module for communicating with Mynt's server."""
import asyncio
from typing import *
from uuid import getnode as get_mac


class Client:
    MAX_MESSAGE_SIZE = 1024
    ADDRESS = ("localhost", 9106)  # TODO: IP
    SEPARATOR = " | "

    def __init__(self, uid: Optional[str] = None):
        self.uid = uid or hex(get_mac())
        self.mynt_id is None

    def __join(self, *args) -> bytes:
        """Create a message by joining parts of it using a separator"""
        return (self.SEPARATOR.join(args) + "\n").encode()

    async def __connect(self):
        """Start a connection with the server."""
        return await asyncio.open_connection(*self.ADDRESS)

    async def __close(self, writer):
        """Close the connection to the server."""
        writer.close()
        await writer.wait_closed()

    def set_mynt_id(self, mynt_id: str):
        """Set the Mynt ID that the client will attempt to connect to. Note that this
        function must be called before functions like send and receive are use!"""
        self.mynt_id = mynt_id

    async def send(self, data: str):
        """A function for sending data to the Mynt server."""
        if self.mynt_id is None:
            return

        _, writer = await self.__connect()

        writer.write(self.__join(self.uid, self.mynt_id, data))
        await writer.drain()

        await self.__close(writer)

    async def receive(self):
        """A function for receiving data from the Mynt server."""
        if self.mynt_id is None:
            return

        reader, writer = await self.__connect()

        writer.write(self.__join(self.uid, self.mynt_id))
        await writer.drain()

        result = (await reader.read(self.MAX_MESSAGE_SIZE)).decode()
        await self.__close(writer)
        return result


# try to talk between the two clients (when the server is running)
if __name__ == "__main__":
    c1 = Client("c1")
    c1.set_mynt_id("m1")

    c2 = Client("c2")
    c2.set_mynt_id("m1")

    loop = asyncio.get_event_loop()

    tasks = [
        c1.send("test"),
        c2.receive(),
    ]

    a, b = loop.run_until_complete(asyncio.gather(*tasks))
    print(a, b)

    loop.close()
