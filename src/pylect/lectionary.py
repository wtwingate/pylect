from __future__ import annotations
import csv
import datetime as dt
import dateutil


class Lectionary:
    """Import the BCP lectionary and provide methods for looking up days and lessons"""

    def __init__(self) -> None:
        self.__lectionary = self.__import_lectionary()

    def get_holy_days(self, dates: list[dt.date]) -> list:
        """Return a list of holy days as dictionaries

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
                holy_days.append(
                    {
                        "date": date,
                        "year": year,
                        "season": season,
                        "name": name,
                        "lessons": lessons,
                    }
                )
        return holy_days

    def __import_lectionary(self) -> None:
        """Import lectionary from CSV file."""
        lectionary = {}
        with open("src/pylect/lectionary.csv", newline="", encoding="utf-8") as csvfile:
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
            advent_sunday = nov_30th - dt.timedelta(days=nov_30th.weekday() + 1)
        elif nov_30th.weekday() >= 3:
            advent_sunday = nov_30th + dt.timedelta(days=6 - nov_30th.weekday())

        return {
            "Epiphany": dt.date(date.year, 1, 6),
            "Ash Wednesday": easter_day - dt.timedelta(days=46),
            "Easter Day": easter_day,
            "Pentecost": easter_day + dt.timedelta(days=49),
            "Advent Sunday": advent_sunday,
            "Christmas Day": dt.date(date.year, 12, 25),
        }

    def __get_years(self, date: dt.date, anchors: dict) -> str:
        """Calculate the liturgical year for any given date.

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
        return None

    def __get_seasons(self, date: dt.date, anchors: dict) -> str:
        """Calculate the liturgical season for any given date"""

        if date < anchors["Epiphany"]:
            season = "Christmas"
        elif date < anchors["Ash Wednesday"]:
            season = "Epiphany"
        elif date < anchors["Easter Day"]:
            season = "Lent"
        elif date < anchors["Pentecost"]:
            season = "Easter"
        elif date < anchors["Advent Sunday"]:
            season = "Pentecost"
        elif date < anchors["Christmas Day"]:
            season = "Advent"
        else:
            season = "Christmas"
        return season

    def __get_principal_feasts(self, date: dt.date, anchors: dict) -> str:
        easter_day = anchors["Easter Day"]

        if date == easter_day:
            day = "Easter Day"
        elif date == easter_day + dt.timedelta(days=39):
            day = "Ascension Day"
        elif date == easter_day + dt.timedelta(days=49):
            day = "The Day of Pentecost"
        elif date == easter_day + dt.timedelta(days=56):
            day = "Trinity Sunday"
        elif date == dt.date(date.year, 11, 1):
            day = "All Saints' Day"
        elif date == dt.date(date.year, 12, 25):
            day = "The Nativity of Our Lord Jesus Christ: Christmas Day I"
        elif date == dt.date(date.year, 1, 6):
            day = "The Epiphany of Our Lord Jesus Christ"
        else:
            day = None
        return day

    def __get_ash_wednesday(self, date: dt.date, anchors: dict) -> str:
        if date == anchors["Ash Wednesday"]:
            return "Ash Wednesday"
        return None

    def __get_holy_week(self, date: dt.date, anchors: dict) -> str:
        easter_day = anchors["Easter Day"]

        if date == easter_day - dt.timedelta(days=7):
            day = "Palm Sunday"
        elif date == easter_day - dt.timedelta(days=6):
            day = "Monday of Holy Week"
        elif date == easter_day - dt.timedelta(days=5):
            day = "Tuesday of Holy Week"
        elif date == easter_day - dt.timedelta(days=4):
            day = "Wednesday of Holy Week"
        elif date == easter_day - dt.timedelta(days=3):
            day = "Maundy Thursday"
        elif date == easter_day - dt.timedelta(days=2):
            day = "Good Friday"
        elif date == easter_day - dt.timedelta(days=1):
            day = "Holy Saturday"
        else:
            day = None
        return day

    def __get_easter_week(self, date: dt.date, anchors: dict) -> str:
        easter_day = anchors["Easter Day"]

        if date == easter_day:
            day = "Easter Day: Principal Service"
        elif date == easter_day + dt.timedelta(days=1):
            day = "Monday of Easter Week"
        elif date == easter_day + dt.timedelta(days=2):
            day = "Tuesday of Easter Week"
        elif date == easter_day + dt.timedelta(days=3):
            day = "Wednesday of Easter Week"
        elif date == easter_day + dt.timedelta(days=4):
            day = "Thursday of Easter Week"
        elif date == easter_day + dt.timedelta(days=5):
            day = "Friday of Easter Week"
        elif date == easter_day + dt.timedelta(days=6):
            day = "Saturday of Easter Week"
        else:
            day = None
        return day

    def __get_sundays(self, date: dt.date, anchors: dict, season: str) -> str:
        """Return proper Sunday based on liturgical season"""
        if date.weekday() != 6:
            return None

        if season == "Advent":
            day = self.__get_advent_sundays(date, anchors)
        elif season == "Christmas":
            day = self.__get_christmas_sundays(date, anchors)
        elif season == "Epiphany":
            day = self.__get_epiphany_sundays(date, anchors)
        elif season == "Lent":
            day = self.__get_lent_sundays(date, anchors)
        elif season == "Easter":
            day = self.__get_easter_sundays(date, anchors)
        elif season == "Pentecost":
            day = self.__get_pentecost_sundays(date, anchors)
        return day

    def __get_advent_sundays(self, date: dt.date, anchors: dict) -> str | None:
        advent_sunday = anchors["Advent Sunday"]

        if date == advent_sunday:
            day = "The First Sunday in Advent"
        elif date == advent_sunday + dt.timedelta(days=7):
            day = "The Second Sunday in Advent"
        elif date == advent_sunday + dt.timedelta(days=14):
            day = "The Third Sunday in Advent"
        elif date == advent_sunday + dt.timedelta(days=21):
            day = "The Fourth Sunday in Advent"
        return day

    def __get_christmas_sundays(self, date: dt.date, anchors: dict) -> str | None:
        # There can be either one or two Sundays after Christmas
        christmas = anchors["Christmas Day"]

        if date.weekday() == 6 and date - christmas <= dt.timedelta(days=7):
            day = "The First Sunday of Christmas"
        elif date.weekday() == 6 and date - christmas >= dt.timedelta(days=8):
            day = "The Second Sunday of Christmas"
        return day

    def __get_epiphany_sundays(self, date: dt.date, anchors: dict) -> str | None:
        epiphany = anchors["Epiphany"]
        easter_day = anchors["Easter Day"]
        first_sunday_of_epiphany = epiphany + dt.timedelta(
            days=(6 - epiphany.weekday())
        )

        if date == first_sunday_of_epiphany:
            day = "The First Sunday of Epiphany: Baptism of Our Lord"
        elif date == first_sunday_of_epiphany + dt.timedelta(days=7):
            day = "The Second Sunday of Epiphany"
        # The number of Sundays after Epiphany can range from 4 to 9.
        # To account for this, check for the final two Sundays here.
        elif date == easter_day - dt.timedelta(days=56):
            day = "The Second to Last Sunday of Epiphany: World Mission"
        elif date == easter_day - dt.timedelta(days=49):
            day = "The Last Sunday of Epiphany: Transfiguration"
        # Continue checking dates from the start of Epiphany
        elif date == first_sunday_of_epiphany + dt.timedelta(days=14):
            day = "The Third Sunday of Epiphany"
        elif date == first_sunday_of_epiphany + dt.timedelta(days=21):
            day = "The Fourth Sunday of Epiphany"
        elif date == first_sunday_of_epiphany + dt.timedelta(days=28):
            day = "The Fifth Sunday of Epiphany"
        elif date == first_sunday_of_epiphany + dt.timedelta(days=35):
            day = "The Sixth Sunday of Epiphany"
        elif date == first_sunday_of_epiphany + dt.timedelta(days=42):
            day = "The Seventh Sunday of Epiphany"
        elif date == first_sunday_of_epiphany + dt.timedelta(days=49):
            day = "The Eighth Sunday of Epiphany"
        return day

    def __get_lent_sundays(self, date: dt.date, anchors: dict) -> str | None:
        easter_day = anchors["Easter Day"]

        if date == easter_day - dt.timedelta(days=42):
            day = "The First Sunday in Lent"
        elif date == easter_day - dt.timedelta(days=35):
            day = "The Second Sunday in Lent"
        elif date == easter_day - dt.timedelta(days=28):
            day = "The Third Sunday in Lent"
        elif date == easter_day - dt.timedelta(days=21):
            day = "The Fourth Sunday in Lent"
        elif date == easter_day - dt.timedelta(days=14):
            day = "The Fifth Sunday in Lent: Passion Sunday"
        return day

    def __get_easter_sundays(self, date: dt.date, anchors: dict) -> str | None:
        easter_day = anchors["Easter Day"]

        if date == easter_day + dt.timedelta(days=7):
            day = "The Second Sunday of Easter"
        elif date == easter_day + dt.timedelta(days=14):
            day = "The Third Sunday of Easter"
        elif date == easter_day + dt.timedelta(days=21):
            day = "The Fourth Sunday of Easter: Good Shepherd"
        elif date == easter_day + dt.timedelta(days=28):
            day = "The Fifth Sunday of Easter"
        elif date == easter_day + dt.timedelta(days=35):
            day = "The Sixth Sunday of Easter: Rogation Sunday"
        elif date == easter_day + dt.timedelta(days=42):
            day = "The Sunday after Ascension Day"
        return day

    def __get_pentecost_sundays(self, date: dt.date, anchors: dict) -> str | None:
        advent_sunday = anchors["Advent Sunday"]

        # Like Epiphany, the number of days in the season after Pentecost
        # varies from year to year. Thankfully, we can account for this by
        # simply calculating the proper day from the end of the season.
        if date == advent_sunday - dt.timedelta(days=203):
            day = "Proper 1"
        elif date == advent_sunday - dt.timedelta(days=196):
            day = "Proper 2"
        elif date == advent_sunday - dt.timedelta(days=189):
            day = "Proper 3"
        elif date == advent_sunday - dt.timedelta(days=182):
            day = "Proper 4"
        elif date == advent_sunday - dt.timedelta(days=175):
            day = "Proper 5"
        elif date == advent_sunday - dt.timedelta(days=168):
            day = "Proper 6"
        elif date == advent_sunday - dt.timedelta(days=161):
            day = "Proper 7"
        elif date == advent_sunday - dt.timedelta(days=154):
            day = "Proper 8"
        elif date == advent_sunday - dt.timedelta(days=147):
            day = "Proper 9"
        elif date == advent_sunday - dt.timedelta(days=140):
            day = "Proper 10"
        elif date == advent_sunday - dt.timedelta(days=133):
            day = "Proper 11"
        elif date == advent_sunday - dt.timedelta(days=126):
            day = "Proper 12"
        elif date == advent_sunday - dt.timedelta(days=119):
            day = "Proper 13"
        elif date == advent_sunday - dt.timedelta(days=112):
            day = "Proper 14"
        elif date == advent_sunday - dt.timedelta(days=105):
            day = "Proper 15"
        elif date == advent_sunday - dt.timedelta(days=98):
            day = "Proper 16"
        elif date == advent_sunday - dt.timedelta(days=91):
            day = "Proper 17"
        elif date == advent_sunday - dt.timedelta(days=84):
            day = "Proper 18"
        elif date == advent_sunday - dt.timedelta(days=77):
            day = "Proper 19"
        elif date == advent_sunday - dt.timedelta(days=70):
            day = "Proper 20"
        elif date == advent_sunday - dt.timedelta(days=63):
            day = "Proper 21"
        elif date == advent_sunday - dt.timedelta(days=56):
            day = "Proper 22"
        elif date == advent_sunday - dt.timedelta(days=49):
            day = "Proper 23"
        elif date == advent_sunday - dt.timedelta(days=42):
            day = "Proper 24"
        elif date == advent_sunday - dt.timedelta(days=35):
            day = "Proper 25"
        elif date == advent_sunday - dt.timedelta(days=28):
            day = "Proper 26"
        elif date == advent_sunday - dt.timedelta(days=21):
            day = "Proper 27"
        elif date == advent_sunday - dt.timedelta(days=14):
            day = "Proper 28"
        elif date == advent_sunday - dt.timedelta(days=7):
            day = "Proper 29: Christ the King"
        return day

    def __get_red_letter_days(self, date: dt.date) -> str:
        if date == dt.date(date.year, 1, 1):
            day = "The Circumcision and Holy Name of Our Lord Jesus Christ"
        elif date == dt.date(date.year, 1, 6):
            day = "The Epiphany of Our Lord Jesus Christ"
        elif date == dt.date(date.year, 1, 18):
            day = "Confession of Peter the Apostle"
        elif date == dt.date(date.year, 1, 25):
            day = "Conversion of Paul the Apostle"
        elif date == dt.date(date.year, 2, 2):
            day = "The Presentation of Our Lord Jesus Christ in the Temple"
        elif date == dt.date(date.year, 2, 24):
            day = "Matthias the Apostle"
        elif date == dt.date(date.year, 3, 19):
            day = "Joseph, Husband of the Virgin Mary and Guardian of Jesus"
        elif date == dt.date(date.year, 3, 25):
            day = "The Annunciation of our Lord Jesus Christ to the Virgin Mary"
        elif date == dt.date(date.year, 4, 25):
            day = "Mark the Evangelist"
        elif date == dt.date(date.year, 5, 1):
            day = "Philip and James, Apostles"
        elif date == dt.date(date.year, 5, 31):
            day = "The Visitation of the Virgin Mary to Elizabeth and Zechariah"
        elif date == dt.date(date.year, 6, 11):
            day = "Barnabas the Apostle"
        elif date == dt.date(date.year, 6, 24):
            day = "The Nativity of John the Baptist"
        elif date == dt.date(date.year, 6, 29):
            day = "Peter and Paul, Apostles"
        elif date == dt.date(date.year, 7, 22):
            day = "Mary Magdalene"
        elif date == dt.date(date.year, 7, 25):
            day = "James the Elder, Apostle"
        elif date == dt.date(date.year, 8, 6):
            day = "The Transfiguration of Our Lord Jesus Christ"
        elif date == dt.date(date.year, 8, 15):
            day = "The Virgin Mary, Mother of Our Lord Jesus Christ"
        elif date == dt.date(date.year, 8, 24):
            day = "Bartholomew the Apostle"
        elif date == dt.date(date.year, 9, 14):
            day = "Holy Cross Day"
        elif date == dt.date(date.year, 9, 21):
            day = "Matthew, Apostle and Evangelist"
        elif date == dt.date(date.year, 9, 29):
            day = "Holy Michael and All Angels"
        elif date == dt.date(date.year, 10, 18):
            day = "Luke the Evangelist and Companion of Paul"
        elif date == dt.date(date.year, 10, 23):
            day = "James of Jerusalem, Bishop and Martyr, Brother of Our Lord"
        elif date == dt.date(date.year, 10, 28):
            day = "Simon and Jude, Apostles"
        elif date == dt.date(date.year, 11, 1):
            day = "All Saints' Day"
        elif date == dt.date(date.year, 11, 30):
            day = "Andrew the Apostle"
        elif date == dt.date(date.year, 12, 21):
            day = "Thomas the Apostle"
        elif date == dt.date(date.year, 12, 25):
            day = "The Nativity of Our Lord Jesus Christ"
        elif date == dt.date(date.year, 12, 26):
            day = "Stephen, Deacon and Martyr"
        elif date == dt.date(date.year, 12, 27):
            day = "John, Apostle and Evangelist"
        elif date == dt.date(date.year, 12, 28):
            day = "The Holy Innocents"
        else:
            day = None
        return day

    def __get_lessons(self, name: str, year: str) -> list:
        lessons = self.__lectionary[name][year].split("|")
        return lessons
