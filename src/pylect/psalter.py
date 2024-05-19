"""The Psalter class provides an easy way to fetch the text of the New Coverdale Psalter."""

import json
import re


class Psalter:
    """Import the text of the Psalms as a dictionary and provide methods for retrieving them."""

    def __init__(self) -> None:
        self._psalms = {}
        self._load_psalms_from_json()

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
        "23:1-3(4-6)" -> returns verses 1-6

        The lectionary designates some verses as optional by enclosing them in
        parentheses. For now, these are always included in the returned text.
        """
        text_list = []
        chapter, verses = self._parse_reference(reference)
        psalm = self._psalms[chapter - 1] # zero-indexing ftw
        text_list.append(f"Psalm {psalm["number"]}\n")
        if len(verses) == 0:
            verses = psalm["verses"]
        else:
            verses = [psalm["verses"][v - 1] for v in verses]
        for verse in verses:
            text_list.append(f"{verse["number"]} {verse["first_half"]} *")
            text_list.append(f"{verse["second_half"]}")
        psalm_text = "\n".join(text_list)
        return psalm_text

    def _parse_reference(self, ref: str) -> tuple[int, list[int]]:
        """Make human-readable verse references computer-friendly."""
        ref = ref.replace("Ps ", "").replace("v", "")
        chapter = int(ref.split(":")[0])
        if ":" in ref:
            verses = self._parse_verse_reference(ref.split(":")[1])
        else:
            verses = []
        return chapter, verses

    def _parse_verse_reference(self, verse_ref: str) -> list[int]:
        verse_ref = re.split(r";|,|\(|\)| ", verse_ref)
        verse_nums = []
        for ref in verse_ref:
            if len(ref) == 0:
                continue
            if "-" in ref:
                start = ref.split("-")[0]
                end = ref.split("-")[1]
                verse_nums.extend([v for v in range(int(start), int(end) + 1)])
            else:
                verse_nums.append(int(ref))
        return verse_nums

    def _load_psalms_from_json(self) -> None:
        """Load saved psalm dictionary"""
        with open("src/pylect/psalter.json", "r", encoding="utf-8") as json_file:
            self._psalms = json.load(json_file)