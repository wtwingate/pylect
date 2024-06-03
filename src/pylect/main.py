"""This is the primary user facing module of the program. The CLI class
is initiated when the program is started and begin running a script
that gather the appropriate readings for the lectionary for the given
date range. It then prompts the user to select one or more of the
readings so that it can fetch the texts and copy them to the system
clipboard.
"""

from datetime import date, timedelta
import sys

import pyperclip
from pylect.esv import get_esv_text
from pylect.holyday import HolyDay
from pylect.lectionary import Lectionary
from pylect.psalter import Psalter


def get_holy_days() -> list[HolyDay]:
    """Iterate through and range of dates and search for the corresponding
    holy days in the lectionary.
    """

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
        holy_days.extend(Lectionary(this_date).holy_days)
        this_date += timedelta(days=1)

    return holy_days


def cli_start() -> None:
    holy_days = get_holy_days()

    print()
    print("*** Welcome to the Pylect CLI ***\n")
    print("Here are the upcoming days in the lectionary:\n")
    for i, day in enumerate(holy_days):
        print(f"{i + 1})\t{day.name}:")
        for v in day.lessons.values():
            print(f"\t- {" or ".join(v)}")
        print()

    print(
        "Enter a number to copy the text of the lessons into your clipboard"
        " or press and enter 'q' to exit the program.\n"
    )

    cli_loop(holy_days)


def cli_loop(holy_days: list[HolyDay]) -> None:
    while True:
        choice = input("Please enter your choice: ")

        if choice.lower().startswith("q"):
            break

        try:
            day = holy_days[int(choice) - 1]
        except IndexError:
            print("Error: invalid selection")
            continue

        psalter = Psalter()

        try:
            texts = [day.name]
            for k, v in day.lessons.items():
                if k == "Psalm":
                    texts.append(psalter.get_psalm(v[0]))
                else:
                    texts.append(get_esv_text(v[0]))
        except ValueError:
            print("Error: could not fetch requested texts")
            continue

        pyperclip.copy("\n\n".join(texts))
        print(f"Lessons for {day.name} copied to clipboard!")


if __name__ == "__main__":
    cli_start()
