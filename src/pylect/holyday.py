"""Provides access to the HolyDay class."""

from pylect.constants import LECTIONARY, Rank


class HolyDay:
    """The HolyDay class is data structure that contains all the relevant
    information for any given Sunday, Holy Day, or Commemoration found
    in the lectionary."""

    def __init__(self, name: str, year: str, season: str, rank: Rank):
        self.name: str = name
        self.year: str = year
        self.season: str = season
        self.rank: Rank = rank
        self.collect: str = self.__get_collect()
        self.lessons: dict = self.__get_lessons()

    def __get_collect(self) -> str:
        pass

    def __get_lessons(self) -> dict:
        if self.name == "Christmas Day":
            return (LECTIONARY.get(self.name).get("I").get(self.year),)

        if self.name == "Easter Day":
            return (
                LECTIONARY.get(self.name)
                .get("Principal Service")
                .get(self.year),
            )

        return LECTIONARY.get(self.name).get(self.year)
