import datetime as dt

from pylect.lectionary import Lectionary


class TestLectionary:
    def test_anchors(self):
        """Tests that anchor dates and deltas are correctly calculated
        for the years 2000 - 3999.
        """

        # easter_day,sundays_after_epiphany,ash_wednesday,ascension_day,pentecost,collect_after_trinity,advent_sunday
        test_data = [
            [(3, 22), 4, (2, 4), (4, 30), (5, 10), 3, (11, 29)],
            [(3, 23), 4, (2, 5), (5, 1), (5, 11), 3, (11, 30)],
            [(3, 24), 4, (2, 6), (5, 2), (5, 12), 3, (12, 1)],
            [(3, 25), 5, (2, 7), (5, 3), (5, 13), 3, (12, 2)],
            [(3, 26), 5, (2, 8), (5, 4), (5, 14), 3, (12, 3)],
            [(3, 27), 5, (2, 9), (5, 5), (5, 15), 4, (11, 27)],
            [(3, 28), 5, (2, 10), (5, 6), (5, 16), 4, (11, 28)],
            [(3, 29), 5, (2, 11), (5, 7), (5, 17), 4, (11, 29)],
            [(3, 30), 5, (2, 12), (5, 8), (5, 18), 4, (11, 30)],
            [(3, 31), 5, (2, 13), (5, 9), (5, 19), 4, (12, 1)],
            [(4, 1), 6, (2, 14), (5, 10), (5, 20), 4, (12, 2)],
            [(4, 2), 6, (2, 15), (5, 11), (5, 21), 4, (12, 3)],
            [(4, 3), 6, (2, 16), (5, 12), (5, 22), 5, (11, 27)],
            [(4, 4), 6, (2, 17), (5, 13), (5, 23), 5, (11, 28)],
            [(4, 5), 6, (2, 18), (5, 14), (5, 24), 5, (11, 29)],
            [(4, 6), 6, (2, 19), (5, 15), (5, 25), 5, (11, 30)],
            [(4, 7), 6, (2, 20), (5, 16), (5, 26), 5, (12, 1)],
            [(4, 8), 7, (2, 21), (5, 17), (5, 27), 5, (12, 2)],
            [(4, 9), 7, (2, 22), (5, 18), (5, 28), 5, (12, 3)],
            [(4, 10), 7, (2, 23), (5, 19), (5, 29), 6, (11, 27)],
            [(4, 11), 7, (2, 24), (5, 20), (5, 30), 6, (11, 28)],
            [(4, 12), 7, (2, 25), (5, 21), (5, 31), 6, (11, 29)],
            [(4, 13), 7, (2, 26), (5, 22), (6, 1), 6, (11, 30)],
            [(4, 14), 7, (2, 27), (5, 23), (6, 2), 6, (12, 1)],
            [(4, 15), 8, (2, 28), (5, 24), (6, 3), 6, (12, 2)],
            [(4, 16), 8, (3, 1), (5, 25), (6, 4), 6, (12, 3)],
            [(4, 17), 8, (3, 2), (5, 26), (6, 5), 7, (11, 27)],
            [(4, 18), 8, (3, 3), (5, 27), (6, 6), 7, (11, 28)],
            [(4, 19), 8, (3, 4), (5, 28), (6, 7), 7, (11, 29)],
            [(4, 20), 8, (3, 5), (5, 29), (6, 8), 7, (11, 30)],
            [(4, 21), 8, (3, 6), (5, 30), (6, 9), 7, (12, 1)],
            [(4, 22), 9, (3, 7), (5, 31), (6, 10), 7, (12, 2)],
            [(4, 23), 9, (3, 8), (6, 1), (6, 11), 7, (12, 3)],
            [(4, 24), 9, (3, 9), (6, 2), (6, 12), 8, (11, 27)],
            [(4, 25), 9, (3, 10), (6, 3), (6, 13), 8, (11, 28)],
        ]

        for year in range(2000, 3000):
            print(f"Testing anchors for year {year}...")
            lectionary = Lectionary(dt.date(year, 1, 1))
            a = lectionary.anchors

            easter_month = a["easter_day"].month
            easter_day = a["easter_day"].day

            test_index = None
            test_case = None
            for index, test in enumerate(test_data):
                if easter_month == test[0][0] and easter_day == test[0][1]:
                    test_index = index
                    test_case = test
                    break

            if not test_case:
                raise Exception(f"Invalid date of Easter for year {year}")

            assert (
                a["easter_day"].month == test_case[0][0]
                and a["easter_day"].day == test_case[0][1]
            )

            # In leap years, the number of Sundays after Epiphany is the same
            # as if Easter Day were one day later than it appear in the test
            # data. Likewise, the date of Ash Wednesday occurs one day later
            # in the month of February.
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                alt_test_case = test_data[test_index + 1]
                assert a["sundays_after_epiphany"] == alt_test_case[1]
                assert a["ash_wednesday"].month == test_case[2][0]
                if a["ash_wednesday"].month == 2:
                    assert a["ash_wednesday"].day == test_case[2][1] + 1
                else:
                    assert a["ash_wednesday"].day == test_case[2][1]
            else:
                assert a["sundays_after_epiphany"] == test_case[1]
                assert (
                    a["ash_wednesday"].month == test_case[2][0]
                    and a["ash_wednesday"].day == test_case[2][1]
                )

            assert (
                a["ascension_day"].month == test_case[3][0]
                and a["ascension_day"].day == test_case[3][1]
            )

            assert (
                a["pentecost"].month == test_case[4][0]
                and a["pentecost"].day == test_case[4][1]
            )

            assert a["collect_after_trinity"] == test_case[5]

            assert (
                a["advent_sunday"].month == test_case[6][0]
                and a["advent_sunday"].day == test_case[6][1]
            )
