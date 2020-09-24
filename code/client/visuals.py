"""A module for anything color/animation related."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import ceil, cos, pi
from time import time
from typing import *

Numeric = Union[int, float]


def linear_interpolation(a: Numeric, b: Numeric, x: Numeric) -> Numeric:
    """Interpolate between a and b. $x \\in [0, 1]$"""
    return a * (1 - x) + b * x


def sinify(x: float) -> float:
    """Run through a sin function that returns values \\in [0, 1]"""
    return 1 - (cos(x * pi * 2) + 1) / 2


@dataclass
class Color:
    r: Numeric
    g: Numeric
    b: Numeric

    def to_tuple(self) -> Tuple[int, int, int]:
        """Return the color as a tuple."""
        return int(self.r), int(self.g), int(self.b)

    def to_rgb(self) -> str:
        """Return the color as a RRRGGGBBB string. Mostly for testing."""
        return "#%02x%02x%02x" % self.to_tuple()

    def interpolate(self, other: Color, x: Numeric) -> Color:
        """Interpolate between two colors. $x \\in [0, 1]$"""
        return Color(
            linear_interpolation(self.r, other.r, x),
            linear_interpolation(self.g, other.g, x),
            linear_interpolation(self.b, other.b, x),
        )

    def darker(self, coefficient: float):
        """Darken the color to a certain coefficient."""
        return Color(self.r * coefficient, self.g * coefficient, self.b * coefficient)


class Animation(ABC):
    """A base class for all LED animations."""

    def get_period(self) -> float:
        """Return, which period the animation is on."""
        period = (time() - self.offset) / self.period

        # if we're not repeating, stay stuck at the last state of the animation
        if period > 1 and not self.repeats:
            period = 0.99999

        return period

    def __init__(self, period: int, offset=0, led_count=5, repeats=True):
        self.period = period
        self.led_count = led_count
        self.repeats = repeats

        # the animations are based on $current time - this offset$
        # this is done so animations can properly start and smoothly transition
        # if offset is -1, it is set to current time to start the animation from the
        # beginning
        self.offset = offset if offset != -1 else time()

    @abstractmethod
    def __call__(self) -> Tuple[Color]:
        """All animations must be callable and return a tuple of the LED colors."""


class PulsingAnimation(Animation):
    """A pulsing animation - from color to color in a sine wave."""

    def __init__(self, c1: Color, c2: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.c1 = c1
        self.c2 = c2

    def __call__(self):
        color = self.c1.interpolate(self.c2, sinify(self.get_period()))
        return [color] * self.led_count


class MetronomeAnimation(Animation):
    """A metronome animation - from one end of the LEDs to the other."""

    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def __call__(self):
        # all colors are 0
        colors = [Color(0, 0, 0) for _ in range(self.led_count)]

        # LED position, based on the period
        pos = sinify(self.get_period()) * (self.led_count - 1)

        l1 = int(pos)
        l2 = int(ceil(pos))

        l1_c = 1 - (pos - int(pos))
        l2_c = 1 - (int(ceil(pos)) - pos)

        colors[l1] = self.color.darker(l1_c)
        colors[l2] = self.color.darker(l2_c)

        return colors


class LinearAnimation(Animation):
    """A linear animation - from one end of the LEDs to the other."""

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


class ChainedAnimation(Animation):
    """A sequence of animations chained one after another."""

    def __init__(self, *args: Animation, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO - period is based on the provided animations


class Colors:
    NONE = Color(0, 0, 0)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    WHITE = Color(255, 255, 255)
    PINK = Color(170, 0, 50)


class Animations:
    """All the different animations of Mynt."""

    DEFAULT = lambda: Colors.NONE  # nothing
    ERROR = PulsingAnimation(Colors.NONE, Colors.RED, 1)

    CONFIGURATION_READ = PulsingAnimation(
        Colors.NONE, Colors.WHITE, 2, repeats=False, offset=-1
    )

    CONNECTING_TO_WIFI = MetronomeAnimation(Colors.WHITE, 1.5)  # white
    CONNECTING_TO_SERVER = MetronomeAnimation(Colors.GREEN, 1.5)  # green

    # transitions from white to pink briefly when a beat is detected
    CONTACTING_PAIR_BLANK = LinearAnimation(Colors.WHITE, 1.5)  # white
    CONTACTING_PAIR_BEAT = LinearAnimation(Colors.PINK, 1.5)  # pink


# runs testing code when ran as a module
if __name__ == "__main__":
    import tkinter

    top = tkinter.Tk()

    r = 100

    animation = Animations.CONFIGURATION_READ

    canvas = tkinter.Canvas(top, bg="blue", height=r, width=r * animation.led_count)
    canvas.pack()

    while True:
        top.update_idletasks()
        top.update()

        for i in range(animation.led_count):
            color = animation()[i].to_rgb()
            print(animation()[i].to_tuple())
            canvas.create_rectangle(i * r, 0, (i + 1) * r, r, fill=color)
