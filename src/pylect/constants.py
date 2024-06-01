from datetime import date

TODAY = date.today()

ADVENT_SUNDAYS: dict[int, str] = {
    0: "The First Sunday in Advent",
    7: "The Second Sunday in Advent",
    14: "The Third Sunday in Advent",
    21: "The Fourth Sunday in Advent",
}

EPIPHANY_SUNDAYS: dict[int, str] = {
    0: "The First Sunday of Epiphany: Baptism of Our Lord",
    7: "The Second Sunday of Epiphany",
    14: "The Third Sunday of Epiphany",
    21: "The Fourth Sunday of Epiphany",
    28: "The Fifth Sunday of Epiphany",
    35: "The Sixth Sunday of Epiphany",
    42: "The Seventh Sunday of Epiphany",
    49: "The Eighth Sunday of Epiphany",
}

LENT_SUNDAYS: dict[int, str] = {
    42: "The First Sunday in Lent",
    35: "The Second Sunday in Lent",
    28: "The Third Sunday in Lent",
    21: "The Fourth Sunday in Lent",
    14: "The Fifth Sunday in Lent: Passion Sunday",
}

HOLY_WEEK: dict[int, str] = {
    7: "Palm Sunday",
    6: "Monday in Holy Week",
    5: "Tuesday in Holy Week",
    4: "Wednesday in Holy Week",
    3: "Maundy Thursday",
    2: "Good Friday",
    1: "Holy Saturday",
}

EASTER_WEEK: dict[int, str] = {
    1: "Monday of Easter Week",
    2: "Tuesday of Easter Week",
    3: "Wednesday of Easter Week",
    4: "Thursday of Easter Week",
    5: "Friday of Easter Week",
    6: "Saturday of Easter Week",
}

EASTER_SUNDAYS: dict[int, str] = {
    7: "The Second Sunday of Easter",
    14: "The Third Sunday of Easter",
    21: "The Fourth Sunday of Easter: Good Shepherd",
    28: "The Fifth Sunday of Easter",
    35: "The Sixth Sunday of Easter: Rogation Sunday",
    42: "The Sunday after Ascension Day",
}

PENTECOST_SUNDAYS: dict[int, str] = {
    203: "Proper 1",
    196: "Proper 2",
    189: "Proper 3",
    182: "Proper 4",
    175: "Proper 5",
    168: "Proper 6",
    161: "Proper 7",
    154: "Proper 8",
    147: "Proper 9",
    140: "Proper 10",
    133: "Proper 11",
    126: "Proper 12",
    119: "Proper 13",
    112: "Proper 14",
    105: "Proper 15",
    98: "Proper 16",
    91: "Proper 17",
    84: "Proper 18",
    77: "Proper 19",
    70: "Proper 20",
    63: "Proper 21",
    56: "Proper 22",
    49: "Proper 23",
    42: "Proper 24",
    35: "Proper 25",
    28: "Proper 26",
    21: "Proper 27",
    14: "Proper 28",
    7: "Proper 29: Christ the King",
}


RED_LETTER_DAYS: dict[date, str] = {
    date(
        TODAY.year, 1, 1
    ): "The Circumcision and Holy Name of Our Lord Jesus Christ",
    date(TODAY.year, 1, 18): "Confession of Peter the Apostle",
    date(TODAY.year, 1, 25): "Conversion of Paul the Apostle",
    date(
        TODAY.year, 2, 2
    ): "The Presentation of Our Lord Jesus Christ in the Temple",
    date(TODAY.year, 2, 24): "Matthias the Apostle",
    date(
        TODAY.year, 3, 19
    ): "Joseph, Husband of the Virgin Mary and Guardian of Jesus",
    date(
        TODAY.year, 3, 25
    ): "The Annunciation of our Lord Jesus Christ to the Virgin Mary",
    date(TODAY.year, 4, 25): "Mark the Evangelist",
    date(TODAY.year, 5, 1): "Philip and James, Apostles",
    date(
        TODAY.year, 5, 31
    ): "The Visitation of the Virgin Mary to Elizabeth and Zechariah",
    date(TODAY.year, 6, 11): "Barnabas the Apostle",
    date(TODAY.year, 6, 24): "The Nativity of John the Baptist",
    date(TODAY.year, 6, 29): "Peter and Paul, Apostles",
    date(TODAY.year, 7, 22): "Mary Magdalene",
    date(TODAY.year, 7, 25): "James the Elder, Apostle",
    date(TODAY.year, 8, 6): "The Transfiguration of Our Lord Jesus Christ",
    date(
        TODAY.year, 8, 15
    ): "The Virgin Mary, Mother of Our Lord Jesus Christ",
    date(TODAY.year, 8, 24): "Bartholomew the Apostle",
    date(TODAY.year, 9, 14): "Holy Cross Day",
    date(TODAY.year, 9, 21): "Matthew, Apostle and Evangelist",
    date(TODAY.year, 9, 29): "Holy Michael and All Angels",
    date(TODAY.year, 10, 18): "Luke the Evangelist and Companion of Paul",
    date(
        TODAY.year, 10, 23
    ): "James of Jerusalem, Bishop and Martyr, Brother of Our Lord",
    date(TODAY.year, 10, 28): "Simon and Jude, Apostles",
    date(TODAY.year, 11, 30): "Andrew the Apostle",
    date(TODAY.year, 12, 21): "Thomas the Apostle",
    date(TODAY.year, 12, 26): "Stephen, Deacon and Martyr",
    date(TODAY.year, 12, 27): "John, Apostle and Evangelist",
    date(TODAY.year, 12, 28): "The Holy Innocents",
}
