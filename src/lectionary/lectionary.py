import csv
import calendar
import datetime
import dateutil


class Lectionary:
    def __init__(self) -> None:
        self.__lectionary = {}
        self.__import_lectionary()

    def get_lessons(self, date: datetime.date) -> str:
        day, year = self.__get_liturgical_day(date)
        lessons = self.__lectionary[day][year].split("; ")
        return lessons

    def __import_lectionary(self) -> None:
        """Import lectionary from CSV file"""
        with open("docs/sunday_lectionary.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.__lectionary[row["DAY"]] = row

    def __get_liturgical_day(self, today: datetime.date) -> tuple:
        easter_sunday = dateutil.easter.easter(today.year)
        this_sunday = today + datetime.timedelta(6 - today.weekday())
        return ("PROPER 5", "YEAR A")


if __name__ == "__main__":
    lectionary = Lectionary()
    print(lectionary.get_lessons("today"))
