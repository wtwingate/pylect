from enum import Enum
import json


class Year(Enum):
    A = 0
    B = 1
    C = 2


class Rank(Enum):
    MINOR = 0
    MAJOR = 1
    SUNDAY = 2
    FIXED = 3
    PRINCIPAL = 4


with open("lectionary.json") as f:
    LECTIONARY = json.load(f)
