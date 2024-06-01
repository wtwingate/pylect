from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, SU
from dateutil.easter import easter
from pylect.constants import *
from pylect.holyday import HolyDay


class Lectionary:
    """The lectionary class provides methods for calculating holy days according
    to the liturgical calendar of the Anglican Church.
    """

    def __init__(self, given_date: date) -> None:
        self.date = given_date
        self.easter_day = self.__get_easter_day()
        self.moveable_dates = self.__get_moveable_dates()
        self.liturgical_year = self.__get_liturgical_year()
        self.liturgical_season = self.__get_liturgical_season()
        self.holy_days = self.__get_holy_days()

    def __get_easter_day(self) -> date:
        return easter(self.date.year)

    def __get_moveable_dates(self) -> dict[str, date]:
        return {
            "easter_day": self.easter_day,
            "ash_wednesday": self.__get_ash_wednesday(),
            "pentecost": self.__get_pentecost(),
            "advent_sunday": self.__get_advent_sunday(),
        }

    def __get_ash_wednesday(self) -> date:
        return self.easter_day - timedelta(days=46)

    def __get_pentecost(self) -> date:
        return self.easter_day + timedelta(days=49)

    def __get_advent_sunday(self) -> date:
        return date(self.date.year, 12, 25) + relativedelta(
            days=-1, weekday=SU(-4)
        )

    def __get_liturgical_year(self) -> int:
        if self.date >= self.moveable_dates["advent_sunday"]:
            return self.date.year % 3
        return (self.date.year - 1) % 3

    def __get_liturgical_season(self) -> str:
        if self.date < date(self.date.year, 1, 6):
            return "Christmas"
        if self.date < self.moveable_dates["ash_wednesday"]:
            return "Epiphany"
        if self.date < self.moveable_dates["easter_day"]:
            return "Lent"
        if self.date < self.moveable_dates["pentecost"]:
            return "Easter"
        if self.date < self.moveable_dates["advent_sunday"]:
            return "Pentecost"
        if self.date < date(self.date.year, 12, 25):
            return "Advent"
        return "Christmas"

    def __get_holy_days(self) -> list[HolyDay]:
        holy_days: list[HolyDay] = []
        self.__check_major_days(holy_days)
        self.__check_holy_week(holy_days)
        self.__check_easter_week(holy_days)
        self.__check_sundays(holy_days)
        self.__check_red_letter_days(holy_days)
        return holy_days

    def __check_major_days(self, holy_days: list[HolyDay]) -> None:
        if self.date == self.easter_day:
            holy_days.append(
                HolyDay(
                    "Easter Day",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == self.easter_day + timedelta(days=39):
            holy_days.append(
                HolyDay(
                    "Ascension Day",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == self.moveable_dates["pentecost"]:
            holy_days.append(
                HolyDay(
                    "The Day of Pentecost",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == self.easter_day + timedelta(days=56):
            holy_days.append(
                HolyDay(
                    "Trinity Sunday",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == date(self.date.year, 12, 25):
            holy_days.append(
                HolyDay(
                    "Christmas Day",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == date(self.date.year, 1, 6):
            holy_days.append(
                HolyDay(
                    "The Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == date(self.date.year, 11, 1):
            holy_days.append(
                HolyDay(
                    "All Saints' Day",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif self.date == self.moveable_dates["ash_wednesday"]:
            holy_days.append(
                HolyDay(
                    "Ash Wednesday",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )

    def __check_holy_week(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.easter_day - self.date
        day_name = HOLY_WEEK.get(date_delta.days)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )

    def __check_easter_week(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.easter_day
        day_name = EASTER_WEEK.get(date_delta.days)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )

    def __check_sundays(self, holy_days: list[HolyDay]) -> None:
        if self.date.weekday() != 6:
            return

        if self.liturgical_season == "Advent":
            self.__check_advent_sundays(holy_days)
        elif self.liturgical_season == "Christmas":
            self.__check_christmas_sundays(holy_days)
        elif self.liturgical_season == "Epiphany":
            self.__check_epiphany_sundays(holy_days)
        elif self.liturgical_season == "Lent":
            self.__check_lent_sundays(holy_days)
        elif self.liturgical_season == "Easter":
            self.__check_easter_sundays(holy_days)
        elif self.liturgical_season == "Pentecost":
            self.__check_pentecost_sundays(holy_days)

    def __check_advent_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.moveable_dates["advent_sunday"]
        day_name = ADVENT_SUNDAYS.get(date_delta.days)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )

    def __check_christmas_sundays(self, holy_days: list[HolyDay]) -> None:
        if (
            date(self.date.year, 12, 25)
            < self.date
            <= date(self.date.year + 1, 1, 1)
        ):
            holy_days.append(
                HolyDay(
                    "The First Sunday of Christmas",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        else:
            holy_days.append(
                HolyDay(
                    "The Second Sunday of Christmas",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )

    def __check_epiphany_sundays(self, holy_days: list[HolyDay]) -> None:
        first_sunday_of_epiphany = date(self.date.year, 1, 6) + relativedelta(
            days=+1, weekday=SU(+1)
        )
        date_delta = self.date - first_sunday_of_epiphany

        # The number of Sundays after Epiphany can range from 4 to 9.
        # To account for this, check for the final two Sundays first.
        if self.date == self.easter_day - timedelta(days=56):
            holy_days.append(
                HolyDay(
                    "The Second to Last Sunday of Epiphany: World Mission",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == self.easter_day - timedelta(days=49):
            holy_days.append(
                HolyDay(
                    "The Last Sunday of Epiphany: Transfiguration",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        else:
            day_name = EPIPHANY_SUNDAYS.get(date_delta.days)
            if day_name:
                holy_days.append(
                    HolyDay(
                        day_name,
                        self.liturgical_year,
                        self.liturgical_season,
                        1,
                    )
                )

    def __check_lent_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.easter_day - self.date
        day_name = LENT_SUNDAYS.get(date_delta.days)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )

    def __check_easter_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.easter_day
        day_name = EASTER_SUNDAYS.get(date_delta.days)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )

    def __check_pentecost_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.moveable_dates["advent_sunday"] - self.date
        day_name = PENTECOST_SUNDAYS.get(date_delta.days)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )

    def __check_red_letter_days(self, holy_days: list[HolyDay]) -> None:
        day_name = RED_LETTER_DAYS.get(self.date)
        if day_name:
            holy_days.append(
                HolyDay(
                    day_name,
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )


if __name__ == "__main__":
    for i in range(365):
        day = date.today() + timedelta(days=i)
        lectionary = Lectionary(day)
        for holy_day in lectionary.holy_days:
            print(day, holy_day.name)
