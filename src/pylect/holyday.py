class HolyDay:
    def __init__(self, name: str, year: int, season: str, rank: int):
        self.name = name
        self.year = year
        self.season = season
        self.rank = rank
        self.collect = self.__get_collect()
        self.lessons = self.__get_lessons()

    def __get_collect(self):
        pass

    def __get_lessons(self):
        pass
