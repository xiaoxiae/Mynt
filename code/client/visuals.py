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

    def to_tuple(self) -> Tuple[int, int, int]:
        """Return the color as a tuple."""
        return int(self.r), int(self.g), int(self.b)

    def to_rgb(color) -> str:
        """Return the color as a RRRGGGBBB string. Mostly for testing."""
        return "#%02x%02x%02x" % color.to_tuple()

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

    def sinify(self, x: float) -> float:
        """Run through a sin function that returns values \in [0, 1]"""
        return 1 - (cos(x * pi * 2) + 1) / 2

    def get_period(self) -> float:
        """Return, which period the animation is on."""
        period = (time() - self.offset) / self.period

        if period > 1 and not self.repeats:
            period = 0.99999

        return period

    def __init__(self, period, offset=0, led_count=5, repeats=True):
        self.period = period
        self.led_count = led_count
        self.repeats = repeats

        # the animations are based on $current time - this offset$
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
        color = self.c1.interpolate(self.c2, self.sinify(self.get_period()))
        return [color] * self.led_count


class MetronomeAnimation(Animation):
    """A metronome animation -- from one end of the LEDs to the other."""

    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def __call__(self):
        # all colors are 0
        colors = [Color(0, 0, 0) for _ in range(self.led_count)]

        # LED position, based on the period
        pos = self.sinify(self.get_period()) * (self.led_count - 1)

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
        colors = [Color(0, 0, 0) for _ in range(self.led_count)]

        pos = self.get_period() * self.led_count

        l1 = int(pos) % self.led_count
        l2 = int(ceil(pos)) % self.led_count

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
        colors = [Color(0, 0, 0) for _ in range(self.led_count)]

        pos = self.get_period() * self.led_count
        colors[int(pos) % self.led_count] = self.color.darker(pos - int(pos))

        for i in range(int(pos) % self.led_count):
            colors[i] = self.color

        return colors


class TransitionAnimation(Animation):
    """An animation transition - slowly transition from one animation to another."""

    def __init__(self, a1: Animation, a2: Animation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a1 = a1
        self.a2 = a2

        self.offset = time()
        self.repeats = False

        self.prev_c = None

    def __call__(self):
        c = self.get_period()

        colors = []
        a1c = self.a1()
        a2c = self.a2()

        for i in range(self.led_count):
            colors.append(a1c[i].interpolate(a2c[i], c))

        # if the transition is over, discard the first animation
        # this way there isn't an infinite recursion
        # might look odd, but will likely simplify the code immensely
        if self.prev_c == c and self.a1 is not self.a2:
            self.a1 = self.a2

        self.prev_c = c

        return colors


# runs testing code when ran as a module
if __name__ == "__main__":
    import tkinter

    top = tkinter.Tk()

    r = 100

    a1 = MetronomeAnimation(Color(255, 0, 0), 1)
    a2 = PulsingAnimation(Color(0, 255, 0), Color(255, 0, 0), 1)

    animation = TransitionAnimation(a1, a2, 1)

    canvas = tkinter.Canvas(top, bg="blue", height=r, width=r * animation.led_count)
    canvas.pack()

    while True:
        top.update_idletasks()
        top.update()

        for i in range(animation.led_count):
            color = animation()[i].to_rgb()
            canvas.create_rectangle(i * r, 0, (i + 1) * r, r, fill=color)
