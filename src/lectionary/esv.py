import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["ESV_API_KEY"]
API_URL = "https://api.esv.org/v3/passage/text/"


def get_esv_text(query):
    params = {
        "q": query,
        "include-passage-references": True,
        "include-verse-numbers": True,
        "include-footnotes": False,
        "include-footnotes-body": False,
        "include-headings": False,
        "include-short-copyright": True,
    }
    headers = {"Authorization": f"Token {API_KEY}"}
    response = requests.get(API_URL, params=params, headers=headers)
    passages = response.json()["passages"]
    return passages[0].strip() if passages else "Error: passage not found"


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    if query:
        print(get_esv_text(query))
