from requests import get
from json import dump
from os import path

words = [
    # Put your words here
]

for word in words:

    all_words = []
    for i in range(4, len(word) + 1):
        url = f"https://scrabble.merriam.com/lapi/1/sbl_finder/get_limited_data?mode=wfd&type=search&rack={word}&len={i}"
        response = get(url)
        all_words.extend(response.json()["data"])

    # Enforce pangram rule
    if word not in all_words:
        print(f"\"{word}\" not found in dictionary, no level was created.")
        continue

    letters = [letter.upper() for letter in word]
    data = {
        "letters": letters,
        "words": all_words
    }

    with open(f"{path.dirname(path.abspath(__file__))}/levels/{word}.json", "w") as f:
        dump(data, f, indent=4)
    print(f"Level file for \"{word}\" successfully created.")