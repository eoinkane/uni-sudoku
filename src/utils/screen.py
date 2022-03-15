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
    print("      " + "   ".join(column_references))
    print("    _____________________________________")
    for row_index, row in enumerate(board):
        print(f"{row_index + 1} - | " +
              f"{' | '.join(str(item) for item in row).replace('0', ' ')} |"
              )
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
