from lectionary.psalter import Psalter


def main():
    psalter = Psalter()
    print(psalter.get_psalm("126 or 127"))
    print(psalter.get_psalm("119:1-4, 10"))


if __name__ == "__main__":
    main()
