"""This is the primary user facing module of the program. The CLI class
is initiated when the program is started and begin running a script
that gather the appropriate readings for the lectionary for the given
date range. It then prompts the user to select one or more of the
readings so that it can fetch the texts and copy them to the system
clipboard.
"""

from datetime import date, timedelta
import sys

from pylect.esv import get_esv_text
from pylect.holyday import HolyDay
from pylect.lectionary import Lectionary
from pylect.psalter import Psalter


# def get_next_week(self) -> date:
#     """Set the end date to 7 days from the start date if no end date is specified"""
#     return self.__start_date + timedelta(days=7)


# def get_holy_days(self) -> list:
#     """Iterate through range of dates and search for matches in the lectionary."""
#     dates = []
#     current_day = self.__start_date
#     day_delta = timedelta(days=1)
#     while current_day <= self.__end_date:
#         dates.append(current_day)
#         current_day += day_delta
#     holy_days = self.__lectionary.get_holy_days(dates)
#     return holy_days


# def get_texts(self) -> None:
#     """Print holy days within date range and allow user to fetch and copy specified texts."""
#     print()
#     print(
#         f"Sundays and Holy Days between {self.__start_date} and {self.__end_date}:"
#     )
#     print()
#     for index, holy_day in enumerate(self.__holy_days):
#         print(f"{index + 1}) {holy_day['name']} [{holy_day['date']}]")
#         for lesson in holy_day["lessons"]:
#             print(f"   * {lesson}")
#         print()
#     print(
#         """Enter a number to copy the lessons for the selected Sunday or Holy Day
# into your clipboard, or enter "q" to quit the program."""
#     )
#     while True:
#         selection = input("Please enter your selection: ")
#         if selection.lower().startswith("q"):
#             break
#         try:
#             holy_day = self.__holy_days[int(selection) - 1]
#             lessons = holy_day["lessons"]
#         except IndexError:
#             print("Error: invalid selection")
#             continue
#         try:
#             texts = []
#             for lesson in lessons:
#                 lesson = lesson.split(" or ")[0]
#                 try:
#                     if lesson.startswith("Ps"):
#                         texts.append(self.__psalter.get_psalm(lesson))
#                     else:
#                         texts.append(get_esv_text(lesson))
#                 except ValueError:
#                     print(f"Error: could not get text for {lesson}")
#             text = "\n\n".join(texts)
#             pyperclip.copy(text)
#             print(f"Lessons for {holy_day['name']} copied to clipboard!")
#         except ValueError:
#             print("Error: could not fetch requested texts")


def main():
    start_date: date
    end_date: date

    if len(sys.argv) == 2:
        try:
            start = [int(x) for x in sys.argv[1].split("-")]
            start_date = date(start[0], start[1], start[2])
            end_date = start_date + timedelta(days=7)
        except IndexError:
            print("Error: Invalid date format in arguments")
            sys.exit(1)
    elif len(sys.argv) == 3:
        try:
            start = [int(x) for x in sys.argv[1].split("-")]
            start_date = date(start[0], start[1], start[2])
            end = [int(x) for x in sys.argv[2].split("-")]
            end_date = date(end[0], end[1], end[2])
        except IndexError:
            print("Error: Invalid date format in arguments")
            sys.exit()
    else:
        start_date = date.today()
        end_date = start_date + timedelta(days=7)

    holy_days: list[HolyDay] = []
    this_date = start_date
    while this_date <= end_date:
        holy_days.extend(check_lectionary(this_date))
        this_date += timedelta(days=1)

    psalter = Psalter()
    for day in holy_days:
        texts = [day.name]
        for k, v in day.lessons.items():
            if k == "Psalm":
                texts.append(psalter.get_psalm(v[0]))
            else:
                texts.append(get_esv_text(v[0]))
        print("\n\n".join(texts))


def check_lectionary(this_date: date) -> list[HolyDay]:
    lectionary = Lectionary(this_date)
    return lectionary.holy_days


if __name__ == "__main__":
    main()
