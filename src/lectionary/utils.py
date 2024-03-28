import fitz


def get_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text_list = []
    for page in doc.pages(279, 478):
        text = page.get_text()
        text_list.append(text)
    full_text = "\n".join(text_list)
    return full_text
