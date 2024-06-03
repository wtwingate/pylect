# pylint: skip-file

from datetime import date

from pylect.lectionary import Lectionary


class TestMoveableDates:
    def test_march_22(self):
        """Tests the earliest possible date of Easter."""
        lectionary = Lectionary(date(2285, 1, 1))
        expect = {
            "easter_day": date(2285, 3, 22),
            "ash_wednesday": date(2285, 2, 4),
            "pentecost": date(2285, 5, 10),
            "advent_sunday": date(2285, 11, 29),
        }
        assert lectionary.moveable_dates == expect

    def test_april_25(self):
        """Tests the latest possible date for Easter."""
        lectionary = Lectionary(date(2038, 1, 1))
        expect = {
            "easter_day": date(2038, 4, 25),
            "ash_wednesday": date(2038, 3, 10),
            "pentecost": date(2038, 6, 13),
            "advent_sunday": date(2038, 11, 28),
        }
        assert lectionary.moveable_dates == expect

    def test_leap_year(self):
        """Tests that calculations account for leap years."""
        lectionary = Lectionary(date(2024, 1, 1))
        expect = {
            "easter_day": date(2024, 3, 31),
            "ash_wednesday": date(2024, 2, 14),
            "pentecost": date(2024, 5, 19),
            "advent_sunday": date(2024, 12, 1),
        }
        assert lectionary.moveable_dates == expect
