from lectionary.psalter import Psalter
import pytest


class TestGetPsalm:

    def test_whole_psalm(self):
        psalter = Psalter()
        psalm_23 = """Psalm 23

1 The Lord is my shepherd; *
therefore I can lack nothing.
2 He shall feed me in green pastures *
and lead me forth beside the waters of comfort.
3 He shall refresh my soul *
and bring me forth in the paths of righteousness for his Name's sake.
4 Even though I walk through the valley of the shadow of death, I will fear no evil, *
for you are with me; your rod and your staff comfort me.
5 You shall prepare a table before me, in the presence of those who trouble me; *
you have anointed my head with oil, and my cup shall be full.
6 Surely your goodness and mercy shall follow me all the days of my life, *
and I will dwell in the house of the Lord for ever."""
        assert psalter.get_psalm("23") == psalm_23
