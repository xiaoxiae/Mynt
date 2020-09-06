"""A module for communicating with the Mynt server."""
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from typing import *
from time import sleep
from uuid import getnode as get_mac


class Client:
    """A class for talking to the Mynt server (as a client)."""

    MAX_MESSAGE_SIZE = 1024  # TODO: read from some config file
    ADDRESS = ("localhost", 9106)  # TODO: IP

    def __init__(self, mynt_id: str, uid: Optional[str] = None):
        self.mynt_id = mynt_id
        self.uid = uid or hex(get_mac())

    def connect(function):
        """a decorator for connecting to the server using a socket, doing stuff and
        then closing the socket."""

        def wrapper(self, *args, **kwargs):
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(self.ADDRESS)
            result = function(self, sock, *args, **kwargs)
            sock.close()
            return result

        return wrapper

    @connect
    def send(self, sock: socket, data: Optional[str] = None):
        """A function for sending data to the Mynt server. If no data is specified, only
        the UID and Mynt ID are sent, prompting the server to send a message back."""
        sock.sendall(f"{self.uid} | {self.mynt_id} | {data}\n".encode("utf-8"))

    @connect
    def receive(self, sock: socket) -> str:
        """A private function for receiving data from the Mynt server."""
        sock.sendall(f"{self.uid} | {self.mynt_id}\n".encode("utf-8"))
        return sock.recv(self.MAX_MESSAGE_SIZE).decode("utf-8")


# try to talk between the two clients (when the server is running)
if __name__ == "__main__":
    c1 = Client("m1", "c1")
    c2 = Client("m1", "c2")

    c1.send("test")
    print(c2.receive())
