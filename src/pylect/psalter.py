"""Provides access to the Psalter class."""

import json
import re


class Psalter:
    """The Psalter class imports the text of the New Coverdale Psalter as a
    dictionary and provides methods for getting the text of the Psalms."""

    def __init__(self) -> None:
        self.psalms: dict = self.__load_psalms_from_json()

    def get_psalm(self, reference: str) -> str:
        """Get formatted psalm text by chapter and verse reference.

        Valid references must include the "chapter" number and may include
        a verse or range of verses. A colon ":" is used as the delimiter
        between chapter and verse(s), and a comma "," is used to separate
        verse references.

        Examples of valid references:
        "23" -> returns the entire text of Psalm 23
        "23:1" -> returns the only the first verse
        "23:1-3" -> returns the first three verses
        "23:1-3, 5" -> returns verses 1, 2, 3, and 5
        "23:1-3(4-6)" -> returns verses 1-6

        The lectionary indicates optional verses by enclosing them in
        parentheses. For now, these are always included in the returned text.
        """

        chapter, verses = self.__parse_reference(reference)
        psalm = self.psalms[chapter - 1]  # convert to zero index

        if len(verses) == 0:  # if only chapter ref was provided
            verses = psalm["verses"]
        else:
            verses = [psalm["verses"][v - 1] for v in verses]

        text_list = []
        text_list.append(f"Psalm {psalm["number"]}\n")
        text_list.append(f"{psalm["latin_title"]}\n")
        for verse in verses:
            text_list.append(f"    {verse["number"]} {verse["first_half"]} *")
            text_list.append(f"        {verse["second_half"]}")
        psalm_text = "\n".join(text_list)

        return psalm_text

    def __parse_reference(self, ref: str) -> tuple[int, list[int]]:
        """Make human-readable psalm references computer-friendly."""

        ref = ref.replace("Psalm ", "")
        chapter = int(ref.split(":")[0])
        if ":" in ref:
            verses = self.__parse_verses(ref.split(":")[1])
        else:
            verses = []

        return chapter, verses

    def __parse_verses(self, verse_ref: str) -> list[int]:
        """Parse verse references into a list of verse numbers."""

        verse_nums = []
        for ref in re.split(r";|,|\(|\)| ", verse_ref):
            if len(ref) == 0:
                continue
            if "-" in ref:
                start = ref.split("-")[0]
                end = ref.split("-")[1]
                verse_nums.extend(list(range(int(start), int(end) + 1)))
            else:
                verse_nums.append(int(ref))

        return verse_nums

    def __load_psalms_from_json(self) -> dict:
        """Load saved psalm into dictionary"""

        with open(
            "src/pylect/psalter.json", "r", encoding="utf-8"
        ) as json_file:
            return json.load(json_file)
