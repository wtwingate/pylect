from enum import Enum
import json


class Rank(Enum):
    MINOR = 0
    MAJOR = 1
    SUNDAY = 2
    FIXED = 3
    PRINCIPAL = 4


LECTIONARY: dict
with open("src/pylect/lectionary.json") as f:
    LECTIONARY = json.load(f)
