"""Creates the Psalter class which imports the plain text of the Psalter from a
PDF copy of the Book of Common Prayer 2019, cleans up the formatting, and then
creates a nested dictionary of the Psalms by chapter, verse, and half-verse. It
also provides convenient methods for retrieving the entire dictionary of Psalms
or for getting a nicely formatted string of any given Psalm reference.
"""

import json
import re


class Psalter:
    """Import the text of the Psalms as a dictionary and provide methods for retrieving them."""

    def __init__(self) -> None:
        self.__psalms = {}
        self.__load_psalms_from_json()

    def get_psalm(self, reference: str) -> str:
        """Get formatted psalm text by chapter and verse reference.

        Valid references must include the "chapter" number and may include a
        a verse or range of verses. A colon ":" is used as the delimiter between
        chapter and verse(s).

        Examples of valid references:
        "23" -> returns the entire text of Psalm 23
        "23:1" -> returns the only the first verse
        "23:1-3" -> returns the first three verses
        "23:1-3, 5" -> returns verses 1, 2, 3, and 5

        The lectionary designates some verses as optional by enclosing them in
        parentheses. For now, these are always included in the returned text.
        """
        text_list = []
        chapter, verses = self.__parse_reference(reference)
        psalm_chapter = self.__psalms.get(chapter)
        if psalm_chapter is None:
            raise ValueError("Error: invalid chapter reference")
        text_list.append(f"Psalm {chapter}\n")
        if verses is None:
            verses = psalm_chapter.keys()
        for verse in verses:
            psalm_verse = psalm_chapter.get(verse)
            if psalm_verse is None:
                raise ValueError("Error: invalid verse reference")
            text_list.append(f"{verse} {psalm_verse['head']} *")
            text_list.append(f"{psalm_verse['tail']}")
        psalm_text = "\n".join(text_list)
        return psalm_text

    def __parse_reference(self, reference: str) -> tuple[int, list[int]]:
        """Make human-readable verse references computer-friendly."""
        reference = reference.replace("Ps ", "").replace("v", "")
        chapter_ref = reference.split(":")[0]
        verse_ref = reference.split(":")[1]
        chapter = int(chapter_ref)
        verses = self.__parse_verse_reference(verse_ref)
        return chapter, verses

    def __parse_verse_reference(self, verse_ref: str) -> list[int]:

        vv = re.findall(r"\d+-?\d*", verse_ref)
        verses = []
        for ref in verse_refs:
            if "-" in ref:
                start = ref.split("-")[0]
                end = ref.split("-")[1]
                verses.extend([str(v) for v in range(int(start), int(end) + 1)])
            else:
                verses.append(ref)
        return chapter, verses

    def __load_psalms_from_json(self) -> None:
        """Load saved psalm dictionary"""
        with open("src/pylect/psalter.json", "r", encoding="utf-8") as json_file:
            self.__psalms = json.load(json_file)
