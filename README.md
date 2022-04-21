
# Python Sudoku Game

This repo contains a Python Sudoku Game for my university coursework.

As this game is written in Python, it requires the Python interpreter to be installed on your machine. ([Download Python](https://www.python.org/downloads/))

The game can be run by running the following command
`python src/app.py`

The game will then show you some instructions before letting you play Sudoku.

The game can be exited by selecting Option 5 or pressing Ctrl+C (Keyboard Interrupting).

All of the code for this game is contained within the `src` folder. There is a folder called `graveyard` that contains code that is not used in the final version of the game but was used in development attempts. This code has been kept commited for transparency.

## Glossary

Here is a glossary of terms used within the code and some explanations.

* Matrix Reference: a row index and column index to access a matrix at a given position
* Grid Reference: a human readable reference to a position on the sudoku board that used letters for the columns and numbers for the rows. Also used in the game Battleship
* Initial Sudoku Board: a version of a sudoku board without any changes made by a player
* Unedited Sudoku Board: see Initial Sudoku Bard
* Playing Sudoku Board: a version of a sudoku board with changes made by the player. The positions populated in the Initial Sudoku Board cannot be changed however.
* Solution Sudoku Board: a version of a sudoku board that is the target the player is aiming for.
