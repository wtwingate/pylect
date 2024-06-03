"""Defines global constants used throughout the rest of the program."""

import json
from enum import Enum
from importlib.resources import files


class Rank(Enum):
    """Constant values for holy day precedence rankings."""

    MINOR = 0
    MAJOR = 1
    SUNDAY = 2
    FIXED = 3
    PRINCIPAL = 4


LECTIONARY: dict
lectionary_json = files("pylect.data").joinpath("lectionary.json")
with open(lectionary_json, "r", encoding="utf-8") as f:
    LECTIONARY = json.load(f)
