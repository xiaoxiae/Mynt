"""A module for working with Mynt's LED strip."""
from typing import *

import board
from neopixel import NeoPixel

from client.visuals import *


class Strip:
    LED_COUNT = 5
    PIN = board.D18
    BRIGHTNESS = 0.05  # the LEDs are insanely bright, 5% should be fine

    def __init__(self):
        self.strip = NeoPixel(
            self.PIN, self.LED_COUNT, brightness=self.BRIGHTNESS, auto_write=False
        )

    def animate(self, animation: Animation):
        """Set the color of the strip, given an animation."""
        for i, color in enumerate(animation()):
            self.strip[i] = color.to_tuple()

        self.strip.show()


if __name__ == "__main__":
    animation = MetronomeAnimation(Color(100, 200, 200), 1)
    strip = Strip()

    while True:
        strip.animate(animation)
