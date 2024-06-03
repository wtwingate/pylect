"""Provides a function for calling the ESV Bible API to get the text of any
Scripture lessons provided by the lectionary.
"""

import os

import requests
from dotenv import load_dotenv

# The ESV API key is located in the .env file in the project's root directory.
# This function from the dotenv module adds it as an environment variable that
# we can reference below.
load_dotenv()

API_KEY = os.environ["ESV_API_KEY"]
API_URL = "https://api.esv.org/v3/passage/text/"


def get_esv_text(query):
    """Call the ESV API to get Scripture texts."""
    params = {
        "q": query,
        "include-passage-references": True,
        "include-verse-numbers": True,
        "include-footnotes": False,
        "include-footnotes-body": False,
        "include-headings": False,
        "include-short-copyright": False,
        "indent-paragraphs": 0,
        "indent-poetry": True,
    }
    headers = {"Authorization": f"Token {API_KEY}"}
    response = requests.get(
        API_URL, params=params, headers=headers, timeout=10
    )
    passages = response.json()["passages"]
    if passages:
        text = "\n".join([passage.strip() for passage in passages])
        text = text.replace("[", "").replace("]", "")
        return text
    raise ValueError("Error: passage not found")
