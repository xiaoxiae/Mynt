#!/usr/bin/env python3

from threading import *
from socket import *
from typing import *
import os


class MyntServer:

    groups: Dict[str, Thread] = {}

    IP: str = "127.0.0.1"
    PORT: int = 9106

    ID_LENGTH = 16

    @classmethod
    def spawn_id_thread(cls):
        """Spawn a thread that takes care of a single ID."""

    @classmethod
    def spawn_thread_group(cls):
        """Spawn a thread that takes care of a group of IDs."""

    def run(self):
        """Run the server, watching for sockets and spawning thread groups."""
        try:
            s = socket()
            s.bind((self.IP, self.PORT))
        except socket.error as e:
            print(str(e))

        s.listen(5)

        try:
            while True:
                client, address = s.accept()

                # first read the ID (of a reasonable length)
                id = client.recv(2048)

                if id in self.groups:
                    pass  # TODO: if a thread that handles this particular ID exists
                else:
                    pass  # TODO: spawn new thread that handles this ID
        except KeyboardInterrupt:
            pass

        s.close()


if __name__ == "__main__":
    server = MyntServer()
    server.run()
