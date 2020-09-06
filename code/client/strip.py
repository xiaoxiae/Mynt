import board
import neopixel
from typing import *


class Strip:
    LED_COUNT = 5
    PIN = board.D18
    BRIGHTNESS = 0.05  # the LEDs are insanely bright

    def __init__(self):
        self.strip = neopixel.NeoPixel(
            self.PIN, self.LED_COUNT, brightness=self.BRIGHTNESS, auto_write=False
        )

    def set_color(self, i: int, color: Tuple[int]):
        """Set the color of the i-th diode of the strip."""
        self.strip[i] = color

    def display(self):
        """Display the currently set colors."""
        self.strip.show()
