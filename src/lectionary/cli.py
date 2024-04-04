import datetime as dt
import pyperclip

from lectionary.esv import get_esv_text
from lectionary.lectionary import Lectionary
from lectionary.psalter import Psalter


class CLI:
    def __init__(
        self, start_date: dt.date | None = None, end_date: dt.date | None = None
    ) -> None:
        self.__lectionary = Lectionary()
        self.__psalter = Psalter()
        self.__start_date = start_date if start_date is not None else dt.date.today()
        self.__end_date = end_date if end_date is not None else self.__get_sunday()
        self.__holy_days = self.__get_holy_days()

    def __get_sunday(self) -> dt.date:
        return self.__start_date + dt.timedelta(days=6 - self.__start_date.weekday())

    def __get_holy_days(self) -> list:
        dates = []
        current_day = self.__start_date
        day_delta = dt.timedelta(days=1)
        while current_day <= self.__end_date:
            dates.append(current_day)
            current_day += day_delta
        holy_days = self.__lectionary.get_holy_days(dates)
        return holy_days

    def get_texts(self) -> None:
        print()
        print(
            f"Sundays and Holy Days between {self.__start_date} and {self.__end_date}:"
        )
        print()
        for i in range(len(self.__holy_days)):
            day = self.__holy_days[i]
            print(f"{i + 1}) {day.name}")
            for lesson in day.lessons:
                print(f"   * {lesson}")
            print()
        print(
            """Enter a number to copy the lessons of the selected Sunday or Holy Day
into your clipboard, or enter "q" to quit the program."""
        )
        while True:
            selection = input("Please enter your selection: ")
            if selection.lower().startswith("q"):
                break
            try:
                holy_day = self.__holy_days[int(selection) - 1]
                lessons = holy_day.lessons
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
                print(f"Lessons for {holy_day.name} copied to clipboard!")
            except:
                print("Error: invalid selection")


def main():
    cli = CLI()
    cli.get_texts()


if __name__ == "__main__":
    main()
