"""A Python module for controlling a Mynt."""
import asyncio
import os

from client.client import *
from client.configuration import *
from client.sensor import *
from client.strip import *
from client.visuals import *


class Mynt:
    """A class representing the state of Mynt."""

    LOOP_PERIOD = 1 / 60

    def __init__(self):
        # configuration
        self.cw = ConfigurationWatcher()
        self.configuration = self.cw.get()

        # visuals
        self.animation = Animations.DEFAULT
        self.strip = Strip()

        # server
        self.client = Client()
        # TODO: set Mynt ID

        # sensor
        self.sensor = Sensor()

    async def run(self):
        """The main program loop."""
        while True:
            # update configuration
            if self.cw.changed():
                self.configuration = self.cw.get()
                # TODO: error / config load animation

            # if the sensor detected something
            if self.sensor.check():
                # TODO: animation change
                # TODO: communication with the server
                pass

            # if a new message was received
            if message := self.client.get_received_message():
                # TODO: animation change
                pass

            # animate
            self.strip.animate(self.animation)

            await asyncio.sleep(self.LOOP_PERIOD)
            print("LOOP")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mynt().run())
