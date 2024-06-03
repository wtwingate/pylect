# pylect

Pylect is a CLI program that searches the Sunday, Holy Day, and Commemoration Lectionary in the [Book of Common Prayer 2019](https://bcp2019.anglicanchurch.net/) for any upcoming holy days within a given date range and returns their corresponding Scripture lessons. When desired, it can then fetch the text of the Scripture lessons and automatically copy them to the system clipboard.

## Purpose

This is my first personal project! So, the purpose is to try my hand at making something from start to finish with nothing but my own inspiration to guide me. Practically speaking, the impetus for this project is the many hours I've spent creating bulletins and Scripture inserts for my local church. Calculating the correct day in the liturgical calendar, looking up the appropriate Scripture references in the lectionary, and then copying, pasting, and formatting the texts from different PDFs and websites has always been laborious and error-prone. This is my attempt to automate some of the boring stuff in my own life, and hopefully you find it useful too!

## Installation

Pylect is a program written in Python 3. If you don't already have Python installed, head over to the official Python [website](https://www.python.org/) and download the latest version.

Pylect is published on the [Python Package Index](https://pypi.org/project/pylect/), so the easiest way to install it is by simply running `pip install pylect` from the command line.

Next, you will need to get your own ESV API key from [here](https://api.esv.org/) if you want to be able to automatically fetch and copy the Scripture texts into your clipboard. Once you have the key, create a `.env` file in the root Pylect directory and add your key like so:

```
ESV_API_KEY=<your key goes here>
```

## Usage

Run Pylect from the command line with `python3 -m pylect <start_date> <end_date>` or (more simply) with `pylect <start_date> <end_date>`. The start and end dates are optional arguments and must be in the format `YYYY-MM-DD`. When not given any arguments, the program will take the current date as a starting point and return all the liturgical days in the coming week. The results will be printed to your screen. You can select any of the days by entering their corresponding number and Pylect will fetch the text of the lessons for you and copy them to your system clipboard. When you're finished, simply enter `q` to quit the program.

## Examples

With no optional arguments, Pylect will return all liturgical days ocurring over the next 7 days:

```
pylect
```

With the start date argument only, Pylect will return all liturgical days between June 8th and June 15th, 2024:

```
pylect 2024-06-08
```

With both the start and end date arguments, Pylect will return all liturgical days between June 8th and November 1st, 2024:

```
pylect 2024-06-08 2024-11-1
```

## Credits

- The Book of Common Prayer 2019 was produced by the Anglican Church of North America and is freely available for download at the [official website](https://bcp2019.anglicanchurch.net/).

- The JSON-ified text of the Psalms is pulled from the [Daily Office API](https://api.dailyoffice2019.com/api/) created by [Benjamin Locher](https://github.com/blocher). Much thanks to him for doing the hard work of wrangling the PDF text of the New Coverdale Psalter into a usable format!

## Contributing

I would like to develop this into a tool that can be used by multiple denominations with multiple lectionaries, so feedback and pull requests are more than welcome!
