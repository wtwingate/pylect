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

    def __remove_non_ascii(line: str) -> str:
        """Remove all non-ASCII characters from a string"""
        return "".join(c if ord(c) < 128 else " " for c in line)

    def __remove_header_footer(line: str) -> str:
        """Remove headers, footers, and page numbers from Psalter text"""
        mp_header = re.compile(
            r".*(m\s*o\s*r\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*"
        )
        ep_header = re.compile(
            r".*(e\s*v\s*e\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*"
        )
        pg_footer = re.compile(r".*(t\s*h\s*e\s+p\s*s\s*a\s*l\s*t\s*e\s*r).*")
        pg_number = re.compile(
            r".*(15[1-9]|16[1-9]|17[1-9]|18[1-9]|19[1-9]|[2-9]\d{2}).*"
        )
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
            ps_number = self.__get_psalm_number(psalm)
            ps_title = self.__get_psalm_title(psalm)
            ps_verses = self.__get_psalm_verses(psalm)
            self.__psalms[str(index + 1)] = Psalm(ps_number, ps_title, ps_verses)

    def __split_psalms(self) -> list:
        ps_number = re.compile(r"\n\d+\n")
        psalms = re.split(ps_number, self.__text)
        del psalms[23]  # delete duplicate version of Psalm 23
        return psalms

    def __get_psalm_number(self, psalm: str) -> str:
        pass

    def __get_psalm_title(self, psalm: str) -> str:
        pass

    def __get_psalm_verses(self, psalm: str) -> dict:
        pass


class Psalm:
    def __init__(self, number: int, title: str, verses: dict) -> None:
        self.__number = number
        self.__title = title
        self.__verses = verses


def split_verses(text):
    vs_number = re.compile(r"\d+")
    verses = re.split(vs_number, text)
    return verses


def clean_up_verses(verse_list):
    clean_verses = []
    for verse in verse_list:
        clean_verse = verse.strip()
        clean_verse = re.sub("\n", " ", clean_verse)
        clean_verses.append(clean_verse)
    while "" in clean_verses:
        clean_verses.remove("")
    return clean_verses


def split_half_verse(verse):
    asterisk = re.compile(r"\s*\*\s*")
    half_verses = re.split(asterisk, verse)
    return half_verses


def write_to_files(psalm_list):
    for index, psalm in enumerate(psalm_list):
        f = open(f"src/psalter/psalm_{index + 1}.txt", "w")
        f.write(psalm)
        f.close()
