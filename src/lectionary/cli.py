from lectionary.lectionary import Lectionary
from lectionary.psalter import Psalter
from lectionary.esv import get_esv_text
import datetime as dt


class CLI:
    def __init__(self) -> None:
        self.lectionary = Lectionary()
        self.psalter = Psalter()
        self.today = dt.date.today()
        self.sunday = self.__get_sunday()

    def __get_sunday(self):
        return self.today + dt.timedelta(days=6 - self.today.weekday())


def main():
    pass
    # TODO: Print the titles and lectionary references for these dates

    # TODO: Allow the user to choose one of the return dates from a list to
    #       copy the text of the readings to the system clipboard, or quit


if __name__ == "__main__":
    main()
