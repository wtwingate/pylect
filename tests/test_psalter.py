import pytest

from pylect.psalter import Psalter


class TestGetPsalm:
    psalter = Psalter()

    def test_whole_psalm(self):
        psalm = """Psalm 23

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
        assert self.psalter.get_psalm("Ps 23") == psalm

    def test_single_verse(self):
        psalm = """Psalm 23

4 Even though I walk through the valley of the shadow of death, I will fear no evil, *
for you are with me; your rod and your staff comfort me."""
        assert self.psalter.get_psalm("Ps 23:4") == psalm

    def test_split_verses(self):
        psalm = """Psalm 23

1 The Lord is my shepherd; *
therefore I can lack nothing.
3 He shall refresh my soul *
and bring me forth in the paths of righteousness for his Name's sake.
5 You shall prepare a table before me, in the presence of those who trouble me; *
you have anointed my head with oil, and my cup shall be full."""
        assert self.psalter.get_psalm("Ps 23:1,3,5") == psalm

    def test_parenthetical_reference(self):
        psalm = """Psalm 23

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
        assert self.psalter.get_psalm("Ps 23:1(2-5)6") == psalm

    def test_note_in_reference(self):
        psalm = """Psalm 89

20 I have found David my servant; *
with my holy oil have I anointed him.
21 My hand shall hold him fast, *
and my arm shall strengthen him.
22 The enemy shall not be able to do him violence; *
the son of wickedness shall not hurt him.
23 I will smite his foes before his face *
and strike down those who hate him.
24 My faithfulness and my mercy shall be with him, *
and in my Name shall his horn be exalted.
25 I will give him dominion over the sea, *
and with his right hand shall he rule the rivers.
26 He shall say to me, 'You are my Father, *
my God, and the rock of my salvation.'
27 And I will make him my firstborn, *
higher than the kings of the earth.
28 My mercy will I keep for him for ever, *
and my covenant shall stand fast with him.
29 His seed will I make to endure for ever *
and his throne as the days of heaven."""
        assert self.psalter.get_psalm("Ps 89:20-29v") == psalm

    def test_bad_reference_one(self):
        with pytest.raises(Exception):
            self.psalter.get_psalm("Ps 151:1-3")

    def test_bad_reference_two(self):
        with pytest.raises(Exception):
            self.psalter.get_psalm("Ps 23:7")
