import csv


class Lectionary:
    def __init__(self) -> None:
        self.__lectionary = {}
        self.__import_lectionary()

    def get_readings(self, day, year):
        return self.__lectionary[day][year]

    def __import_lectionary(self):
        self.__get_lectionary_from_csv()

    def __get_lectionary_from_csv(self):
        """Extract lectionary table from CSV file"""
        with open("docs/sunday_lectionary.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.__lectionary[row["DAY"]] = {
                    "YEAR A": row["YEAR A"],
                    "YEAR B": row["YEAR B"],
                    "YEAR C": row["YEAR C"],
                }


if __name__ == "__main__":
    lectionary = Lectionary()
    print(lectionary.get_readings("PROPER 5", "YEAR A"))
