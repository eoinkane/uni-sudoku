import platform
import os
from .custom_types import Board, Column_References


def clear_screen():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    print()


def print_sudoku_board(board: Board, column_references: Column_References):
    clear_screen()
    print("      " + "   ".join([str(x + 1) for x in range(len(board))]))
    print("    _____________________________________")
    for row_index, row in enumerate(board):
        print(f"{column_references[row_index]} - | " +
              f"{' | '.join(str(item) for item in row).replace('0', ' ')} |"
              )
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


def print_edit_and_original_sudoku_board(
        unedited_board: Board,
        playing_board: Board,
        board_size: int,
        column_references: Column_References
        ):
    clear_screen()

    column_keys = "   ".join([str(x) for x in range(1, (board_size + 1))])

    top_line = "_" + "____" * board_size
    bottom_line = "¯" + "¯¯¯¯" * board_size
    print("      " + "Original Board" + ("    " + "   " * board_size) + "Playing Board")
    print("      " + column_keys + "            " + column_keys)
    print("    " + top_line + "        " + top_line)
    for row_index in range(board_size):
        unedited_row = unedited_board[row_index]
        playing_row = playing_board[row_index]

        row_key = f"{column_references[row_index]} - | "

        print(row_key +
              f"{' | '.join(str(item) for item in unedited_row).replace('0', ' ')} |"
              "    " +
              row_key +
              f"{' | '.join(str(item) for item in playing_row).replace('0', ' ')} |"
              )
    print("    " + bottom_line + "        " + bottom_line)
