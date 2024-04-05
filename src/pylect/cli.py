"""This is the primary user facing module of the program. The CLI class is
initiated when the program is started and begin running a script that gather the
appropriate readings for the lectionary for the given date range. It then
prompts the user to select one or more of the readings so that it can fetch the
texts and copy them to the system clipboard.
"""

import datetime as dt
import pyperclip
from pylect.esv import get_esv_text
from pylect.lectionary import Lectionary
from pylect.psalter import Psalter


class CLI:
    """The CLI class allows users to interact with the public methods of the other classes."""

    def __init__(
        self, start_date: dt.date | None = None, end_date: dt.date | None = None
    ) -> None:
        self.__lectionary = Lectionary()
        self.__psalter = Psalter()
        self.__start_date = start_date if start_date is not None else dt.date.today()
        self.__end_date = end_date if end_date is not None else self.__get_sunday()
        self.__holy_days = self.__get_holy_days()

    def __get_sunday(self) -> dt.date:
        """Get the date for the upcoming Sunday if no end date is specified."""
        return self.__start_date + dt.timedelta(days=6 - self.__start_date.weekday())

    def __get_holy_days(self) -> list:
        """Iterate through range of dates and search for matches in the lectionary."""
        dates = []
        current_day = self.__start_date
        day_delta = dt.timedelta(days=1)
        while current_day <= self.__end_date:
            dates.append(current_day)
            current_day += day_delta
        holy_days = self.__lectionary.get_holy_days(dates)
        return holy_days

    def get_texts(self) -> None:
        """Print holy days within date range and allow user to fetch and copy specified texts."""
        print()
        print(
            f"Sundays and Holy Days between {self.__start_date} and {self.__end_date}:"
        )
        print()
        for index, holy_day in enumerate(self.__holy_days):
            print(f"{index + 1}) {holy_day['name']}")
            for lesson in holy_day["lessons"]:
                print(f"   * {lesson}")
            print()
        print(
            """Enter a number to copy the lessons for the selected Sunday or Holy Day
into your clipboard, or enter "q" to quit the program."""
        )
        while True:
            selection = input("Please enter your selection: ")
            if selection.lower().startswith("q"):
                break
            try:
                holy_day = self.__holy_days[int(selection) - 1]
                lessons = holy_day["lessons"]
            except IndexError:
                print("Error: invalid selection")
                continue
            try:
                texts = []
                for lesson in lessons:
                    if lesson.startswith("Ps"):
                        texts.append(self.__psalter.get_psalm(lesson))
                    else:
                        if "or" in lesson:
                            texts.append(get_esv_text(lesson.split(" or ")[0]))
                        else:
                            texts.append(get_esv_text(lesson))
                text = "\n\n".join(texts)
                pyperclip.copy(text)
                print(f"Lessons for {holy_day['name']} copied to clipboard!")
            except ValueError:
                print("Error: could not fetch requested texts")


def main():
    """Entry point for the program."""
    cli = CLI()
    cli.get_texts()


if __name__ == "__main__":
    main()
