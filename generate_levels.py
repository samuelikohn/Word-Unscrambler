from requests import get
from bs4 import BeautifulSoup
from json import dump
from os import path

words = [
    # Put your words here
]

for word in words:
    url = f"https://scrabble.merriam.com/finder/{word}"
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    res = []
    tags = soup.find('div', class_='sbl_word_groups').find_all('a')

    for tag in tags:
        text_value = tag.get_text(strip=True)
        if len(text_value) >= 4: # Global min length is 4
            res.append(text_value)

    # Enforce pangram rule
    if word not in res:
        print(f"\"{word}\" not found in dictionary, no level was created.")
        continue

    letters = [letter.upper() for letter in word]
    data = {
        "letters": letters,
        "words": res
    }

    with open(f"{path.dirname(path.abspath(__file__))}/levels/{word}.json", "w") as f:
        dump(data, f, indent=4)
    print(f"Level file for \"{word}\" successfully created.")