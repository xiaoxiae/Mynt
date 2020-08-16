from __future__ import annotations
from dataclasses import dataclass
from typing import *
from math import cos, pi, ceil
from functools import partial
from time import time

Numeric = Union[int, float]


@dataclass
class Color:
    """A class for working with colors."""

    r: Numeric
    g: Numeric
    b: Numeric

    def __call__(self) -> Tuple[int, int, int]:
        """Return the color in RGB."""
        return int(self.r), int(self.g), int(self.b)

    def __linear_interpolation(self, a: Numeric, b: Numeric, x: Numeric) -> Numeric:
        """Interpolate between a and b. $x \in [0, 1]$"""
        return a * (1 - x) + b * x

    def interpolate(self, other: Color, x: Numeric) -> Color:
        """Interpolate between two colors. $x \in [0, 1]$"""
        return Color(
            self.__linear_interpolation(self.r, other.r, x),
            self.__linear_interpolation(self.g, other.g, x),
            self.__linear_interpolation(self.b, other.b, x),
        )

    def darker(self, coefficient: float):
        """Darken the color to a certain coefficient."""
        return Color(self.r * coefficient, self.g * coefficient, self.b * coefficient)


class Animation:
    """A class for working with LED animations."""

    LED_COUNT: int = 5  # how many LEDs there are

    @classmethod
    def __sinify(cls, x):
        """Run through a sin function that returns values \in [0, 1]"""
        return 1 - (cos(x * pi) + 1) / 2

    @classmethod
    def __pulsing(cls, c1: Color, c2: Color, period: float, offset: float = 0):
        t = (time() - offset) / period * 2
        return [c1.interpolate(c2, cls.__sinify(t))] * cls.LED_COUNT

    @classmethod
    def pulsing(cls, c1: Color, c2: Color, period: float, offset: float = 0):
        """A pulsing animation -- from color to color in a sine wave."""
        return partial(cls.__pulsing, c1, c2, period, offset)

    @classmethod
    def __metronome(cls, color: Color, period: float, offset: float = 0):
        colors = [Color(0, 0, 0) for _ in range(cls.LED_COUNT)]
        t = (time() - offset) / period * 2

        led_position = cls.__sinify(t) * (cls.LED_COUNT - 1)

        l1 = int(led_position)
        l2 = int(ceil(led_position))

        l1_c = 1 - (led_position - int(led_position))
        l2_c = 1 - (int(ceil(led_position)) - led_position)

        colors[l1] = color.darker(l1_c)
        colors[l2] = color.darker(l2_c)

        return colors

    @classmethod
    def metronome(cls, color: Color, period: float, offset: float = 0):
        """A metronome animation -- from one end of the LEDs to the other."""
        return partial(cls.__metronome, color, period, offset)

    @classmethod
    def __linear(cls, color: Color, period: float, offset: float = 0):
        colors = [Color(0, 0, 0) for _ in range(cls.LED_COUNT)]
        t = (time() - offset) / period * 2

        l1 = int(t) % cls.LED_COUNT
        l2 = int(ceil(t)) % cls.LED_COUNT

        l1_c = 1 - (t - int(t))
        l2_c = 1 - (int(ceil(t)) - t)

        colors[l1] = color.darker(l1_c)
        colors[l2] = color.darker(l2_c)

        return colors

    @classmethod
    def linear(cls, color: Color, period: float, offset: float = 0):
        """A metronome animation -- from one end of the LEDs to the other."""
        return partial(cls.__linear, color, period, offset)


# TODO: předělat na třídy, tohle je vcelku oser
