from pylect.constants import LECTIONARY, Rank


class HolyDay:
    def __init__(self, name: str, year: str, season: str, rank: Rank):
        self.name = name
        self.year = year
        self.season = season
        self.rank = rank
        self.collect: str = self.__get_collect()
        self.lessons: dict[list[str]] = self.__get_lessons()

    def __get_collect(self):
        return ""

    def __get_lessons(self):
        if self.name == "Christmas Day":
            return (LECTIONARY.get(self.name).get("I").get(self.year),)
        elif self.name == "Easter Day":
            return (
                LECTIONARY.get(self.name)
                .get("Principal Service")
                .get(self.year),
            )
        else:
            return LECTIONARY.get(self.name).get(self.year)
