import os
import logging
from json import loads
from typing import Optional, Any

from .exceptions import InvalidEnvironmentFormat


class Config:
    __slots__ = {"__dict__"}
    __DEFAULT: Any = None
    __KEYS: set = {""}

    def __init__(self, default_value: Optional[Any] = None):
        self.__DEFAULT = default_value
        self.__KEYS = set()

    def __getattr__(self, item):
        if item in self.__KEYS:
            return super().__getattribute__(item)
        logging.warning(f"The key \"{item}\" was accessed but is not set.")
        return self.__DEFAULT

    def __setattr__(self, key, value):
        if key in self.__KEYS:
            logging.warning(f"Updating the environment variable \"{key}\" to be \"{value}\" (previously \"{self.__getattr__(key)}\", is this intentional?)")
        super().__setattr__(key, value)

    @classmethod
    def from_file(cls, path: str):
        new, ln_num = cls(), 1

        with open(path, "r") as f:
            lines = [ln.split("#")[0].strip() for ln in f.readlines()]
        for line in lines:
            if not line:
                continue
            try:
                if line.count("=") >= 2:
                    key, key_type, value = line.split("=", 2)
                    key_type = key_type.upper()
                else:
                    key, value = line.split("=", 1)
                    key_type = "STR"
                key = key.upper()
            except ValueError:
                raise InvalidEnvironmentFormat(f"Invalid format on line {ln_num}: {line}")
            try:
                if value == "":
                    value = None
                elif key_type == "INT":
                    value = int(value)
                elif key_type == "BOOL":
                    value = value.upper() == "TRUE"
                elif key_type == "JSON" or key_type == "ARR":
                    value = loads(value)
                elif key_type != "STR":
                    raise InvalidEnvironmentFormat(f'Environment Key: "{key}" has an invalid type: "{key_type}". Type must be one of "STR", "INT", "BOOL", "ARR" or "JSON"')
                logging.debug(f'[ENV] Setting environment variable "{key}" of type "{key_type}" to "{fr'{value}'}"')
                new.__setattr__(key, value)
                new.__KEYS.add(key)
                os.environ[key] = str(value)
            except ValueError:
                InvalidEnvironmentFormat(f'Environment Key: "{key}" has an invalid value: "{value}"')
            ln_num += 1
        return new
