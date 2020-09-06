"""A module for working with the LED strip."""
import board
from neopixel import NeoPixel
from typing import *

from visuals import *


class Strip:
    LED_COUNT = 5
    PIN = board.D18
    BRIGHTNESS = 0.05  # the LEDs are insanely bright

    def __init__(self):
        self.strip = NeoPixel(
            self.PIN, self.LED_COUNT, brightness=self.BRIGHTNESS, auto_write=False
        )

    def set(self, animation: Animation):
        """Set the color of the strip, given an animation."""
        for i, color in enumerate(animation()):
            self.strip[i] = color

        self.strip.show()


if __name__ == "__main__":
    animation = MetronomeAnimation(Color(100, 200, 200), 1)
    strip = Strip()

    while True:
        strip.set(animation)
