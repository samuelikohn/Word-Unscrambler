# The Untitled Word Game

## About

This is a word unscramble game. Given a collection of letters, the goal is find as many English words as you can using those letters in the alloted time. The Merriam-Webster Scrabble dictionary is used reference for what sequences of letters count as words.

When enough words have been found, the level is completed, the game advances, and a new collection of letters is chosen.

## Difficulty Buffs

As you progress through multiple levels, restrictions are added to increase the difficulty of the game.

- The alloted time per level will decrease
- The minimum length of accepted words will increase
- Letters will be hidden and replaced by a `?`
- Fake letters that are not used in any word are added

In the game settings, you can adjust the starting values for each type of difficulty buff, how often buffs are applied, and the percentage of words required to pass each level to suit your preferences.

## How to Run

- You must have Python 3 installed to run.
- Make sure to also install the dependencies from `requirements.txt`.
- Run `full\path\to\your\python\executable` `full\path\to\main.py` from the command line.
- If the location of your Python executable is registered as an evironment variable on your system, you can replace `full\path\to\your\python\executable` with either `python` or `python3`, whichever alias is accepted on your system.
- Additionally, you can supply the location of `main.py` with relative paths. For example, if you run the command from the same folder as `main.py,` you can replace `full\path\to\main.py` with `main.py`.

## Adding your own levels

- In `generate_levels.py`, add your words as comma-separated strings inside the `words` list.
- Run the file the same as above, but replace `main.py` with `generate_levels.py`.