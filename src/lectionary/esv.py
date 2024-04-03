import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()
"""Load API Key from environment variables"""
API_KEY = os.environ["ESV_API_KEY"]
API_URL = "https://api.esv.org/v3/passage/text/"


def get_esv_text(query):
    """Call the ESV API to get Scripture texts"""
    params = {
        "q": query,
        "include-passage-references": True,
        "include-verse-numbers": True,
        "include-footnotes": False,
        "include-footnotes-body": False,
        "include-headings": False,
        "include-short-copyright": True,
        "indent-paragraphs": 0,
        "indent-poetry": False,
    }
    headers = {"Authorization": f"Token {API_KEY}"}
    response = requests.get(API_URL, params=params, headers=headers)
    passages = response.json()["passages"]
    if passages:
        text = passages[0].strip()
        text = text.replace("\n\n\n", "\n\n")
        text = text.replace("[", "")
        text = text.replace("]", "")
        return text
    else:
        raise Exception("Error: passage not found")


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    if query:
        print(get_esv_text(query))
