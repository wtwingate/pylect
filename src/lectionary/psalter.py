from constants import HEBREW_TITLES
import re


class Psalter:
    """The Psalter class is responsible for taking in the raw text of the
    Psalter that has been extracted from a PDF copy of the Book of Common Prayer
    2019, cleaning up the text (by removing unnecessary formatting), and then
    creating a dictionary of Psalm objects. This dictionary can then be exported
    to a JSON file for use in the rest of the program.
    """

    def __init__(self, text: str) -> None:
        self.__text = self.__clean_up_text(text)
        self.__psalms = {}
        self.__text_to_psalms()

    def get_psalm_text(self, chapter: str, verses: list | None = None) -> str:
        text_list = []
        psalm = self.__psalms.get(chapter)
        if psalm is None:
            raise ValueError("Error: invalid chapter reference")
        text_list.append(psalm.chapter)
        if verses is None:
            verses = psalm.verses.keys()
        for verse in verses:
            psalm_verse = psalm.verses.get(verse)
            if psalm_verse is not None:
                text_list.append(f"{verse} {psalm_verse["head"]} *")
                text_list.append(f"{psalm_verse["tail"]}")
        psalm_text = "\n".join(text_list)
        return psalm_text

    def __clean_up_text(self, text: str) -> str:
        """Remove extraneous formatting from the extracted Psalter text"""
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
        """Remove all non-ASCII characters from a string"""
        return "".join(c if ord(c) < 128 else " " for c in line)

    def __remove_header_footer(self, line: str) -> str:
        """Remove headers, footers, and page numbers from Psalter text"""
        mp_header = re.compile(
            r".*(m\s*o\s*r\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*"
        )
        ep_header = re.compile(
            r".*(e\s*v\s*e\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*"
        )
        pg_footer = re.compile(r".*(t\s*h\s*e\s+p\s*s\s*a\s*l\s*t\s*e\s*r).*")
        pg_number = re.compile( r"[2-9]\d{2}")
        if (
            re.match(mp_header, line)
            or re.match(ep_header, line)
            or re.match(pg_footer, line)
            or re.match(pg_number, line)
        ):
            return ""
        return line

    def __text_to_psalms(self) -> None:
        """Process cleaned-up Psalter text into a dictionary of Psalm objects"""
        psalms = self.__split_psalms()
        for index, psalm in enumerate(psalms):
            ps_chapter = str(index + 1)
            if ps_chapter == "119":
                psalm = self.__remove_psalm_119_titles(psalm)
            ps_verses = self.__get_psalm_verses(psalm)
            self.__psalms[ps_chapter] = Psalm(ps_chapter, ps_verses)

    def __split_psalms(self) -> list:
        ps_number = re.compile(r"\n*\d+\n")
        psalms = re.split(ps_number, self.__text)
        while "" in psalms:
            psalms.remove("")
        del psalms[23]  # delete duplicate version of Psalm 23
        return psalms

    def __get_psalm_verses(self, psalm: str) -> dict:
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
    
    def __remove_psalm_119_titles(self, psalm: str):
        psalm_no_title = psalm
        for title in HEBREW_TITLES:
            psalm_no_title = re.sub(title, "", psalm_no_title)
        return psalm_no_title

    def __clean_up_verses(self, verses: list) -> str:
        clean_verses = []
        for verse in verses:
            clean_verse = verse.strip()
            clean_verse = re.sub("\n", " ", clean_verse)
            clean_verses.append(clean_verse)
        while "" in clean_verses:
            clean_verses.remove("")
        return clean_verses


class Psalm:
    def __init__(self, chapter: str, verses: dict) -> None:
        self.chapter = chapter
        self.verses = verses
