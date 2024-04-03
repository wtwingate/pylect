import csv
import datetime as dt
import dateutil


class Lectionary:
    def __init__(self) -> None:
        self.__lectionary = self.__import_lectionary()

    def get_lessons(self, date: dt.date) -> tuple[str, list]:
        major_days = self.__get_major_days(date)
        year = self.__get_year(date, major_days["Advent Sunday"])
        season = self.__get_season(date, major_days)
        day = self.__get_day(date, major_days, season)

        lessons = self.__lectionary[day][year].split("|")
        return day, lessons

    def __import_lectionary(self) -> None:
        """Import lectionary from CSV file"""
        lectionary = {}
        with open("docs/lectionary.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lectionary[row["Day"]] = row
        return lectionary

    def __get_major_days(self, date: dt.date) -> dict:
        easter_day = dateutil.easter.easter(date.year)

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

    def __get_year(self, date: dt.date, advent_sunday: dt.date) -> str:
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

    def __get_season(self, date: dt.date, days: dict) -> str:
        if date < days["Epiphany"]:
            return "Christmas"
        elif date < days["Ash Wednesday"]:
            return "Epiphany"
        elif date < days["Easter Day"]:
            return "Lent"
        elif date < days["Pentecost"]:
            return "Easter"
        elif date < days["Advent Sunday"]:
            return "Pentecost"
        elif date < days["Christmas Day"]:
            return "Advent"
        else:
            return "Christmas"

    def __get_day(self, date: dt.date, days: dict, season: str) -> str:
        christmas = days["Christmas Day"]
        epiphany = days["Epiphany"]
        ash_wednesday = days["Ash Wednesday"]
        easter_day = days["Easter Day"]
        pentecost = days["Pentecost"]
        advent_sunday = days["Advent Sunday"]

        if season == "Christmas":
            if date == christmas:
                return "Christmas Day I"
            if date - christmas <= dt.timedelta(days=7):
                return "The First Sunday of Christmas"
            if date - christmas >= dt.timedelta(days=8):
                return "The Second Sunday of Christmas"

        if season == "Epiphany":
            first_sunday_of_epiphany = epiphany + dt.timedelta(
                days=(6 - epiphany.weekday())
            )
            if date == epiphany:
                return "Epiphany"
            if date == first_sunday_of_epiphany:
                return "The First Sunday of Epiphany: Baptism of Our Lord"
            if date == first_sunday_of_epiphany + dt.timedelta(days=7):
                return "The Second Sunday of Epiphany"
            # The number of Sundays after Epiphany can range from 4 to 9.
            # To account for this, check for the final two Sundays here.
            if date == easter_day - dt.timedelta(days=56):
                return "The Second to Last Sunday of Epiphany"
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
            if date == ash_wednesday:
                return "Ash Wednesday"
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

        if season == "Easter":
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
            if date == easter_day + dt.timedelta(days=39):
                return "Ascension Day"
            if date == easter_day + dt.timedelta(days=42):
                return "The Sunday after Ascension Day"

        if season == "Pentecost":
            if date == pentecost:
                return "Pentecost"
            if date == pentecost + dt.timedelta(days=7):
                return "Trinity Sunday"
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

        if season == "Advent":
            if date == advent_sunday:
                return "The First Sunday in Advent"
            if date == advent_sunday + dt.timedelta(days=7):
                return "The Second Sunday in Advent"
            if date == advent_sunday + dt.timedelta(days=14):
                return "The Third Sunday in Advent"
            if date == advent_sunday + dt.timedelta(days=21):
                return "The Fourth Sunday in Advent"
