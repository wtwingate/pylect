"""Defines global constants used throughout the rest of the program."""

import json
from enum import Enum


class Rank(Enum):
    """Constant values for holy day precedence rankings."""

    MINOR = 0
    MAJOR = 1
    SUNDAY = 2
    FIXED = 3
    PRINCIPAL = 4


LECTIONARY: dict
with open("src/pylect/lectionary.json", "r", encoding="utf-8") as f:
    LECTIONARY = json.load(f)
