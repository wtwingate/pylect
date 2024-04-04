from __future__ import annotations
import csv
import datetime as dt
import dateutil


class Lectionary:
    def __init__(self) -> None:
        self.__lectionary = self.__import_lectionary()

    def get_holy_days(self, dates: list[dt.date]) -> list:
        """Return a list of HolyDay objects

        This is the public interface for the Lectionary class. The caller
        passes in a list of date objects and receives back a list of HolyDay
        objects, which contain the date, season, name, and lessons for any
        Sunday or Holy Day that falls on the given dates."""
        holy_days = []
        for date in dates:
            anchors = self.__get_anchors(date)
            year = self.__get_years(date, anchors)
            season = self.__get_seasons(date, anchors)
            name = (
                self.__get_principal_feasts(date, anchors)
                or self.__get_ash_wednesday(date, anchors)
                or self.__get_holy_week(date, anchors)
                or self.__get_easter_week(date, anchors)
                or self.__get_sundays(date, anchors, season)
                or self.__get_red_letter_days(date)
            )
            if name is not None:
                lessons = self.__get_lessons(name, year)
                holy_days.append(HolyDay(date, year, season, name, lessons))
        return holy_days

    def __import_lectionary(self) -> None:
        """Import lectionary from CSV file."""
        lectionary = {}
        with open("src/pylect/lectionary.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lectionary[row["Day"]] = row
        return lectionary

    def __get_anchors(self, date: dt.date) -> dict:
        """Generate a dictionary of important days in the liturgical year.

        These are not necessarily the most important days theologically (with
        the obvious exceptions of Christmas and Easter), but they are the most
        important for calculating the absolute dates for all other days in the
        Christian year. Each of these days marks a transition between the six
        major seasons of the church calendar: Advent, Christmas, Epiphany, Lent,
        Easter, and Pentecost.
        """
        easter_day = dateutil.easter.easter(date.year)

        # Advent Sunday always falls on the Sunday closest to Nov 30th
        nov_30th = dt.date(date.year, 11, 30)
        if nov_30th.weekday() == 6:
            advent_sunday = nov_30th
        elif nov_30th.weekday() <= 2:
            advent_sunday = nov_30th - dt.timedelta(days=(nov_30th.weekday() + 1))
        elif nov_30th.weekday() >= 3:
            advent_sunday = nov_30th + dt.timedelta(days=(6 - nov_30th.weekday()))

        return {
            "Epiphany": dt.date(date.year, 1, 6),
            "Ash Wednesday": easter_day - dt.timedelta(days=46),
            "Easter Day": easter_day,
            "Pentecost": easter_day + dt.timedelta(days=49),
            "Advent Sunday": advent_sunday,
            "Christmas Day": dt.date(date.year, 12, 25),
        }

    def __get_years(self, date: dt.date, anchors: dict) -> str:
        """Calculate the liturgical year for any given date

        The lectionary follows a three year cycle of readings. The liturgical
        year begins on the First Sunday of Advent, which is the Sunday closest
        to November 30th. Year A starts in years that are evenly divisible by
        3 (e.g. 2019), followed by Year B and Year C.
        """
        advent_sunday = anchors["Advent Sunday"]

        if date < advent_sunday:
            remainder = (date.year - 1) % 3
        else:
            remainder = date.year % 3

        if remainder == 0:
            return "Year A"
        if remainder == 1:
            return "Year B"
        if remainder == 2:
            return "Year C"

    def __get_seasons(self, date: dt.date, anchors: dict) -> str:
        """Calculate the liturgical season for any given date"""

        if date < anchors["Epiphany"]:
            return "Christmas"
        elif date < anchors["Ash Wednesday"]:
            return "Epiphany"
        elif date < anchors["Easter Day"]:
            return "Lent"
        elif date < anchors["Pentecost"]:
            return "Easter"
        elif date < anchors["Advent Sunday"]:
            return "Pentecost"
        elif date < anchors["Christmas Day"]:
            return "Advent"
        else:
            return "Christmas"

    def __get_principal_feasts(self, date: dt.date, anchors: dict) -> str:
        easter_day = anchors["Easter Day"]

        if date == easter_day:
            return "Easter Day"
        if date == easter_day + dt.timedelta(days=39):
            return "Ascension Day"
        if date == easter_day + dt.timedelta(days=49):
            return "The Day of Pentecost"
        if date == easter_day + dt.timedelta(days=56):
            return "Trinity Sunday"
        if date == dt.date(date.year, 11, 1):
            return "All Saints' Day"
        if date == dt.date(date.year, 12, 25):
            return "The Nativity of Our Lord Jesus Christ: Christmas Day I"
        if date == dt.date(date.year, 1, 6):
            return "The Epiphany of Our Lord Jesus Christ"
        return None

    def __get_ash_wednesday(self, date: dt.date, anchors: dict) -> str:
        if date == anchors["Ash Wednesday"]:
            return "Ash Wednesday"
        return None

    def __get_holy_week(self, date: dt.date, anchors: dict) -> str:
        easter_day = anchors["Easter Day"]

        if date == easter_day - dt.timedelta(days=7):
            return "Palm Sunday"
        if date == easter_day - dt.timedelta(days=6):
            return "Monday of Holy Week"
        if date == easter_day - dt.timedelta(days=5):
            return "Tuesday of Holy Week"
        if date == easter_day - dt.timedelta(days=4):
            return "Wednesday of Holy Week"
        if date == easter_day - dt.timedelta(days=3):
            return "Maundy Thursday"
        if date == easter_day - dt.timedelta(days=2):
            return "Good Friday"
        if date == easter_day - dt.timedelta(days=1):
            return "Holy Saturday"
        return None

    def __get_easter_week(self, date: dt.date, anchors: dict) -> str:
        easter_day = anchors["Easter Day"]

        if date == easter_day:
            return "Easter Day: Principal Service"
        if date == easter_day + dt.timedelta(days=1):
            return "Monday of Easter Week"
        if date == easter_day + dt.timedelta(days=2):
            return "Tuesday of Easter Week"
        if date == easter_day + dt.timedelta(days=3):
            return "Wednesday of Easter Week"
        if date == easter_day + dt.timedelta(days=4):
            return "Thursday of Easter Week"
        if date == easter_day + dt.timedelta(days=5):
            return "Friday of Easter Week"
        if date == easter_day + dt.timedelta(days=6):
            return "Saturday of Easter Week"
        return None

    def __get_sundays(self, date: dt.date, anchors: dict, season: str) -> str:
        """Calculate the liturgical day for any given date"""
        christmas = anchors["Christmas Day"]
        epiphany = anchors["Epiphany"]
        easter_day = anchors["Easter Day"]
        advent_sunday = anchors["Advent Sunday"]

        if season == "Advent":
            if date == advent_sunday:
                return "The First Sunday in Advent"
            if date == advent_sunday + dt.timedelta(days=7):
                return "The Second Sunday in Advent"
            if date == advent_sunday + dt.timedelta(days=14):
                return "The Third Sunday in Advent"
            if date == advent_sunday + dt.timedelta(days=21):
                return "The Fourth Sunday in Advent"

        if season == "Christmas":
            # There can be either one or two Sundays after Christmas
            if date.weekday() == 6 and date - christmas <= dt.timedelta(days=7):
                return "The First Sunday of Christmas"
            if date.weekday() == 6 and date - christmas >= dt.timedelta(days=8):
                return "The Second Sunday of Christmas"

        if season == "Epiphany":
            first_sunday_of_epiphany = epiphany + dt.timedelta(
                days=(6 - epiphany.weekday())
            )
            if date == first_sunday_of_epiphany:
                return "The First Sunday of Epiphany: Baptism of Our Lord"
            if date == first_sunday_of_epiphany + dt.timedelta(days=7):
                return "The Second Sunday of Epiphany"
            # The number of Sundays after Epiphany can range from 4 to 9.
            # To account for this, check for the final two Sundays here.
            if date == easter_day - dt.timedelta(days=56):
                return "The Second to Last Sunday of Epiphany: World Mission"
            if date == easter_day - dt.timedelta(days=49):
                return "The Last Sunday of Epiphany: Transfiguration"
            # Continue checking dates from the start of Epiphany
            if date == first_sunday_of_epiphany + dt.timedelta(days=14):
                return "The Third Sunday of Epiphany"
            if date == first_sunday_of_epiphany + dt.timedelta(days=21):
                return "The Fourth Sunday of Epiphany"
            if date == first_sunday_of_epiphany + dt.timedelta(days=28):
                return "The Fifth Sunday of Epiphany"
            if date == first_sunday_of_epiphany + dt.timedelta(days=35):
                return "The Sixth Sunday of Epiphany"
            if date == first_sunday_of_epiphany + dt.timedelta(days=42):
                return "The Seventh Sunday of Epiphany"
            if date == first_sunday_of_epiphany + dt.timedelta(days=49):
                return "The Eighth Sunday of Epiphany"

        if season == "Lent":
            if date == easter_day - dt.timedelta(days=42):
                return "The First Sunday in Lent"
            if date == easter_day - dt.timedelta(days=35):
                return "The Second Sunday in Lent"
            if date == easter_day - dt.timedelta(days=28):
                return "The Third Sunday in Lent"
            if date == easter_day - dt.timedelta(days=21):
                return "The Fourth Sunday in Lent"
            if date == easter_day - dt.timedelta(days=14):
                return "The Fifth Sunday in Lent: Passion Sunday"

        if season == "Easter":
            if date == easter_day + dt.timedelta(days=7):
                return "The Second Sunday of Easter"
            if date == easter_day + dt.timedelta(days=14):
                return "The Third Sunday of Easter"
            if date == easter_day + dt.timedelta(days=21):
                return "The Fourth Sunday of Easter: Good Shepherd"
            if date == easter_day + dt.timedelta(days=28):
                return "The Fifth Sunday of Easter"
            if date == easter_day + dt.timedelta(days=35):
                return "The Sixth Sunday of Easter: Rogation Sunday"
            if date == easter_day + dt.timedelta(days=42):
                return "The Sunday after Ascension Day"

        if season == "Pentecost":
            # Like Epiphany, the number of days in the season after Pentecost
            # varies from year to year. Thankfully, we can account for this by
            # simply calculating the proper day from the end of the season.
            if date == advent_sunday - dt.timedelta(days=203):
                return "Proper 1"
            if date == advent_sunday - dt.timedelta(days=196):
                return "Proper 2"
            if date == advent_sunday - dt.timedelta(days=189):
                return "Proper 3"
            if date == advent_sunday - dt.timedelta(days=182):
                return "Proper 4"
            if date == advent_sunday - dt.timedelta(days=175):
                return "Proper 5"
            if date == advent_sunday - dt.timedelta(days=168):
                return "Proper 6"
            if date == advent_sunday - dt.timedelta(days=161):
                return "Proper 7"
            if date == advent_sunday - dt.timedelta(days=154):
                return "Proper 8"
            if date == advent_sunday - dt.timedelta(days=147):
                return "Proper 9"
            if date == advent_sunday - dt.timedelta(days=140):
                return "Proper 10"
            if date == advent_sunday - dt.timedelta(days=133):
                return "Proper 11"
            if date == advent_sunday - dt.timedelta(days=126):
                return "Proper 12"
            if date == advent_sunday - dt.timedelta(days=119):
                return "Proper 13"
            if date == advent_sunday - dt.timedelta(days=112):
                return "Proper 14"
            if date == advent_sunday - dt.timedelta(days=105):
                return "Proper 15"
            if date == advent_sunday - dt.timedelta(days=98):
                return "Proper 16"
            if date == advent_sunday - dt.timedelta(days=91):
                return "Proper 17"
            if date == advent_sunday - dt.timedelta(days=84):
                return "Proper 18"
            if date == advent_sunday - dt.timedelta(days=77):
                return "Proper 19"
            if date == advent_sunday - dt.timedelta(days=70):
                return "Proper 20"
            if date == advent_sunday - dt.timedelta(days=63):
                return "Proper 21"
            if date == advent_sunday - dt.timedelta(days=56):
                return "Proper 22"
            if date == advent_sunday - dt.timedelta(days=49):
                return "Proper 23"
            if date == advent_sunday - dt.timedelta(days=42):
                return "Proper 24"
            if date == advent_sunday - dt.timedelta(days=35):
                return "Proper 25"
            if date == advent_sunday - dt.timedelta(days=28):
                return "Proper 26"
            if date == advent_sunday - dt.timedelta(days=21):
                return "Proper 27"
            if date == advent_sunday - dt.timedelta(days=14):
                return "Proper 28"
            if date == advent_sunday - dt.timedelta(days=7):
                return "Proper 29: Christ the King"
        return None

    def __get_red_letter_days(self, date: dt.date) -> str:
        if date == dt.date(date.year, 1, 1):
            return "The Circumcision and Holy Name of Our Lord Jesus Christ"
        if date == dt.date(date.year, 1, 6):
            return "The Epiphany of Our Lord Jesus Christ"
        if date == dt.date(date.year, 1, 18):
            return "Confession of Peter the Apostle"
        if date == dt.date(date.year, 1, 25):
            return "Conversion of Paul the Apostle"
        if date == dt.date(date.year, 2, 2):
            return "The Presentation of Our Lord Jesus Christ in the Temple"
        if date == dt.date(date.year, 2, 24):
            return "Matthias the Apostle"
        if date == dt.date(date.year, 3, 19):
            return "Joseph, Husband of the Virgin Mary and Guardian of Jesus"
        if date == dt.date(date.year, 3, 25):
            return "The Annunciation of our Lord Jesus Christ to the Virgin Mary"
        if date == dt.date(date.year, 4, 25):
            return "Mark the Evangelist"
        if date == dt.date(date.year, 5, 1):
            return "Philip and James, Apostles"
        if date == dt.date(date.year, 5, 31):
            return "The Visitation of the Virgin Mary to Elizabeth and Zechariah"
        if date == dt.date(date.year, 6, 11):
            return "Barnabas the Apostle"
        if date == dt.date(date.year, 6, 24):
            return "The Nativity of John the Baptist"
        if date == dt.date(date.year, 6, 29):
            return "Peter and Paul, Apostles"
        if date == dt.date(date.year, 7, 22):
            return "Mary Magdalene"
        if date == dt.date(date.year, 7, 25):
            return "James the Elder, Apostle"
        if date == dt.date(date.year, 8, 6):
            return "The Transfiguration of Our Lord Jesus Christ"
        if date == dt.date(date.year, 8, 15):
            return "The Virgin Mary, Mother of Our Lord Jesus Christ"
        if date == dt.date(date.year, 8, 24):
            return "Bartholomew the Apostle"
        if date == dt.date(date.year, 9, 14):
            return "Holy Cross Day"
        if date == dt.date(date.year, 9, 21):
            return "Matthew, Apostle and Evangelist"
        if date == dt.date(date.year, 9, 29):
            return "Holy Michael and All Angels"
        if date == dt.date(date.year, 10, 18):
            return "Luke the Evangelist and Companion of Paul"
        if date == dt.date(date.year, 10, 23):
            return "James of Jerusalem, Bishop and Martyr, Brother of Our Lord"
        if date == dt.date(date.year, 10, 28):
            return "Simon and Jude, Apostles"
        if date == dt.date(date.year, 11, 1):
            return "All Saints' Day"
        if date == dt.date(date.year, 11, 30):
            return "Andrew the Apostle"
        if date == dt.date(date.year, 12, 21):
            return "Thomas the Apostle"
        if date == dt.date(date.year, 12, 25):
            return "The Nativity of Our Lord Jesus Christ"
        if date == dt.date(date.year, 12, 26):
            return "Stephen, Deacon and Martyr"
        if date == dt.date(date.year, 12, 27):
            return "John, Apostle and Evangelist"
        if date == dt.date(date.year, 12, 28):
            return "The Holy Innocents"
        return None

    def __get_lessons(self, name: str, year: str) -> list:
        lessons = self.__lectionary[name][year].split("|")
        return lessons


class HolyDay:
    def __init__(
        self, date: dt.date, year: str, season: str, name: str, lessons: list
    ) -> None:
        self.date = date
        self.year = year
        self.season = season
        self.name = name
        self.lessons = lessons
