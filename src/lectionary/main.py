from psalter import Psalter
from utils import get_text_from_pdf


def main():
    text = get_text_from_pdf("docs/bcp_2019.pdf")
    psalter = Psalter(text)
    print(psalter.get_psalm_text("126"))
    print(psalter.get_psalm_text("119", ["1", "2", "3", "4"]))


main()
