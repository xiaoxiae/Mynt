#!/usr/bin/env python3

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 9106))
sock.listen(1)

while True:
    print("waiting")
    connection, client_address = sock.accept()

    print(connection, client_address)

class MyntServer:
    """A class for serving the Mynt clients."""
