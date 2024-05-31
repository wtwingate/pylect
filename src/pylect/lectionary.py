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
        self.holy_days = []
        self.__get_holy_days()

    def __get_easter_day(self) -> date:
        return easter(self.date.year)

    def __get_moveable_dates(self) -> dict[str : date | int]:
        return {
            "easter_day": self.easter_day,
            "sundays_after_epiphany": self.__get_sundays_after_epiphany(),
            "ash_wednesday": self.__get_ash_wednesday(),
            "ascension_day": self.__get_ascension_day(),
            "pentecost": self.__get_pentecost(),
            "proper_after_trinity": self.__get_proper_after_trinity(),
            "advent_sunday": self.__get_advent_sunday(),
        }

    def __get_sundays_after_epiphany(self) -> int:
        first_sunday = date(self.date.year, 1, 6) + relativedelta(
            days=+1, weekday=SU(+1)
        )
        last_sunday = self.easter_day - timedelta(days=42)
        return (last_sunday - first_sunday).days // 7

    def __get_ash_wednesday(self) -> date:
        return self.easter_day - timedelta(days=46)

    def __get_ascension_day(self) -> date:
        return self.easter_day + timedelta(days=39)

    def __get_pentecost(self) -> date:
        return self.easter_day + timedelta(days=49)

    def __get_proper_after_trinity(self) -> int:
        first_sunday = self.easter_day + timedelta(days=63)
        last_sunday = date(self.date.year, 12, 25) + relativedelta(
            days=-1, weekday=SU(-5)
        )
        sundays_after_trinity = (last_sunday - first_sunday).days // 7
        return 29 - sundays_after_trinity

    def __get_advent_sunday(self) -> date:
        return date(self.date.year, 12, 25) + relativedelta(days=-1, weekday=SU(-4))

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

    def __get_holy_days(self) -> None:
        self.__check_major_days()
        self.__check_holy_week()
        self.__check_easter_week()
        self.__check_sundays()
        self.__check_red_letter_days()

    def __check_major_days(self) -> None:
        if self.date == self.easter_day:
            self.holy_days.append(HolyDay("Easter Day", 3))
        elif self.date == self.moveable_dates["ascension_day"]:
            self.holy_days.append(HolyDay("Ascension Day", 3))
        elif self.date == self.moveable_dates["pentecost"]:
            self.holy_days.append(HolyDay("The Day of Pentecost", 3))
        elif self.date == self.easter_day + timedelta(days=56):
            self.holy_days.append(HolyDay("Trinity Sunday", 3))
        elif self.date == date(self.date.year, 12, 25):
            self.holy_days.append(HolyDay("Christmas Day", 3))
        elif self.date == date(self.date.year, 1, 6):
            self.holy_days.append(HolyDay("The Epiphany", 3))
        elif self.date == date(self.date.year, 11, 1):
            self.holy_days.append(HolyDay("All Saints' Day", 3))
        elif self.date == self.moveable_dates["ash_wednesday"]:
            self.holy_days.append(HolyDay("Ash Wednesday", 3))

    def __check_holy_week(self) -> None:
        date_delta = self.easter_day - self.date

        if date_delta.days == 7:
            self.holy_days.append(HolyDay("Palm Sunday", 3))
        elif date_delta.days == 6:
            self.holy_days.append(HolyDay("Monday in Holy Week", 3))
        elif date_delta.days == 5:
            self.holy_days.append(HolyDay("Tuesday in Holy Week", 3))
        elif date_delta.days == 4:
            self.holy_days.append(HolyDay("Wednesday in Holy Week", 3))
        elif date_delta.days == 3:
            self.holy_days.append(HolyDay("Maundy Thursday", 3))
        elif date_delta.days == 2:
            self.holy_days.append(HolyDay("Good Friday", 3))
        elif date_delta.days == 1:
            self.holy_days.append(HolyDay("Holy Saturday", 3))

    def __check_easter_week(self) -> None:
        date_delta = self.date - self.easter_day

        if date_delta.days == 1:
            self.holy_days.append(HolyDay("Monday of Easter Week", 3))
        elif date_delta.days == 2:
            self.holy_days.append(HolyDay("Tuesday of Easter Week", 3))
        elif date_delta.days == 3:
            self.holy_days.append(HolyDay("Wednesday of Easter Week", 3))
        elif date_delta.days == 4:
            self.holy_days.append(HolyDay("Thursday of Easter Week", 3))
        elif date_delta.days == 5:
            self.holy_days.append(HolyDay("Friday of Easter Week", 3))
        elif date_delta.days == 6:
            self.holy_days.append(HolyDay("Saturday of Easter Week", 3))

    def __check_sundays(self) -> None:
        if self.date.weekday() != 6:
            return

        if self.liturgical_season == "Advent":
            self.__check_advent_sundays()
        elif self.liturgical_season == "Christmas":
            self.__check_christmas_sundays()
        elif self.liturgical_season == "Epiphany":
            self.__check_epiphany_sundays()
        elif self.liturgical_season == "Lent":
            self.__check_lent_sundays()
        elif self.liturgical_season == "Easter":
            self.__check_easter_sundays()
        elif self.liturgical_season == "Pentecost":
            self.__check_pentecost_sundays()

    def __check_advent_sundays(self) -> None:
        date_delta = self.date - self.moveable_dates["advent_sunday"]

        if date_delta.days == 0:
            self.holy_days.append(HolyDay("The First Sunday in Advent", 2))
        elif date_delta.days == 7:
            self.holy_days.append(HolyDay("The Second Sunday in Advent", 2))
        elif date_delta.days == 14:
            self.holy_days.append(HolyDay("The Third Sunday in Advent", 2))
        elif date_delta.days == 21:
            self.holy_days.append(HolyDay("The Fourth Sunday in Advent", 2))

    def __check_christmas_sundays(self) -> None:
        if date(self.date.year, 12, 25) < self.date <= date(self.date.year + 1, 1, 1):
            self.holy_days.append(HolyDay("The First Sunday of Christmas", 1))
        else:
            self.holy_days.append(HolyDay("The Second Sunday of Christmas", 1))

    def __check_epiphany_sundays(self) -> None:
        first_sunday_of_epiphany = date(self.date.year, 1, 6) + relativedelta(
            days=+1, weekday=SU(+1)
        )
        date_delta = self.date - first_sunday_of_epiphany

        # The number of Sundays after Epiphany can range from 4 to 9.
        # To account for this, check for the final two Sundays first.
        if self.date == self.easter_day - timedelta(days=56):
            self.holy_days.append(
                HolyDay("The Second to Last Sunday of Epiphany: World Mission", 1)
            )
        elif self.date == self.easter_day - timedelta(days=49):
            self.holy_days.append(
                HolyDay("The Last Sunday of Epiphany: Transfiguration", 1)
            )

        # Then begin checking Sundays from the start of Epiphany
        elif date_delta.days == 0:
            self.holy_days.append(
                HolyDay("The First Sunday of Epiphany: Baptism of Our Lord", 1)
            )
        elif date_delta.days == 7:
            self.holy_days.append(HolyDay("The Second Sunday of Epiphany", 1))
        elif date_delta.days == 14:
            self.holy_days.append(HolyDay("The Third Sunday of Epiphany", 1))
        elif date_delta.days == 21:
            self.holy_days.append(HolyDay("The Fourth Sunday of Epiphany", 1))
        elif date_delta.days == 28:
            self.holy_days.append(HolyDay("The Fifth Sunday of Epiphany", 1))
        elif date_delta.days == 35:
            self.holy_days.append(HolyDay("The Sixth Sunday of Epiphany", 1))
        elif date_delta.days == 42:
            self.holy_days.append(HolyDay("The Seventh Sunday of Epiphany", 1))
        elif date_delta.days == 49:
            self.holy_days.append(HolyDay("The Eighth Sunday of Epiphany", 1))

    def __check_lent_sundays(self) -> None:
        date_delta = self.easter_day - self.date

        if date_delta.days == 42:
            self.holy_days.append(HolyDay("The First Sunday in Lent", 2))
        elif date_delta.days == 35:
            self.holy_days.append(HolyDay("The Second Sunday in Lent", 2))
        elif date_delta.days == 28:
            self.holy_days.append(HolyDay("The Third Sunday in Lent", 2))
        elif date_delta.days == 21:
            self.holy_days.append(HolyDay("The Fourth Sunday in Lent", 2))
        elif date_delta.days == 14:
            self.holy_days.append(
                HolyDay("The Fifth Sunday in Lent: Passion Sunday", 2)
            )

    def __check_easter_sundays(self) -> None:
        date_delta = self.date - self.easter_day

        if date_delta.days == 7:
            self.holy_days.append(HolyDay("The Second Sunday of Easter", 2))
        elif date_delta.days == 14:
            self.holy_days.append(HolyDay("The Third Sunday of Easter", 2))
        elif date_delta.days == 21:
            self.holy_days.append(
                HolyDay("The Fourth Sunday of Easter: Good Shepherd", 2)
            )
        elif date_delta.days == 28:
            self.holy_days.append(HolyDay("The Fifth Sunday of Easter", 2))
        elif date_delta.days == 35:
            self.holy_days.append(
                HolyDay("The Sixth Sunday of Easter: Rogation Sunday", 2)
            )
        elif date_delta.days == 42:
            self.holy_days.append(HolyDay("The Sunday after Ascension Day", 2))

    def __check_pentecost_sundays(self) -> None:
        date_delta = self.moveable_dates["advent_sunday"] - self.date

        if date_delta.days == 203:
            self.holy_days.append(HolyDay("Proper 1", 1))
        elif date_delta.days == 196:
            self.holy_days.append(HolyDay("Proper 2", 1))
        elif date_delta.days == 189:
            self.holy_days.append(HolyDay("Proper 3", 1))
        elif date_delta.days == 182:
            self.holy_days.append(HolyDay("Proper 4", 1))
        elif date_delta.days == 175:
            self.holy_days.append(HolyDay("Proper 5", 1))
        elif date_delta.days == 168:
            self.holy_days.append(HolyDay("Proper 6", 1))
        elif date_delta.days == 161:
            self.holy_days.append(HolyDay("Proper 7", 1))
        elif date_delta.days == 154:
            self.holy_days.append(HolyDay("Proper 8", 1))
        elif date_delta.days == 147:
            self.holy_days.append(HolyDay("Proper 9", 1))
        elif date_delta.days == 140:
            self.holy_days.append(HolyDay("Proper 10", 1))
        elif date_delta.days == 133:
            self.holy_days.append(HolyDay("Proper 11", 1))
        elif date_delta.days == 126:
            self.holy_days.append(HolyDay("Proper 12", 1))
        elif date_delta.days == 119:
            self.holy_days.append(HolyDay("Proper 13", 1))
        elif date_delta.days == 112:
            self.holy_days.append(HolyDay("Proper 14", 1))
        elif date_delta.days == 105:
            self.holy_days.append(HolyDay("Proper 15", 1))
        elif date_delta.days == 98:
            self.holy_days.append(HolyDay("Proper 16", 1))
        elif date_delta.days == 91:
            self.holy_days.append(HolyDay("Proper 17", 1))
        elif date_delta.days == 84:
            self.holy_days.append(HolyDay("Proper 18", 1))
        elif date_delta.days == 77:
            self.holy_days.append(HolyDay("Proper 19", 1))
        elif date_delta.days == 70:
            self.holy_days.append(HolyDay("Proper 20", 1))
        elif date_delta.days == 63:
            self.holy_days.append(HolyDay("Proper 21", 1))
        elif date_delta.days == 56:
            self.holy_days.append(HolyDay("Proper 22", 1))
        elif date_delta.days == 49:
            self.holy_days.append(HolyDay("Proper 23", 1))
        elif date_delta.days == 42:
            self.holy_days.append(HolyDay("Proper 24", 1))
        elif date_delta.days == 35:
            self.holy_days.append(HolyDay("Proper 25", 1))
        elif date_delta.days == 28:
            self.holy_days.append(HolyDay("Proper 26", 1))
        elif date_delta.days == 21:
            self.holy_days.append(HolyDay("Proper 27", 1))
        elif date_delta.days == 14:
            self.holy_days.append(HolyDay("Proper 28", 1))
        elif date_delta.days == 7:
            self.holy_days.append(HolyDay("Proper 29: Christ the King", 1))

    def __check_red_letter_days(self) -> None:
        if self.date == date(self.date.year, 1, 1):
            self.holy_days.append(
                HolyDay("The Circumcision and Holy Name of Our Lord Jesus Christ", 1)
            )
        elif self.date == date(self.date.year, 1, 18):
            self.holy_days.append(HolyDay("Confession of Peter the Apostle", 1))
        elif self.date == date(self.date.year, 1, 25):
            self.holy_days.append(HolyDay("Conversion of Paul the Apostle", 1))
        elif self.date == date(self.date.year, 2, 2):
            self.holy_days.append(
                HolyDay("The Presentation of Our Lord Jesus Christ in the Temple", 1)
            )
        elif self.date == date(self.date.year, 2, 24):
            self.holy_days.append(HolyDay("Matthias the Apostle", 1))
        elif self.date == date(self.date.year, 3, 19):
            self.holy_days.append(
                HolyDay("Joseph, Husband of the Virgin Mary and Guardian of Jesus", 1)
            )
        elif self.date == date(self.date.year, 3, 25):
            self.holy_days.append(
                HolyDay(
                    "The Annunciation of our Lord Jesus Christ to the Virgin Mary", 1
                )
            )
        elif self.date == date(self.date.year, 4, 25):
            self.holy_days.append(HolyDay("Mark the Evangelist", 1))
        elif self.date == date(self.date.year, 5, 1):
            self.holy_days.append(HolyDay("Philip and James, Apostles", 1))
        elif self.date == date(self.date.year, 5, 31):
            self.holy_days.append(
                HolyDay(
                    "The Visitation of the Virgin Mary to Elizabeth and Zechariah", 1
                )
            )
        elif self.date == date(self.date.year, 6, 11):
            self.holy_days.append(HolyDay("Barnabas the Apostle", 1))
        elif self.date == date(self.date.year, 6, 24):
            self.holy_days.append(HolyDay("The Nativity of John the Baptist", 1))
        elif self.date == date(self.date.year, 6, 29):
            self.holy_days.append(HolyDay("Peter and Paul, Apostles", 1))
        elif self.date == date(self.date.year, 7, 22):
            self.holy_days.append(HolyDay("Mary Magdalene", 1))
        elif self.date == date(self.date.year, 7, 25):
            self.holy_days.append(HolyDay("James the Elder, Apostle", 1))
        elif self.date == date(self.date.year, 8, 6):
            self.holy_days.append(
                HolyDay("The Transfiguration of Our Lord Jesus Christ", 1)
            )
        elif self.date == date(self.date.year, 8, 15):
            self.holy_days.append(
                HolyDay("The Virgin Mary, Mother of Our Lord Jesus Christ", 1)
            )
        elif self.date == date(self.date.year, 8, 24):
            self.holy_days.append(HolyDay("Bartholomew the Apostle", 1))
        elif self.date == date(self.date.year, 9, 14):
            self.holy_days.append(HolyDay("Holy Cross Day", 1))
        elif self.date == date(self.date.year, 9, 21):
            self.holy_days.append(HolyDay("Matthew, Apostle and Evangelist", 1))
        elif self.date == date(self.date.year, 9, 29):
            self.holy_days.append(HolyDay("Holy Michael and All Angels", 1))
        elif self.date == date(self.date.year, 10, 18):
            self.holy_days.append(
                HolyDay("Luke the Evangelist and Companion of Paul", 1)
            )
        elif self.date == date(self.date.year, 10, 23):
            self.holy_days.append(
                HolyDay("James of Jerusalem, Bishop and Martyr, Brother of Our Lord", 1)
            )
        elif self.date == date(self.date.year, 10, 28):
            self.holy_days.append(HolyDay("Simon and Jude, Apostles", 1))
        elif self.date == date(self.date.year, 11, 30):
            self.holy_days.append(HolyDay("Andrew the Apostle", 1))
        elif self.date == date(self.date.year, 12, 21):
            self.holy_days.append(HolyDay("Thomas the Apostle", 1))
        elif self.date == date(self.date.year, 12, 26):
            self.holy_days.append(HolyDay("Stephen, Deacon and Martyr", 1))
        elif self.date == date(self.date.year, 12, 27):
            self.holy_days.append(HolyDay("John, Apostle and Evangelist", 1))
        elif self.date == date(self.date.year, 12, 28):
            self.holy_days.append(HolyDay("The Holy Innocents", 1))


if __name__ == "__main__":
    for i in range(365):
        day = date(2024, 1, 1) + timedelta(days=i)
        lectionary = Lectionary(day)
        for holy_day in lectionary.holy_days:
            print(day, holy_day.name)
