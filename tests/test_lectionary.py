from datetime import date
from pylect.lectionary import Lectionary


class TestMoveableDates:
    def test_march_22(self):
        """Tests the earliest possible date of Easter."""
        lectionary = Lectionary(date(2285, 1, 1))
        expect = {
            "easter_day": date(2285, 3, 22),
            "sundays_after_epiphany": 4,
            "ash_wednesday": date(2285, 2, 4),
            "ascension_day": date(2285, 4, 30),
            "pentecost": date(2285, 5, 10),
            "proper_after_trinity": 3,
            "advent_sunday": date(2285, 11, 29),
        }
        assert lectionary.moveable_dates == expect

    def test_april_25(self):
        """Tests the latest possible date for Easter."""
        lectionary = Lectionary(date(2038, 1, 1))
        expect = {
            "easter_day": date(2038, 4, 25),
            "sundays_after_epiphany": 9,
            "ash_wednesday": date(2038, 3, 10),
            "ascension_day": date(2038, 6, 3),
            "pentecost": date(2038, 6, 13),
            "proper_after_trinity": 8,
            "advent_sunday": date(2038, 11, 28),
        }
        assert lectionary.moveable_dates == expect

    def test_leap_year(self):
        """Tests that calculations account for leap years."""
        lectionary = Lectionary(date(2024, 1, 1))
        expect = {
            "easter_day": date(2024, 3, 31),
            "sundays_after_epiphany": 6,
            "ash_wednesday": date(2024, 2, 14),
            "ascension_day": date(2024, 5, 9),
            "pentecost": date(2024, 5, 19),
            "proper_after_trinity": 4,
            "advent_sunday": date(2024, 12, 1),
        }
        assert lectionary.moveable_dates == expect
