from __future__ import annotations
from typing import *
from dataclasses import *
from yaml import safe_load, YAMLError
import sys


@dataclass
class Strict:
    """A class for strictly checking whether each of the dataclass var types match."""

    def __post_init__(self):
        """Perform the check."""
        for name, field_type in self.__annotations__.items():
            value = self.__dict__[name]

            # ignore None values and Any types
            if value is None or field_type is Any:
                continue

            # go through all of the field types and check the types
            for f in (
                get_args(field_type)
                if get_origin(field_type) is Union
                else [field_type]
            ):
                if isinstance(value, f):
                    break
            else:
                raise TypeError(
                    f"The key '{name}' "
                    + f"in class {self.__class__.__name__} "
                    + f"expected '{field_type.__name__}' "
                    + f"but got '{type(value).__name__}' instead."
                )


@dataclass
class Wifi(Strict):
    name: str
    password: str


@dataclass
class Configuration(Strict):
    wifi: Wifi

    @classmethod
    def from_dictionary(cls, d: Dict):
        """Initialize a Configuration object from the given dictionary."""
        return cls.__from_dictionary(cls, d)

    @classmethod
    def __from_dictionary(cls, c, d):
        """A helper function that converts a nested dictionary to a dataclass.
        Inspired by https://stackoverflow.com/a/54769644."""
        if is_dataclass(c):
            fieldtypes = {f.name: f.type for f in fields(c)}
            return c(**{f: cls.__from_dictionary(fieldtypes[f], d[f]) for f in d})
        else:
            return d

    @classmethod
    def from_file(cls, path: str) -> Configuration:
        """Initialize a Configuration object from a file. Can throw exceptions."""
        with open(path, "r") as f:
            return Configuration.from_dictionary(safe_load(f) or {})
