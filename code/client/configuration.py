"""A module for working with Mynt's configuration file. Most of the code is stolen from
my other project: https://github.com/xiaoxiae/Education-Scripts."""
import os
from dataclasses import *
from typing import *

from typeguard import check_type
from yaml import safe_load


class Strict:
    """A class for checking whether each of the dataclass variable types matches."""

    def __post_init__(self):
        """Perform the check."""
        # disabled because Pylint doesn't understand the magical __annotations__...
        # pylint: disable=E1101
        for name, field_type in self.__annotations__.items():
            check_type("", self.__dict__[name], field_type)


@dataclass
class Wifi(Strict):
    name: str
    password: Optional[str] = None


@dataclass
class Configuration(Strict):
    wifi: List[Wifi]
    id: str  # Mynt ID, but 'id' is more understandable to a common user

    @classmethod
    def from_dictionary(cls, d: Dict):
        """Initialize a Configuration object from the given dictionary."""
        return cls.__from_dictionary(cls, d)

    @classmethod
    def __from_dictionary(cls, c, d):
        """A helper function that converts a nested dictionary to a dataclass.
        Inspired by https://stackoverflow.com/a/54769644."""

        def recursion(cls, c, d):
            fieldtypes = {f.name: f.type for f in fields(c)}
            return c(**{f: cls.__from_dictionary(fieldtypes[f], d[f]) for f in d})

        if is_dataclass(c):
            return recursion(cls, c, d)

        if get_origin(c) is list:
            return [recursion(cls, get_args(c)[0], i) for i in d]

        return d

    @classmethod
    def from_file(cls, path: str):
        """Initialize a Configuration object from a file. Returns None if the file
        doesn't exist, can't be open or the parsing failed."""
        # we don't care about specific exceptions in this case
        # pylint: disable=W0703
        try:
            with open(path, "r") as f:
                return Configuration.from_dictionary(safe_load(f) or {})
        except Exception:
            pass


class ConfigurationWatcher:
    """A class for watching for changes in the configuration file and reading it."""

    PATH = "/home/pi/mynt/config.txt"

    def __init__(self, path=PATH):
        self.path = path
        self.last_mtime = None

    def changed(self):
        """Check the modified time of the configuration, returning True if it has
        changed since the last time we checked and False if not."""
        # Checking for the existence of the file doesn't work here, since getmtime seems
        # to fail, when the file is inaccessible due to (for example) someone writing
        # to it. That's why try-except is used here.
        try:
            new_mtime = os.path.getmtime(self.path)
        except FileNotFoundError:
            new_mtime = None

        result = new_mtime != self.last_mtime
        self.last_mtime = new_mtime

        return result

    def get(self):
        """Return the configuration."""
        return Configuration.from_file(self.PATH)
