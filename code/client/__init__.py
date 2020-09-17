import os
from asyncio 

from visuals import *
from configuration import *


class Mynt:
    """A class representing the state of Mynt."""

    def __init__(self):
        self.configuration = ConfigurationWatcher()
        self.animation = Animations.DEFAULT

    async def run(self):
        """The main program loop."""

        # TODO: LEDs
        # TODO: communication with the server

        if self.cw.changed():
            if self.cw.configuration is None:
                self.animation = Animations.ERROR


if __name__ == "__main__":
    mynt = Mynt()
    mynt.run()
