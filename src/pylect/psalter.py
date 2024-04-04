"""Creates a Psalter object which imports the plain text of the Psalter from a
PDF copy of the Book of Common Prayer 2019, cleans up the formatting, and then
creates a nested dictionary of the Psalms by chapter, verse, and half-verse. It
also provides convenient methods for retrieving the entire dictionary of Psalms
or for getting a nicely formatted string of any given Psalm reference.
"""

import json
import os
import re
import fitz


class Psalter:
    """The Psalter class imports the Psalms and provides methods for retrieving them."""

    def __init__(self) -> None:
        self.__psalms = {}
        self.__import_psalms()

    def get_psalms(self) -> dict:
        """Return the entire Psalter as a dictionary"""
        return self.__psalms

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

    def __parse_reference(self, reference: str) -> tuple[str, list]:
        """Make human-readable verse references computer-friendly."""
        ref = reference.replace("Ps ", "")
        ref = ref.replace("v", "")
        if "or" in ref:
            psalm_reference = ref.split(" or ")[0]  # use first option
        else:
            psalm_reference = ref
        chapter_verse = psalm_reference.split(":")
        chapter = chapter_verse[0]
        if len(chapter_verse) == 1:
            return chapter, None
        verse_split = chapter_verse[1]
        verse_refs = re.findall(r"\d+-?\d*", verse_split)
        verses = []
        for ref in verse_refs:
            if "-" in ref:
                start = ref.split("-")[0]
                end = ref.split("-")[1]
                verses.extend([str(v) for v in range(int(start), int(end) + 1)])
            else:
                verses.append(ref)
        return chapter, verses

    def __import_psalms(self) -> None:
        """Populate Psalter.__psalms dictionary with psalms."""
        if os.path.isfile("src/pylect/psalter.json"):
            self.__load_from_json()
        else:
            raw_text = self.__get_psalter_from_pdf()
            clean_text = self.__clean_up_text(raw_text)
            self.__text_to_psalms(clean_text)
            self.__dump_to_json()

    def __load_from_json(self) -> None:
        """Load saved psalm dictionary"""
        with open("src/pylect/psalter.json", "r", encoding="utf-8") as json_file:
            self.__psalms = json.load(json_file)

    def __dump_to_json(self) -> None:
        """Save psalm dictionary as a JSON file"""
        with open("src/pylect/psalter.json", "w", encoding="utf-8") as json_file:
            json.dump(self.__psalms, json_file)

    def __get_psalter_from_pdf(self) -> str:
        """Extract plain text Psalter from PDF copy of the BCP"""
        doc = fitz.open("bcp_2019.pdf")
        text_list = []
        for page in doc.pages(279, 478):
            text = page.get_text()
            text_list.append(text)
        full_text = "\n".join(text_list)
        return full_text

    def __clean_up_text(self, text: str) -> str:
        """Remove extraneous formatting from the extracted Psalter text."""
        lines = text.splitlines()
        clean_lines = []
        for line in lines:
            clean_line = line.strip()
            clean_line = self.__remove_non_ascii(clean_line)
            clean_line = self.__remove_header_footer(clean_line)
            if clean_line:
                clean_lines.append(clean_line)
        clean_text = "\n".join(clean_lines)
        return clean_text

    def __remove_non_ascii(self, line: str) -> str:
        """Remove all non-ASCII characters from a string."""
        ascii_str = line.replace("’", "'")
        ascii_str = ascii_str.replace("‘", "'")
        return "".join(c if ord(c) < 128 else " " for c in ascii_str)

    def __remove_header_footer(self, line: str) -> str:
        """Remove headers, footers, and page numbers from Psalter text."""
        mp_header = re.compile(
            r".*(m\s*o\s*r\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*"
        )
        ep_header = re.compile(
            r".*(e\s*v\s*e\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*"
        )
        pg_footer = re.compile(r".*(t\s*h\s*e\s+p\s*s\s*a\s*l\s*t\s*e\s*r).*")
        pg_number = re.compile(r"[2-9]\d{2}")
        if (
            re.match(mp_header, line)
            or re.match(ep_header, line)
            or re.match(pg_footer, line)
            or re.match(pg_number, line)
        ):
            return ""
        return line

    def __text_to_psalms(self, text: str) -> None:
        """Process cleaned-up Psalter text into a dictionary of Psalm objects."""
        psalms = self.__split_psalms(text)
        for index, psalm in enumerate(psalms):
            ps_chapter = str(index + 1)
            if ps_chapter == "119":
                psalm = self.__remove_psalm_119_titles(psalm)
            ps_verses = self.__get_psalm_verses(psalm)
            self.__psalms[ps_chapter] = ps_verses

    def __split_psalms(self, text: str) -> list:
        """Split psalms into separate chapters."""
        ps_number = re.compile(r"\n*\d+\n")
        psalms = re.split(ps_number, text)
        while "" in psalms:
            psalms.remove("")
        del psalms[23]  # delete duplicate version of Psalm 23
        return psalms

    def __remove_psalm_119_titles(self, psalm: str) -> str:
        """Remove Hebrew and Latin titles throughout Psalm 119."""
        psalm_no_titles = psalm
        titles = [
            re.compile(r".*\nAleph\n"),
            re.compile(r".*\nBeth\n"),
            re.compile(r".*\nGimel\n"),
            re.compile(r".*\nDaleth\n"),
            re.compile(r".*\nHe\n"),
            re.compile(r".*\nWaw\n"),
            re.compile(r".*\nZayin\n"),
            re.compile(r".*\nHeth\n"),
            re.compile(r".*\nTeth\n"),
            re.compile(r".*\nYodh\n"),
            re.compile(r".*\nKaph\n"),
            re.compile(r".*\nLamedh\n"),
            re.compile(r".*\nMem\n"),
            re.compile(r".*\nNun\n"),
            re.compile(r".*\nSamekh\n"),
            re.compile(r".*\nAyin\n"),
            re.compile(r".*\nPe\n"),
            re.compile(r".*\nSadhe\n"),
            re.compile(r".*\nQoph\n"),
            re.compile(r".*\nResh\n"),
            re.compile(r".*\nShin\n"),
            re.compile(r".*\nTaw\n"),
        ]
        for title in titles:
            psalm_no_titles = re.sub(title, "", psalm_no_titles)
        return psalm_no_titles

    def __get_psalm_verses(self, psalm: str) -> dict:
        """Split psalms into separate verses and half-verses."""
        vs_number = re.compile(r"\d+")
        asterisk = re.compile(r"\s*\*\s*")
        verses = re.split(vs_number, psalm)
        if "*" not in verses[0]:
            del verses[0]  # remove title
        clean_verses = self.__clean_up_verses(verses)
        split_verses = {}
        for index, verse in enumerate(clean_verses):
            split_verse = re.split(asterisk, verse)
            split_verses[str(index + 1)] = {
                "head": split_verse[0],
                "tail": split_verse[1],
            }
        return split_verses

    def __clean_up_verses(self, verses: list) -> str:
        """Remove extraneous formatting within individual verses."""
        clean_verses = []
        for verse in verses:
            clean_verse = verse.strip()
            clean_verse = re.sub("\n", " ", clean_verse)
            clean_verses.append(clean_verse)
        while "" in clean_verses:
            clean_verses.remove("")
        return clean_verses
