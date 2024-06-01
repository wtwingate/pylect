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

    def __get_liturgical_year(self) -> Year:
        if self.date >= self.moveable_dates["advent_sunday"]:
            start_year = self.date.year
        else:
            start_year = self.date.year - 1

        if start_year % 3 == 0:
            return Year.A
        elif start_year % 3 == 1:
            return Year.B
        elif start_year % 3 == 2:
            return Year.C

    def __get_liturgical_season(self) -> str:
        if self.date < date(self.date.year, 1, 6):
            return "Christmas"
        elif self.date < self.moveable_dates["ash_wednesday"]:
            return "Epiphany"
        elif self.date < self.moveable_dates["easter_day"]:
            return "Lent"
        elif self.date < self.moveable_dates["pentecost"]:
            return "Easter"
        elif self.date < self.moveable_dates["advent_sunday"]:
            return "Pentecost"
        elif self.date < date(self.date.year, 12, 25):
            return "Advent"
        else:
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
            day_name = "The Day of Pentecost"
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
            day_name = "Monday of Easter Week"
        elif date_delta.days == 2:
            day_name = "Tuesday of Easter Week"
        elif date_delta.days == 3:
            day_name = "Wednesday of Easter Week"
        elif date_delta.days == 4:
            day_name = "Thursday of Easter Week"
        elif date_delta.days == 5:
            day_name = "Friday of Easter Week"
        elif date_delta.days == 6:
            day_name = "Saturday of Easter Week"
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
            day_name = "The First Sunday in Advent"
        elif date_delta.days == 7:
            day_name = "The Second Sunday in Advent"
        elif date_delta.days == 14:
            day_name = "The Third Sunday in Advent"
        elif date_delta.days == 21:
            day_name = "The Fourth Sunday in Advent"
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
            day_name = "The First Sunday of Christmas"
        else:
            day_name = "The Second Sunday of Christmas"

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
            day_name = "The Second to Last Sunday of Epiphany: World Mission"
        elif self.date == self.easter_day - timedelta(days=49):
            day_name = "The Last Sunday of Epiphany: Transfiguration"
        elif date_delta.days == 0:
            day_name = "The First Sunday of Epiphany: Baptism of Our Lord"
        elif date_delta.days == 7:
            day_name = "The Second Sunday of Epiphany"
        elif date_delta.days == 14:
            day_name = "The Third Sunday of Epiphany"
        elif date_delta.days == 21:
            day_name = "The Fourth Sunday of Epiphany"
        elif date_delta.days == 28:
            day_name = "The Fifth Sunday of Epiphany"
        elif date_delta.days == 35:
            day_name = "The Sixth Sunday of Epiphany"
        elif date_delta.days == 42:
            day_name = "The Seventh Sunday of Epiphany"
        elif date_delta.days == 49:
            day_name = "The Eighth Sunday of Epiphany"
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
            day_name = "The First Sunday in Lent"
        elif date_delta.days == 35:
            day_name = "The Second Sunday in Lent"
        elif date_delta.days == 28:
            day_name = "The Third Sunday in Lent"
        elif date_delta.days == 21:
            day_name = "The Fourth Sunday in Lent"
        elif date_delta.days == 14:
            day_name = "The Fifth Sunday in Lent: Passion Sunday"
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
            day_name = "The Second Sunday of Easter"
        elif date_delta.days == 14:
            day_name = "The Third Sunday of Easter"
        elif date_delta.days == 21:
            day_name = "The Fourth Sunday of Easter: Good Shepherd"
        elif date_delta.days == 28:
            day_name = "The Fifth Sunday of Easter"
        elif date_delta.days == 35:
            day_name = "The Sixth Sunday of Easter: Rogation Sunday"
        elif date_delta.days == 42:
            day_name = "The Sunday after Ascension Day"
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
            day_name = "Proper 29: Christ the King"
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
        if self.date == date(self.date.year, 1, 1):
            day_name = (
                "The Circumcision and Holy Name of Our Lord Jesus Christ"
            )
        elif self.date == date(self.date.year, 1, 18):
            day_name = "Confession of Peter the Apostle"
        elif self.date == date(self.date.year, 1, 25):
            day_name = "Conversion of Paul the Apostle"
        elif self.date == date(self.date.year, 2, 2):
            day_name = (
                "The Presentation of Our Lord Jesus Christ in the Temple"
            )
        elif self.date == date(self.date.year, 2, 24):
            day_name = "Matthias the Apostle"
        elif self.date == date(self.date.year, 3, 19):
            day_name = (
                "Joseph, Husband of the Virgin Mary and Guardian of Jesus"
            )
        elif self.date == date(self.date.year, 3, 25):
            day_name = (
                "The Annunciation of our Lord Jesus Christ to the Virgin Mary"
            )
        elif self.date == date(self.date.year, 4, 25):
            day_name = "Mark the Evangelist"
        elif self.date == date(self.date.year, 5, 1):
            day_name = "Philip and James, Apostles"
        elif self.date == date(self.date.year, 5, 31):
            day_name = (
                "The Visitation of the Virgin Mary to Elizabeth and Zechariah"
            )
        elif self.date == date(self.date.year, 6, 11):
            day_name = "Barnabas the Apostle"
        elif self.date == date(self.date.year, 6, 24):
            day_name = "The Nativity of John the Baptist"
        elif self.date == date(self.date.year, 6, 29):
            day_name = "Peter and Paul, Apostles"
        elif self.date == date(self.date.year, 7, 22):
            day_name = "Mary Magdalene"
        elif self.date == date(self.date.year, 7, 25):
            day_name = "James the Elder, Apostle"
        elif self.date == date(self.date.year, 8, 6):
            day_name = "The Transfiguration of Our Lord Jesus Christ"
        elif self.date == date(self.date.year, 8, 15):
            day_name = "The Virgin Mary, Mother of Our Lord Jesus Christ"
        elif self.date == date(self.date.year, 8, 24):
            day_name = "Bartholomew the Apostle"
        elif self.date == date(self.date.year, 9, 14):
            day_name = "Holy Cross Day"
        elif self.date == date(self.date.year, 9, 21):
            day_name = "Matthew, Apostle and Evangelist"
        elif self.date == date(self.date.year, 9, 29):
            day_name = "Holy Michael and All Angels"
        elif self.date == date(self.date.year, 10, 18):
            day_name = "Luke the Evangelist and Companion of Paul"
        elif self.date == date(self.date.year, 10, 23):
            day_name = (
                "James of Jerusalem, Bishop and Martyr, Brother of Our Lord"
            )
        elif self.date == date(self.date.year, 10, 28):
            day_name = "Simon and Jude, Apostles"
        elif self.date == date(self.date.year, 11, 30):
            day_name = "Andrew the Apostle"
        elif self.date == date(self.date.year, 12, 21):
            day_name = "Thomas the Apostle"
        elif self.date == date(self.date.year, 12, 26):
            day_name = "Stephen, Deacon and Martyr"
        elif self.date == date(self.date.year, 12, 27):
            day_name = "John, Apostle and Evangelist"
        elif self.date == date(self.date.year, 12, 28):
            day_name = "The Holy Innocents"
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


if __name__ == "__main__":
    for i in range(365):
        day = date.today() + timedelta(days=i)
        lectionary = Lectionary(day)
        for holy_day in lectionary.holy_days:
            print(day, holy_day.name)
