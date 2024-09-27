import datetime as dt

from dateutil.easter import easter
from dateutil.relativedelta import SU, relativedelta

from pylect.constants import (
    HOLY_WEEK_DELTAS,
    EASTER_WEEK_DELTAS,
    ADVENT_DELTAS,
    EPIPHANY_DELTAS,
    LENT_DELTAS,
    EASTER_DELTAS,
    PENTECOST_DELTAS,
    RED_LETTER_DAYS,
)


class Lectionary:
    def __init__(self, date):
        self.date = date
        self.anchors = self.__calc_anchors()
        self.lit_year = self.__calc_lit_year()
        self.lit_season = self.__calc_lit_season()
        self.lit_days = self.__calc_lit_days()

    def __calc_anchors(self):
        # Easter Day
        easter_day = easter(self.date.year, 3)

        # Ash Wednesday
        ash_wednesday = easter_day - dt.timedelta(days=46)

        # Ascension Day
        ascension_day = easter_day + dt.timedelta(days=39)

        # Day of Pentecost
        pentecost = easter_day + dt.timedelta(days=49)

        # Advent Sunday
        christmas_day = dt.date(self.date.year, 12, 25)
        advent_sunday = christmas_day + relativedelta(days=(-1), weekday=SU(-4))

        # Sundays after Epiphany
        epiphany = dt.date(self.date.year, 1, 6)
        first_sunday_after_epiphany = epiphany + relativedelta(
            days=(+1), weekday=SU(+1)
        )
        last_sunday_after_epiphany = ash_wednesday + relativedelta(weekday=SU(-1))
        epiphany_delta = last_sunday_after_epiphany - first_sunday_after_epiphany
        sundays_after_epiphany = (epiphany_delta.days // 7) + 1

        # First collect after Trinity Sunday
        ordinary_time_delta = advent_sunday - pentecost
        collect_after_trinity = 32 - (ordinary_time_delta.days // 7)

        return {
            "easter_day": easter_day,
            "sundays_after_epiphany": sundays_after_epiphany,
            "ash_wednesday": ash_wednesday,
            "ascension_day": ascension_day,
            "pentecost": pentecost,
            "collect_after_trinity": collect_after_trinity,
            "advent_sunday": advent_sunday,
        }

    def __calc_lit_year(self):
        if self.date >= self.anchors["advent_sunday"]:
            year_start = self.date.year
        else:
            year_start = self.date.year - 1

        if year_start % 3 == 0:
            return "A"
        if year_start % 3 == 1:
            return "B"
        if year_start % 3 == 2:
            return "C"

    def __calc_lit_season(self):
        if self.date < dt.date(self.date.year, 1, 6):
            return "Christmas"
        if self.date < self.anchors["ash_wednesday"]:
            return "Epiphany"
        if self.date < self.anchors["easter_day"]:
            return "Lent"
        if self.date < self.anchors["pentecost"]:
            return "Easter"
        if self.date < self.anchors["advent_sunday"]:
            return "Pentecost"
        if self.date < dt.date(self.date.year, 12, 25):
            return "Advent"
        return "Christmas"

    def __calc_lit_days(self):
        lit_days = [
            self.__principal_feasts(),
            self.__principal_eves(),
            self.__ash_wednesday(),
            self.__holy_week(),
            self.__easter_week(),
            self.__sundays(),
            self.__red_letter_days(),
        ]

        # use list comprehension to filter out all values that are None
        return [day for day in lit_days if day]

    def __principal_feasts(self):
        if self.date == self.anchors["easter_day"]:
            return "Easter Day"
        if self.date == self.anchors["ascension_day"]:
            return "Ascension Day"
        if self.date == self.anchors["pentecost"]:
            return "Day of Pentecost"
        if self.date == self.anchors["pentecost"] + dt.timedelta(days=7):
            return "Trinity Sunday"
        if self.date == dt.date(self.date.year, 12, 25):
            return "Christmas Day"
        if self.date == dt.date(self.date.year, 1, 6):
            return "The Epiphany"
        if self.date == dt.date(self.date.year, 11, 1):
            return "All Saints' Day"

    def __principal_eves(self):
        if self.date == self.anchors["easter_day"] - dt.timedelta(days=1):
            return "Easter Eve"
        if self.date == dt.date(self.date.year, 12, 24):
            return "Christmas Eve"

    def __ash_wednesday(self):
        if self.date == self.anchors["ash_wednesday"]:
            return "Ash Wednesday"

    def __holy_week(self):
        delta = self.anchors["easter_day"] - self.date
        return HOLY_WEEK_DELTAS.get(delta.days)

    def __easter_week(self):
        delta = self.date - self.anchors["easter_day"]
        return EASTER_WEEK_DELTAS.get(delta.days)

    def __sundays(self):
        if self.date.weekday() != 6:
            return None

        if self.lit_season == "Advent":
            return self.__advent_sundays()
        if self.lit_season == "Christmas":
            return self.__christmas_sundays()
        if self.lit_season == "Epiphany":
            return self.__epiphany_sundays()
        if self.lit_season == "Lent":
            return self.__lent_sundays()
        if self.lit_season == "Easter":
            return self.__easter_sundays()
        if self.lit_season == "Pentecost":
            return self.__pentecost_sundays()

    def __advent_sundays(self):
        delta = self.date - self.anchors["ash_wednesday"]
        return ADVENT_DELTAS.get(delta.days)

    def __christmas_sundays(self):
        christmas_day = dt.date(self.date.year, 12, 25)
        if christmas_day < self.date <= christmas_day + dt.timedelta(days=7):
            return "First Sunday after Christmas"
        else:
            return "Second Sunday after Christmas"

    def __epiphany_sundays(self):
        epiphany = dt.date(self.date.year, 1, 6)
        first_sunday_after_epiphany = epiphany + relativedelta(
            days=(+1), weekday=SU(+1)
        )
        delta = self.date - first_sunday_after_epiphany

        # The number of Sundays after Epiphany can range from 4 to 9.
        # To account for this, check for the final two Sundays first.
        if self.date == self.anchors["easter_day"] - dt.timedelta(days=56):
            return "Second to Last Sunday after Epiphany"
        if self.date == self.anchors["easter_day"] - dt.timedelta(days=49):
            return "Last Sunday after Epiphany"

        return EPIPHANY_DELTAS.get(delta.days)

    def __lent_sundays(self):
        delta = self.anchors["easter_day"] - self.date
        return LENT_DELTAS.get(delta.days)

    def __easter_sundays(self):
        delta = self.date - self.anchors["easter_day"]
        return EASTER_DELTAS.get(delta.days)

    def __pentecost_sundays(self):
        delta = self.anchors["advent_sunday"] - self.date
        return PENTECOST_DELTAS.get(delta.days)

    def __red_letter_days(self):
        return RED_LETTER_DAYS.get(self.date.month).get(self.date.day)
