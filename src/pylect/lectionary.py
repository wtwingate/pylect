from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, SU
from dateutil.easter import easter
from pylect.holyday import HolyDay


class Lectionary:
    """The lectionary class provides methods for calculating holy days according
    to the liturgical calendar of the Anglican Church.
    """

    def __init__(self, today: date) -> None:
        self.date = today
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

        if date_delta.days == 7:
            holy_days.append(
                HolyDay(
                    "Palm Sunday",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 6:
            holy_days.append(
                HolyDay(
                    "Monday in Holy Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 5:
            holy_days.append(
                HolyDay(
                    "Tuesday in Holy Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 4:
            holy_days.append(
                HolyDay(
                    "Wednesday in Holy Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 3:
            holy_days.append(
                HolyDay(
                    "Maundy Thursday",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 2:
            holy_days.append(
                HolyDay(
                    "Good Friday",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 1:
            holy_days.append(
                HolyDay(
                    "Holy Saturday",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )

    def __check_easter_week(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.easter_day

        if date_delta.days == 1:
            holy_days.append(
                HolyDay(
                    "Monday of Easter Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 2:
            holy_days.append(
                HolyDay(
                    "Tuesday of Easter Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 3:
            holy_days.append(
                HolyDay(
                    "Wednesday of Easter Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 4:
            holy_days.append(
                HolyDay(
                    "Thursday of Easter Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 5:
            holy_days.append(
                HolyDay(
                    "Friday of Easter Week",
                    self.liturgical_year,
                    self.liturgical_season,
                    3,
                )
            )
        elif date_delta.days == 6:
            holy_days.append(
                HolyDay(
                    "Saturday of Easter Week",
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

        if date_delta.days == 0:
            holy_days.append(
                HolyDay(
                    "The First Sunday in Advent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 7:
            holy_days.append(
                HolyDay(
                    "The Second Sunday in Advent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 14:
            holy_days.append(
                HolyDay(
                    "The Third Sunday in Advent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 21:
            holy_days.append(
                HolyDay(
                    "The Fourth Sunday in Advent",
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

        # Then begin checking Sundays from the start of Epiphany
        elif date_delta.days == 0:
            holy_days.append(
                HolyDay(
                    "The First Sunday of Epiphany: Baptism of Our Lord",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 7:
            holy_days.append(
                HolyDay(
                    "The Second Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 14:
            holy_days.append(
                HolyDay(
                    "The Third Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 21:
            holy_days.append(
                HolyDay(
                    "The Fourth Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 28:
            holy_days.append(
                HolyDay(
                    "The Fifth Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 35:
            holy_days.append(
                HolyDay(
                    "The Sixth Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 42:
            holy_days.append(
                HolyDay(
                    "The Seventh Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 49:
            holy_days.append(
                HolyDay(
                    "The Eighth Sunday of Epiphany",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )

    def __check_lent_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.easter_day - self.date

        if date_delta.days == 42:
            holy_days.append(
                HolyDay(
                    "The First Sunday in Lent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 35:
            holy_days.append(
                HolyDay(
                    "The Second Sunday in Lent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 28:
            holy_days.append(
                HolyDay(
                    "The Third Sunday in Lent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 21:
            holy_days.append(
                HolyDay(
                    "The Fourth Sunday in Lent",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 14:
            holy_days.append(
                HolyDay(
                    "The Fifth Sunday in Lent: Passion Sunday",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )

    def __check_easter_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.date - self.easter_day

        if date_delta.days == 7:
            holy_days.append(
                HolyDay(
                    "The Second Sunday of Easter",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 14:
            holy_days.append(
                HolyDay(
                    "The Third Sunday of Easter",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 21:
            holy_days.append(
                HolyDay(
                    "The Fourth Sunday of Easter: Good Shepherd",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 28:
            holy_days.append(
                HolyDay(
                    "The Fifth Sunday of Easter",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 35:
            holy_days.append(
                HolyDay(
                    "The Sixth Sunday of Easter: Rogation Sunday",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )
        elif date_delta.days == 42:
            holy_days.append(
                HolyDay(
                    "The Sunday after Ascension Day",
                    self.liturgical_year,
                    self.liturgical_season,
                    2,
                )
            )

    def __check_pentecost_sundays(self, holy_days: list[HolyDay]) -> None:
        date_delta = self.moveable_dates["advent_sunday"] - self.date

        if date_delta.days == 203:
            holy_days.append(
                HolyDay(
                    "Proper 1",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 196:
            holy_days.append(
                HolyDay(
                    "Proper 2",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 189:
            holy_days.append(
                HolyDay(
                    "Proper 3",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 182:
            holy_days.append(
                HolyDay(
                    "Proper 4",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 175:
            holy_days.append(
                HolyDay(
                    "Proper 5",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 168:
            holy_days.append(
                HolyDay(
                    "Proper 6",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 161:
            holy_days.append(
                HolyDay(
                    "Proper 7",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 154:
            holy_days.append(
                HolyDay(
                    "Proper 8",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 147:
            holy_days.append(
                HolyDay(
                    "Proper 9",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 140:
            holy_days.append(
                HolyDay(
                    "Proper 10",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 133:
            holy_days.append(
                HolyDay(
                    "Proper 11",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 126:
            holy_days.append(
                HolyDay(
                    "Proper 12",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 119:
            holy_days.append(
                HolyDay(
                    "Proper 13",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 112:
            holy_days.append(
                HolyDay(
                    "Proper 14",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 105:
            holy_days.append(
                HolyDay(
                    "Proper 15",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 98:
            holy_days.append(
                HolyDay(
                    "Proper 16",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 91:
            holy_days.append(
                HolyDay(
                    "Proper 17",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 84:
            holy_days.append(
                HolyDay(
                    "Proper 18",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 77:
            holy_days.append(
                HolyDay(
                    "Proper 19",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 70:
            holy_days.append(
                HolyDay(
                    "Proper 20",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 63:
            holy_days.append(
                HolyDay(
                    "Proper 21",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 56:
            holy_days.append(
                HolyDay(
                    "Proper 22",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 49:
            holy_days.append(
                HolyDay(
                    "Proper 23",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 42:
            holy_days.append(
                HolyDay(
                    "Proper 24",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 35:
            holy_days.append(
                HolyDay(
                    "Proper 25",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 28:
            holy_days.append(
                HolyDay(
                    "Proper 26",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 21:
            holy_days.append(
                HolyDay(
                    "Proper 27",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 14:
            holy_days.append(
                HolyDay(
                    "Proper 28",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif date_delta.days == 7:
            holy_days.append(
                HolyDay(
                    "Proper 29: Christ the King",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )

    def __check_red_letter_days(self, holy_days: list[HolyDay]) -> None:
        if self.date == date(self.date.year, 1, 1):
            holy_days.append(
                HolyDay(
                    "The Circumcision and Holy Name of Our Lord Jesus Christ",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 1, 18):
            holy_days.append(
                HolyDay(
                    "Confession of Peter the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 1, 25):
            holy_days.append(
                HolyDay(
                    "Conversion of Paul the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 2, 2):
            holy_days.append(
                HolyDay(
                    "The Presentation of Our Lord Jesus Christ in the Temple",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 2, 24):
            holy_days.append(
                HolyDay(
                    "Matthias the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 3, 19):
            holy_days.append(
                HolyDay(
                    "Joseph, Husband of the Virgin Mary and Guardian of Jesus",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 3, 25):
            holy_days.append(
                HolyDay(
                    "The Annunciation of our Lord Jesus Christ to the Virgin Mary",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 4, 25):
            holy_days.append(
                HolyDay(
                    "Mark the Evangelist",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 5, 1):
            holy_days.append(
                HolyDay(
                    "Philip and James, Apostles",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 5, 31):
            holy_days.append(
                HolyDay(
                    "The Visitation of the Virgin Mary to Elizabeth and Zechariah",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 6, 11):
            holy_days.append(
                HolyDay(
                    "Barnabas the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 6, 24):
            holy_days.append(
                HolyDay(
                    "The Nativity of John the Baptist",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 6, 29):
            holy_days.append(
                HolyDay(
                    "Peter and Paul, Apostles",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 7, 22):
            holy_days.append(
                HolyDay(
                    "Mary Magdalene",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 7, 25):
            holy_days.append(
                HolyDay(
                    "James the Elder, Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 8, 6):
            holy_days.append(
                HolyDay(
                    "The Transfiguration of Our Lord Jesus Christ",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 8, 15):
            holy_days.append(
                HolyDay(
                    "The Virgin Mary, Mother of Our Lord Jesus Christ",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 8, 24):
            holy_days.append(
                HolyDay(
                    "Bartholomew the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 9, 14):
            holy_days.append(
                HolyDay(
                    "Holy Cross Day",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 9, 21):
            holy_days.append(
                HolyDay(
                    "Matthew, Apostle and Evangelist",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 9, 29):
            holy_days.append(
                HolyDay(
                    "Holy Michael and All Angels",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 10, 18):
            holy_days.append(
                HolyDay(
                    "Luke the Evangelist and Companion of Paul",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 10, 23):
            holy_days.append(
                HolyDay(
                    "James of Jerusalem, Bishop and Martyr, Brother of Our Lord",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 10, 28):
            holy_days.append(
                HolyDay(
                    "Simon and Jude, Apostles",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 11, 30):
            holy_days.append(
                HolyDay(
                    "Andrew the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 12, 21):
            holy_days.append(
                HolyDay(
                    "Thomas the Apostle",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 12, 26):
            holy_days.append(
                HolyDay(
                    "Stephen, Deacon and Martyr",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 12, 27):
            holy_days.append(
                HolyDay(
                    "John, Apostle and Evangelist",
                    self.liturgical_year,
                    self.liturgical_season,
                    1,
                )
            )
        elif self.date == date(self.date.year, 12, 28):
            holy_days.append(
                HolyDay(
                    "The Holy Innocents",
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
