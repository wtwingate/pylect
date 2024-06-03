"""Provides access to the Lectionary class."""

from datetime import date, timedelta

from dateutil.easter import easter
from dateutil.relativedelta import SU, relativedelta

from pylect.constants import Rank
from pylect.holyday import HolyDay


class Lectionary:
    """The Lectionary class provides a data structure which calculates the
    relevant data for how any given date in the Gregorian calendar relates
    to the Church's liturgical calendar. If any Sunday or Holy Day falls on
    the specified date, then a new HolyDay object is created and stored in
    the holy_days instance variable.
    """

    def __init__(self, this_date: date) -> None:
        self.date: date = this_date
        self.easter_day: date = self.__get_easter_day()
        self.moveable_dates: dict[str, date] = self.__get_moveable_dates()
        self.liturgical_year: str = self.__get_liturgical_year()
        self.liturgical_season: str = self.__get_liturgical_season()
        self.holy_days: list[HolyDay] = self.__get_holy_days()

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

    def __get_liturgical_year(self) -> str:
        if self.date >= self.moveable_dates["advent_sunday"]:
            start_year = self.date.year
        else:
            start_year = self.date.year - 1

        if start_year % 3 == 0:
            return "Year A"
        if start_year % 3 == 1:
            return "Year B"
        return "Year C"

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
        self.__check_principal_feasts(holy_days)
        self.__check_ash_wednesday(holy_days)
        self.__check_holy_week(holy_days)
        self.__check_easter_week(holy_days)
        self.__check_sundays(holy_days)
        self.__check_red_letter_days(holy_days)
        return holy_days

    def __check_principal_feasts(self, holy_days: list[HolyDay]) -> None:
        if self.date == self.easter_day:
            day_name = "Easter Day"
        elif self.date == self.easter_day + timedelta(days=39):
            day_name = "Ascension Day"
        elif self.date == self.moveable_dates["pentecost"]:
            day_name = "Day of Pentecost"
        elif self.date == self.easter_day + timedelta(days=56):
            day_name = "Trinity Sunday"
        elif self.date == date(self.date.year, 12, 25):
            day_name = "Christmas Day"
        elif self.date == date(self.date.year, 1, 6):
            day_name = "The Epiphany"
        elif self.date == date(self.date.year, 11, 1):
            day_name = "All Saints' Day"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.PRINCIPAL,
            )
        )

    def __check_ash_wednesday(self, holy_days: list[HolyDay]) -> None:
        if self.date == self.moveable_dates["ash_wednesday"]:
            holy_days.append(
                HolyDay(
                    "Ash Wednesday",
                    self.liturgical_year,
                    self.liturgical_season,
                    Rank.FIXED,
                )
            )

    def __check_holy_week(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.easter_day - self.date
        if date_delta.days == 7:
            day_name = "Palm Sunday"
        elif date_delta.days == 6:
            day_name = "Monday in Holy Week"
        elif date_delta.days == 5:
            day_name = "Tuesday in Holy Week"
        elif date_delta.days == 4:
            day_name = "Wednesday in Holy Week"
        elif date_delta.days == 3:
            day_name = "Maundy Thursday"
        elif date_delta.days == 2:
            day_name = "Good Friday"
        elif date_delta.days == 1:
            day_name = "Holy Saturday"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.FIXED,
            )
        )

    def __check_easter_week(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.easter_day
        if date_delta.days == 1:
            day_name = "Monday in Easter Week"
        elif date_delta.days == 2:
            day_name = "Tuesday in Easter Week"
        elif date_delta.days == 3:
            day_name = "Wednesday in Easter Week"
        elif date_delta.days == 4:
            day_name = "Thursday in Easter Week"
        elif date_delta.days == 5:
            day_name = "Friday in Easter Week"
        elif date_delta.days == 6:
            day_name = "Saturday in Easter Week"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.FIXED,
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
        if date_delta.days == 0:
            day_name = "First Sunday of Advent"
        elif date_delta.days == 7:
            day_name = "Second Sunday of Advent"
        elif date_delta.days == 14:
            day_name = "Third Sunday of Advent"
        elif date_delta.days == 21:
            day_name = "Fourth Sunday of Advent"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.SUNDAY,
            )
        )

    def __check_christmas_sundays(self, holy_days: list[HolyDay]) -> None:
        christmas_day = date(self.date.year, 12, 25)
        if christmas_day < self.date <= christmas_day + timedelta(days=7):
            day_name = "First Sunday after Christmas"
        else:
            day_name = "Second Sunday after Christmas"

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.SUNDAY,
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
            day_name = "Second to Last Sunday after Epiphany"
        elif self.date == self.easter_day - timedelta(days=49):
            day_name = "Last Sunday after Epiphany"
        elif date_delta.days == 0:
            day_name = "First Sunday after Epiphany"
        elif date_delta.days == 7:
            day_name = "Second Sunday after Epiphany"
        elif date_delta.days == 14:
            day_name = "Third Sunday after Epiphany"
        elif date_delta.days == 21:
            day_name = "Fourth Sunday after Epiphany"
        elif date_delta.days == 28:
            day_name = "Fifth Sunday after Epiphany"
        elif date_delta.days == 35:
            day_name = "Sixth Sunday after Epiphany"
        elif date_delta.days == 42:
            day_name = "Seventh Sunday after Epiphany"
        elif date_delta.days == 49:
            day_name = "Eighth Sunday after Epiphany"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.SUNDAY,
            )
        )

    def __check_lent_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.easter_day - self.date
        if date_delta.days == 42:
            day_name = "First Sunday in Lent"
        elif date_delta.days == 35:
            day_name = "Second Sunday in Lent"
        elif date_delta.days == 28:
            day_name = "Third Sunday in Lent"
        elif date_delta.days == 21:
            day_name = "Fourth Sunday in Lent"
        elif date_delta.days == 14:
            day_name = "Fifth Sunday in Lent"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.SUNDAY,
            )
        )

    def __check_easter_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.easter_day
        if date_delta.days == 7:
            day_name = "Second Sunday of Easter"
        elif date_delta.days == 14:
            day_name = "Third Sunday of Easter"
        elif date_delta.days == 21:
            day_name = "Fourth Sunday of Easter"
        elif date_delta.days == 28:
            day_name = "Fifth Sunday of Easter"
        elif date_delta.days == 35:
            day_name = "Sixth Sunday of Easter"
        elif date_delta.days == 42:
            day_name = "Sunday after Ascension Day"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.SUNDAY,
            )
        )

    def __check_pentecost_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.moveable_dates["advent_sunday"] - self.date
        if date_delta.days == 203:
            day_name = "Proper 1"
        elif date_delta.days == 196:
            day_name = "Proper 2"
        elif date_delta.days == 189:
            day_name = "Proper 3"
        elif date_delta.days == 182:
            day_name = "Proper 4"
        elif date_delta.days == 175:
            day_name = "Proper 5"
        elif date_delta.days == 168:
            day_name = "Proper 6"
        elif date_delta.days == 161:
            day_name = "Proper 7"
        elif date_delta.days == 154:
            day_name = "Proper 8"
        elif date_delta.days == 147:
            day_name = "Proper 9"
        elif date_delta.days == 140:
            day_name = "Proper 10"
        elif date_delta.days == 133:
            day_name = "Proper 11"
        elif date_delta.days == 126:
            day_name = "Proper 12"
        elif date_delta.days == 119:
            day_name = "Proper 13"
        elif date_delta.days == 112:
            day_name = "Proper 14"
        elif date_delta.days == 105:
            day_name = "Proper 15"
        elif date_delta.days == 98:
            day_name = "Proper 16"
        elif date_delta.days == 91:
            day_name = "Proper 17"
        elif date_delta.days == 84:
            day_name = "Proper 18"
        elif date_delta.days == 77:
            day_name = "Proper 19"
        elif date_delta.days == 70:
            day_name = "Proper 20"
        elif date_delta.days == 63:
            day_name = "Proper 21"
        elif date_delta.days == 56:
            day_name = "Proper 22"
        elif date_delta.days == 49:
            day_name = "Proper 23"
        elif date_delta.days == 42:
            day_name = "Proper 24"
        elif date_delta.days == 35:
            day_name = "Proper 25"
        elif date_delta.days == 28:
            day_name = "Proper 26"
        elif date_delta.days == 21:
            day_name = "Proper 27"
        elif date_delta.days == 14:
            day_name = "Proper 28"
        elif date_delta.days == 7:
            day_name = "Proper 29"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.SUNDAY,
            )
        )

    def __check_red_letter_days(self, holy_days: list[HolyDay]) -> None:
        if self.date == date(self.date.year, 11, 30):
            day_name = "Saint Andrew"
        elif self.date == date(self.date.year, 12, 21):
            day_name = "Saint Thomas"
        elif self.date == date(self.date.year, 12, 26):
            day_name = "Saint Stephen"
        elif self.date == date(self.date.year, 12, 27):
            day_name = "Saint John"
        elif self.date == date(self.date.year, 12, 28):
            day_name = "Holy Innocents"
        elif self.date == date(self.date.year, 1, 1):
            day_name = "Holy Name"
        elif self.date == date(self.date.year, 1, 18):
            day_name = "Confession of Saint Peter"
        elif self.date == date(self.date.year, 1, 25):
            day_name = "Conversion of Saint Paul"
        elif self.date == date(self.date.year, 2, 2):
            day_name = "The Presentation"
        elif self.date == date(self.date.year, 2, 24):
            day_name = "Saint Matthias"
        elif self.date == date(self.date.year, 3, 19):
            day_name = "Saint Joseph"
        elif self.date == date(self.date.year, 3, 25):
            day_name = "The Annunciation"
        elif self.date == date(self.date.year, 4, 25):
            day_name = "Saint Mark"
        elif self.date == date(self.date.year, 5, 1):
            day_name = "Saint Philip and Saint James"
        elif self.date == date(self.date.year, 5, 31):
            day_name = "The Visitation"
        elif self.date == date(self.date.year, 6, 11):
            day_name = "Saint Barnabas"
        elif self.date == date(self.date.year, 6, 24):
            day_name = "Nativity of Saint John the Baptist"
        elif self.date == date(self.date.year, 6, 29):
            day_name = "Saint Peter and Saint Paul"
        elif self.date == date(self.date.year, 7, 22):
            day_name = "Saint Mary Magdalene"
        elif self.date == date(self.date.year, 7, 25):
            day_name = "Saint James"
        elif self.date == date(self.date.year, 8, 6):
            day_name = "The Transfiguration"
        elif self.date == date(self.date.year, 8, 15):
            day_name = "Saint Mary the Virgin"
        elif self.date == date(self.date.year, 8, 24):
            day_name = "Saint Bartholomew"
        elif self.date == date(self.date.year, 9, 14):
            day_name = "Holy Cross Day"
        elif self.date == date(self.date.year, 9, 21):
            day_name = "Saint Matthew"
        elif self.date == date(self.date.year, 9, 29):
            day_name = "Saint Michael and All Angels"
        elif self.date == date(self.date.year, 10, 18):
            day_name = "Saint Luke"
        elif self.date == date(self.date.year, 10, 23):
            day_name = "Saint James of Jerusalem"
        elif self.date == date(self.date.year, 10, 28):
            day_name = "Saint Simon and Saint Jude"
        else:
            return

        holy_days.append(
            HolyDay(
                day_name,
                self.liturgical_year,
                self.liturgical_season,
                Rank.MAJOR,
            )
        )
