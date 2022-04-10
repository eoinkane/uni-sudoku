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
