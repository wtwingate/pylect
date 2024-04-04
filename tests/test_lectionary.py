import datetime as dt

import pytest

from pylect.lectionary import Lectionary


class TestGetHolyDays:
    lectionary = Lectionary()

    def test_year_a(self):
        date = dt.date(2022, 11, 27)
        result = self.lectionary.get_holy_days([date])
        day = result[0]
        assert day.year == "Year A"
        assert day.season == "Advent"
        assert day.name == "The First Sunday in Advent"
        assert day.lessons == [
            "Isa 2:1-5",
            "Ps 122",
            "Rom 13:8-14",
            "Matt 24:29-44",
        ]

    def test_year_b(self):
        date = dt.date(2023, 12, 3)
        result = self.lectionary.get_holy_days([date])
        day = result[0]
        assert day.year == "Year B"
        assert day.season == "Advent"
        assert day.name == "The First Sunday in Advent"
        assert day.lessons == [
            "Isa 64:1-9a",
            "Ps 80 or 80:1-7v",
            "1 Cor 1:1-9",
            "Mark 13:24-37",
        ]

    def test_year_c(self):
        date = dt.date(2024, 12, 1)
        result = self.lectionary.get_holy_days([date])
        day = result[0]
        assert day.year == "Year C"
        assert day.season == "Advent"
        assert day.name == "The First Sunday in Advent"
        assert day.lessons == [
            "Zech 14:(1-2)3-9",
            "Ps 50 or 50:1-6",
            "1 Thess 3:6-13",
            "Luke 21:25-33",
        ]
