"""A Python module for controlling a Mynt."""
import os

from client.configuration import *
from client.visuals import *


class Mynt:
    """A class representing the state of Mynt."""

    def __init__(self):
        # configuration
        self.cw = ConfigurationWatcher()
        self.configuration = self.cw.get()

        # visuals
        self.animation = Animations.DEFAULT
        self.strip = Strip()

        # client version (for automatic updates)
        self.version = "0.1"

    def run(self):
        """The main program loop $n$ times per second."""
        # update configuration
        if self.cw.changed():
            self.configuration = self.cw.get()

            # TODO: error / config load animation

        # animate
        self.strip.animate(self.animation)

        # TODO: communication with the server


if __name__ == "__main__":
    mynt = Mynt()
    mynt.run()
