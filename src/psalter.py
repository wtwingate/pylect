import fitz
import re


def psalter_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text_list = []
    for page in doc.pages(279, 478):
        text = page.get_text()
        text_list.append(text)
    full_text = "\n".join(text_list)
    clean_text = clean_up_text(full_text)
    psalm_list = split_psalms(clean_text)
    write_to_files(psalm_list)


def clean_up_text(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        clean_line = line.strip()
        clean_line = remove_header_footer(clean_line)
        clean_line = remove_page_number(clean_line)
        clean_line = remove_non_ascii(clean_line)
        clean_lines.append(clean_line)
    while "" in clean_lines:
        clean_lines.remove("")
    while " " in clean_lines:
        clean_lines.remove(" ")
    clean_text = "\n".join(clean_lines)
    return clean_text


def remove_header_footer(line):
    mp_header = re.compile(r".*(m\s*o\s*r\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*")
    ep_header = re.compile(r".*(e\s*v\s*e\s*n\s*i\s*n\s*g\s+p\s*r\s*a\s*y\s*e\s*r).*")
    ps_footer = re.compile(r".*(t\s*h\s*e\s+p\s*s\s*a\s*l\s*t\s*e\s*r).*")

    if (
        re.match(mp_header, line)
        or re.match(ep_header, line)
        or re.match(ps_footer, line)
    ):
        return ""
    return line


def remove_page_number(line):
    pg_number = re.compile(r".*(15[1-9]|16[1-9]|17[1-9]|18[1-9]|19[1-9]|[2-9]\d{2}).*")

    if re.match(pg_number, line):
        return ""
    return line


def remove_non_ascii(line):
    return "".join(c if ord(c) < 128 else " " for c in line)


def split_psalms(text):
    ps_number = re.compile(r"\n\d+\n")
    psalms = re.split(ps_number, text)
    del psalms[23]  # delete duplicate version of Psalm 23
    return psalms


def write_to_files(psalm_list):
    for index, psalm in enumerate(psalm_list):
        f = open(f"src/psalter/psalm_{index + 1}.txt", "w")
        f.write(psalm)
        f.close()


if __name__ == "__main__":
    psalter_from_pdf("bcp_2019.pdf")
