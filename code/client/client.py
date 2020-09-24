"""A module for communicating with Mynt's server."""
# disabled because Pylint doesn't like decorators that mess with parameters
# pylint: disable=E1120
import asyncio
from typing import *
from uuid import getnode as get_mac


def connect_and_close(function):
    """a decorator for connecting to the server using a socket, doing stuff and
    then closing the socket."""

    async def wrapper(self, *args, **kwargs):
        if self.mynt_id is None:
            return

        reader, writer = await asyncio.open_connection(*self.ADDRESS)

        result = await function(self, reader, writer, *args, **kwargs)

        await writer.drain()
        writer.close()
        await writer.wait_closed()

        return result

    return wrapper


class Client:
    MAX_MESSAGE_SIZE = 1024
    ADDRESS = ("localhost", 9106)  # TODO: IP
    SEPARATOR = " | "

    CHECK_PERIOD = 1 / 2  # how frequently to check for new messages
    received_message: Optional[str] = None  # the last received message

    def __init__(self, uid: Optional[str] = None):
        self.mynt_id = None
        self.uid = uid or hex(get_mac())

        asyncio.ensure_future(self.periodic_send())

    def __join(self, *args) -> bytes:
        """Create a message by joining parts of it using a separator"""
        return (self.SEPARATOR.join(args) + "\n").encode()

    def set_mynt_id(self, mynt_id: str):
        """Set the Mynt ID that the client will attempt to connect to. Note that this
        function must be called before functions like send and receive are use!"""
        self.mynt_id = mynt_id

    @connect_and_close
    async def send(self, _, writer, data: str):
        """A function for sending data to the Mynt server."""
        writer.write(self.__join(self.uid, self.mynt_id, data))

    @connect_and_close
    async def receive(self, reader, writer):
        """A function for receiving data from the Mynt server."""
        writer.write(self.__join(self.uid, self.mynt_id))
        return (await reader.read(self.MAX_MESSAGE_SIZE)).decode()

    async def periodic_send(self):
        """An async function for periodically receiving data from the server and placing
        it in a variable."""
        while True:
            self.received_message = await self.receive()

            await asyncio.sleep(self.CHECK_PERIOD)

    def get_received_message(self) -> Optional[str]:
        """Return the last received message and clear the received_message variable."""
        message = self.received_message
        self.received_message = None
        return message


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
