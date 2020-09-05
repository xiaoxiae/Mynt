"""A module for working with the configuration file. Most of the code is stolen from my
other project: https://github.com/xiaoxiae/Education-Scripts."""
from typing import *
from dataclasses import *
from yaml import safe_load, YAMLError
import sys
import os
from typeguard import check_type


class Strict:
    """A class for checking whether each of the dataclass variable types matches."""

    def __post_init__(self):
        """Perform the check."""
        for name, field_type in self.__annotations__.items():
            check_type("", self.__dict__[name], field_type)


@dataclass
class Wifi(Strict):
    name: str
    password: Optional[str] = None


@dataclass
class Configuration(Strict):
    wifi: List[Wifi]
    id: str

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
        elif get_origin(c) is list:
            return [recursion(cls, get_args(c)[0], i) for i in d]
        else:
            return d

    @classmethod
    def from_file(cls, path: str):
        """Initialize a Configuration object from a file. Returns None if the file
        doesn't exist, can't be open or the parsing failed."""
        try:
            with open(path, "r") as f:
                return Configuration.from_dictionary(safe_load(f) or {})
        except Exception as e:
            print(e)


class ConfigurationWatcher:
    """A class for interacting with the configuration (and watching for changes)."""

    PATH = "/home/pi/mynt/config.txt"

    def __init__(self, path=PATH):
        self.path = path
        self.__update_configuration()
        self.modified_time = None

    def __update_configuration(self):
        """Re-parse the configuration, setting it to None if it is not present."""
        self.configuration = Configuration.from_file(self.path)

    def changed(self):
        """Check the modified time of the configuration, returning True if it has
        changed since the last time we checked and False if not."""
        # Checking for the existence of the file doesn't work here, since getmtime seems
        # to fail, when the file is inaccessible due to (for example) someone writing
        # to it. That's why try-except is used here.
        try:
            mtime = os.path.getmtime(self.path)
        except FileNotFoundError:
            mtime = None

        result = mtime != self.modified_time
        self.modified_time = mtime

        if result:
            self.__update_configuration()

        return result


if __name__ == "__main__":
    cw = ConfigurationWatcher(
        "/home/xiaoxiae/Documents/Education/Programming/Other/projects/Mynt/code/setup/config/mynt/config.txt"
    )

    print(cw.configuration)
