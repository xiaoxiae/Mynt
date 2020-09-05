import time
from rpi_ws281x import PixelStrip
import argparse


class Strip:
    LED_COUNT = 5
    LED_PIN = 18
    LED_FREQ_HZ = 2000  # from WS2813 datasheet

    def __init__(self):
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, freq_hz=LED_FREQ_HZ)
        self.strip.begin()

    def set_color(self, i: int, color: int):
        """Set the color of the i-th diode of the strip."""
        strip.setPixelColor(i, color)

    def display(self):
        """Display the currently set colors."""
        strip.show()
