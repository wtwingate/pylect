from lectionary.lectionary import Lectionary
from lectionary.psalter import Psalter
from lectionary.esv import get_esv_text


def main():
    psalter = Psalter()
    lectionary = Lectionary()
    lessons = lectionary.get_lessons("today")
    texts = []
    texts.append(get_esv_text(lessons[0]))  # The First Lesson
    texts.append(psalter.get_psalm(lessons[1]))  # The Psalm
    texts.append(get_esv_text(lessons[2]))  # The Second Lesson
    texts.append(get_esv_text(lessons[3]))  # The Gospel
    print("\n\n".join(texts))


if __name__ == "__main__":
    main()
