# pylint: skip-file

import pytest

from pylect.psalter import Psalter


class TestGetPsalm:
    psalter = Psalter()

    def test_whole_psalm(self):
        psalm = """Psalm 23

Dominus regit me

    1 The LORD is my shepherd; *
        therefore I can lack nothing.
    2 He shall feed me in green pastures *
        and lead me forth beside the waters of comfort.
    3 He shall refresh my soul *
        and bring me forth in the paths of righteousness for his Name’s sake.
    4 Even though I walk through the valley of the shadow of death, I will fear no evil, *
        for you are with me; your rod and your staff comfort me.
    5 You shall prepare a table before me, in the presence of those who trouble me; *
        you have anointed my head with oil, and my cup shall be full.
    6 Surely your goodness and mercy shall follow me all the days of my life, *
        and I will dwell in the house of the LORD for ever."""
        assert self.psalter.get_psalm("Psalm 23") == psalm

    def test_single_verse(self):
        psalm = """Psalm 23

Dominus regit me

    4 Even though I walk through the valley of the shadow of death, I will fear no evil, *
        for you are with me; your rod and your staff comfort me."""
        assert self.psalter.get_psalm("Psalm 23:4") == psalm

    def test_split_verses(self):
        psalm = """Psalm 23

Dominus regit me

    1 The LORD is my shepherd; *
        therefore I can lack nothing.
    3 He shall refresh my soul *
        and bring me forth in the paths of righteousness for his Name’s sake.
    5 You shall prepare a table before me, in the presence of those who trouble me; *
        you have anointed my head with oil, and my cup shall be full."""
        assert self.psalter.get_psalm("Psalm 23:1,3,5") == psalm

    def test_parenthetical_reference(self):
        psalm = """Psalm 23

Dominus regit me

    1 The LORD is my shepherd; *
        therefore I can lack nothing.
    2 He shall feed me in green pastures *
        and lead me forth beside the waters of comfort.
    3 He shall refresh my soul *
        and bring me forth in the paths of righteousness for his Name’s sake.
    4 Even though I walk through the valley of the shadow of death, I will fear no evil, *
        for you are with me; your rod and your staff comfort me.
    5 You shall prepare a table before me, in the presence of those who trouble me; *
        you have anointed my head with oil, and my cup shall be full.
    6 Surely your goodness and mercy shall follow me all the days of my life, *
        and I will dwell in the house of the LORD for ever."""
        assert self.psalter.get_psalm("Psalm 23:1(2-5)6") == psalm

    def test_bad_reference_one(self):
        with pytest.raises(Exception):
            self.psalter.get_psalm("Psalm 151:1-3")

    def test_bad_reference_two(self):
        with pytest.raises(Exception):
            self.psalter.get_psalm("Psalm 23:7")
