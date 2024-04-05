import datetime as dt
from pylect.lectionary import Lectionary


class TestGetHolyDays:
    lectionary = Lectionary()

    def test_year_a(self):
        date = dt.date(2022, 11, 27)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["year"] == "Year A"
        assert day["season"] == "Advent"
        assert day["name"] == "The First Sunday in Advent"
        assert day["lessons"] == [
            "Isa 2:1-5",
            "Ps 122",
            "Rom 13:8-14",
            "Matt 24:29-44",
        ]

    def test_year_b(self):
        date = dt.date(2023, 12, 3)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["year"] == "Year B"
        assert day["season"] == "Advent"
        assert day["name"] == "The First Sunday in Advent"
        assert day["lessons"] == [
            "Isa 64:1-9a",
            "Ps 80 or 80:1-7v",
            "1 Cor 1:1-9",
            "Mark 13:24-37",
        ]

    def test_year_c(self):
        date = dt.date(2024, 12, 1)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["year"] == "Year C"
        assert day["season"] == "Advent"
        assert day["name"] == "The First Sunday in Advent"
        assert day["lessons"] == [
            "Zech 14:(1-2)3-9",
            "Ps 50 or 50:1-6",
            "1 Thess 3:6-13",
            "Luke 21:25-33",
        ]

    def test_christmas_day(self):
        date = dt.date(2022, 12, 25)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "The Nativity of Our Lord Jesus Christ: Christmas Day I"

    def test_one_sunday_after_christmas_one(self):
        date = dt.date(2023, 12, 31)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "The First Sunday of Christmas"

    def test_one_sunday_after_christmas_two(self):
        date = dt.date(2023, 1, 1)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "The First Sunday of Christmas"

    def test_two_sundays_after_christmas_one(self):
        first_sunday = dt.date(2020, 12, 27)
        second_sunday = dt.date(2021, 1, 3)
        results = self.lectionary.get_holy_days([first_sunday, second_sunday])
        day_one = results[0]
        day_two = results[1]
        assert day_one["name"] == "The First Sunday of Christmas"
        assert day_two["name"] == "The Second Sunday of Christmas"

    def test_two_sundays_after_christmas_two(self):
        first_sunday = dt.date(2024, 12, 29)
        second_sunday = dt.date(2025, 1, 5)
        results = self.lectionary.get_holy_days([first_sunday, second_sunday])
        day_one = results[0]
        day_two = results[1]
        assert day_one["name"] == "The First Sunday of Christmas"
        assert day_two["name"] == "The Second Sunday of Christmas"

    def test_short_epiphany(self):
        date = dt.date(2285, 2, 1)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "The Last Sunday of Epiphany: Transfiguration"

    def test_long_epiphany(self):
        date = dt.date(2038, 3, 7)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "The Last Sunday of Epiphany: Transfiguration"

    def test_short_after_pentecost(self):
        date = dt.date(2038, 6, 27)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Proper 8"

    def test_long_after_pentecost(self):
        date = dt.date(2285, 5, 24)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Proper 3"

    def test_ash_wednesday(self):
        date = dt.date(2025, 3, 5)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Ash Wednesday"

    def test_holy_week_one(self):
        date = dt.date(2025, 4, 13)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Palm Sunday"

    def test_holy_week_two(self):
        date = dt.date(2025, 4, 14)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Monday of Holy Week"

    def test_easter_week(self):
        date = dt.date(2025, 4, 20)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Easter Day: Principal Service"

    def test_all_saints_day_midweek(self):
        date = dt.date(2020, 11, 1)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "All Saints' Day"

    def test_all_saints_day_sunday(self):
        date = dt.date(2024, 11, 1)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "All Saints' Day"

    def test_red_letter_day_weekday(self):
        date = dt.date(2025, 12, 26)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "Stephen, Deacon and Martyr"

    def test_red_letter_day_sunday(self):
        date = dt.date(2025, 12, 28)
        results = self.lectionary.get_holy_days([date])
        day = results[0]
        assert day["name"] == "The First Sunday of Christmas"
