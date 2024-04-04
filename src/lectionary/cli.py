import datetime as dt

from lectionary.esv import get_esv_text
from lectionary.lectionary import Lectionary
from lectionary.psalter import Psalter


class CLI:
    def __init__(
        self, start_date: dt.date | None = None, end_date: dt.date | None = None
    ) -> None:
        self.lectionary = Lectionary()
        self.psalter = Psalter()
        self.start_date = start_date if start_date is not None else dt.date.today()
        self.end_date = end_date if end_date is not None else self.__get_sunday()

    def __get_sunday(self) -> dt.date:
        return self.today + dt.timedelta(days=6 - self.today.weekday())

    def get_holy_days_from_lectionary(self) -> list:
        dates = []
        current_day = self.start_date
        day_delta = dt.timedelta(days=1)
        while current_day <= self.end_date:
            dates.append(current_day)
            current_day += day_delta
        holy_days = self.lectionary.get_holy_days(dates)
        return holy_days


def main():
    # TODO: Print the titles and lectionary references for these dates
    cli = CLI(dt.date(2024, 4, 1), dt.date(2024, 6, 1))
    holy_days = cli.get_holy_days_from_lectionary()
    for day in holy_days:
        print(day.name)
        print(day.lessons)

    # TODO: Allow the user to choose one of the return dates from a list to
    #       copy the text of the readings to the system clipboard, or quit


if __name__ == "__main__":
    main()
