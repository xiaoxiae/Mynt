"""A module for working with the configuration file. Most of the code is stolen from my
other project: https://github.com/xiaoxiae/Education-Scripts."""
from typing import *
from dataclasses import *
from yaml import safe_load, YAMLError
import sys
import os


@dataclass
class Strict:
    """A class for strictly checking whether each of the dataclass variable types
    match."""

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
    password: Optional[str]


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
    def from_file(cls, path: str):
        """Initialize a Configuration object from a file. Returns None if the file
        doesn't exist, can't be open or the parsing failed."""
        try:
            with open(path, "r") as f:
                return Configuration.from_dictionary(safe_load(f) or {})
        except Exception:
            pass


class ConfigurationWatcher:
    """A class for interacting with the configuration (and watching for changes)."""

    # PATH = "/home/pi/mynt/config.txt"
    PATH = "/home/xiaoxiae/config.txt"

    def __init__(self):
        self.__update_configuration()
        self.modified_time = None

    def __update_configuration(self):
        """Re-parse the configuration."""
        self.configuration = Configuration.from_file(self.PATH)

    def changed(self):
        """Check the modified time of the configuration, returning True if it has
        changed since the last time we checked and False if not."""
        # Checking for the existence of the file doesn't work here, since getmtime seems
        # to fail, when the file is inaccessible due to (for example) someone writing
        # to it. That's why try-except is used here.
        try:
            mtime = os.path.getmtime(self.PATH)
        except FileNotFoundError:
            mtime = None

        result = mtime != self.modified_time
        self.modified_time = mtime

        if result:
            self.__update_configuration()

        return result
