"""A module for handing anything color/animation related."""
from __future__ import annotations
from dataclasses import dataclass
from typing import *
from math import cos, pi, ceil
from abc import ABC, abstractmethod
from time import time
from random import randint, seed

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


class Animation(ABC):
    """A base class for all LED animations."""

    LED_COUNT: int = 5  # how many LEDs there are to animate

    def sinify(self, x: float) -> float:
        """Run through a sin function that returns values \in [0, 1]"""
        return 1 - (cos(x * pi * 2) + 1) / 2

    def get_period(self):
        """Return, which period the animation is on."""
        return (time() - self.offset) / self.period

    def __init__(self, period, repeats=True, offset=0):
        self.period = period
        self.repeats = repeats

        # the animations are based on time - this offset
        # this is done so animations can properly start and smoothly transition
        self.offset = offset

    @abstractmethod
    def __call__(self) -> Tuple[Tuple[int, int, int]]:
        """All animations must be callable and return a tuple of the LED colors."""


class PulsingAnimation(Animation):
    """A pulsing animation -- from color to color in a sine wave."""

    def __init__(self, c1: Color, c2: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.c1 = c1
        self.c2 = c2

    def __call__(self):
        return [
            self.c1.interpolate(self.c2, self.sinify(self.get_period()))
        ] * self.LED_COUNT


class MetronomeAnimation(Animation):
    """A metronome animation -- from one end of the LEDs to the other."""

    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def __call__(self):
        colors = [Color(0, 0, 0) for _ in range(self.LED_COUNT)]

        # LED position
        pos = self.sinify(self.get_period()) * (self.LED_COUNT - 1)

        l1 = int(pos)
        l2 = int(ceil(pos))

        l1_c = 1 - (pos - int(pos))
        l2_c = 1 - (int(ceil(pos)) - pos)

        colors[l1] = self.color.darker(l1_c)
        colors[l2] = self.color.darker(l2_c)

        return colors


class LinearAnimation(Animation):
    """A linear animation -- from one end of the LEDs to the other."""

    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def __call__(self):
        colors = [Color(0, 0, 0) for _ in range(self.LED_COUNT)]

        pos = self.get_period() * self.LED_COUNT

        l1 = int(pos) % self.LED_COUNT
        l2 = int(ceil(pos)) % self.LED_COUNT

        l1_c = 1 - (pos - int(pos))
        l2_c = 1 - (int(ceil(pos)) - pos)

        colors[l1] = self.color.darker(l1_c)
        colors[l2] = self.color.darker(l2_c)

        return colors


class ProgressAnimation(Animation):
    """Like linear animation, but fills up the progress bar."""

    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def __call__(self):
        colors = [Color(0, 0, 0) for _ in range(self.LED_COUNT)]

        pos = self.get_period() * self.LED_COUNT
        colors[int(pos) % self.LED_COUNT] = self.color.darker(pos - int(pos))

        for i in range(int(pos) % self.LED_COUNT):
            colors[i] = self.color

        return colors


# runs testing code when ran as a module
if __name__ == "__main__":
    import tkinter

    def from_rgb(color):
        return "#%02x%02x%02x" % (int(color.r), int(color.g), int(color.b))

    top = tkinter.Tk()

    r = 50

    canvas = tkinter.Canvas(top, bg="blue", height=r, width=r * Animation.LED_COUNT)
    canvas.pack()

    animation = ProgressAnimation(Color(200, 200, 200), 1)  # TODO add animation here

    while True:
        top.update_idletasks()
        top.update()

        for i in range(Animation.LED_COUNT):
            color = from_rgb(animation()[i])
            canvas.create_rectangle(i * r, 0, (i + 1) * r, r, fill=color)
