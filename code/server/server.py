#!/usr/bin/env python3

from dataclasses import dataclass
from threading import *
from socket import *
from typing import *
import os


class MyntDeviceThread(Thread):
    """A thread class that handles a single Mynt device."""

    def __init__(self, client, address, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = client
        self.address = address

        self.start()

    def run(self):
        while True:
            pass


class MyntGroupThread(Thread):
    """A thread class that handles a group of Mynt devices with the same ID."""

    threads: List[MyntDeviceThread] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start()

    def run(self):
        while True:
            pass

    def add_thread(self, t: MyntDeviceThread):
        self.threads.append(t)


class MyntServer:

    groups: Dict[str, MyntGroupThread] = {}

    IP: str = "127.0.0.1"
    PORT: int = 9106

    def run(self):
        """Run the server, watching for sockets and spawning thread groups."""
        s = socket()
        s.bind((self.IP, self.PORT))
        s.listen(5)

        try:
            while True:
                client, address = s.accept()

                # first read the ID (of a reasonable length)
                id = client.recv(2048)

                # spawn a new group, if the ID was not yet read
                if not id in self.groups:
                    mgt = MyntGroupThread()
                    self.groups[id] = mgt

                # spawn a new thread handling the client
                mdt = MyntDeviceThread(client, address)
                mdt.start()
                self.groups[id].add_thread(mdt)

        except KeyboardInterrupt:
            pass

        s.close()


if __name__ == "__main__":
    server = MyntServer()
    server.run()
