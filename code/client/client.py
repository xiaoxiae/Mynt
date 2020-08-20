"""A module for communicating with the Mynt server."""
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(sock.connect(('localhost', 9106)))

class MyntClient:
    """A class for interacting with the Mynt server."""

