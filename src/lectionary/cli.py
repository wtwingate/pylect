import datetime as dt

from lectionary.esv import get_esv_text
from lectionary.lectionary import Lectionary
from lectionary.psalter import Psalter


class CLI:
    def __init__(self, date: dt.date | None = None) -> None:
        self.lectionary = Lectionary()
        self.psalter = Psalter()
        self.today = date if date is not None else dt.date.today()
        self.sunday = self.__get_sunday()

    def __get_sunday(self) -> dt.date:
        return self.today + dt.timedelta(days=6 - self.today.weekday())

    def get_holy_days_from_lectionary(self) -> list:
        dates = []
        current_day = self.today
        day_delta = dt.timedelta(days=1)
        while current_day <= self.sunday:
            dates.append(current_day)
            current_day += day_delta
        holy_days = self.lectionary.get_holy_days(dates)
        return holy_days


def main():
    # TODO: Print the titles and lectionary references for these dates
    cli = CLI(dt.date(2023, 12, 25))
    holy_days = cli.get_holy_days_from_lectionary()
    for day in holy_days:
        print(day.name)
        print(day.lessons)

    # TODO: Allow the user to choose one of the return dates from a list to
    #       copy the text of the readings to the system clipboard, or quit


if __name__ == "__main__":
    main()
