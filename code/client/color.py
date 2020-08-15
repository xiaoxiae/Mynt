from __future__ import annotations
from dataclasses import dataclass
from typing import *

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
