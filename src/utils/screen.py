import platform
import os
from .custom_types import Board, Column_References


def clear_screen():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    print()


def print_sudoku_board(
    board: Board,
    board_size: int,
    column_references: Column_References,
    **kwargs
):
    should_clear_screen = kwargs.get(
        "should_clear_screen",
        True
    )
    time_elasped_str = kwargs.get(
        "time_elasped_str",
        None
    )
    if should_clear_screen:
        clear_screen()

    column_keys = "   ".join([str(x) for x in range(1, (board_size + 1))])

    top_line = "_" + "____" * board_size
    bottom_line = "¯" + "¯¯¯¯" * board_size

    print("      " + column_keys)
    print("    " + top_line)
    for row_index in range(board_size):
        row = board[row_index]
        row_key = f"{column_references[row_index]} - | "

        print(row_key +
              f"{' | '.join(str(item) for item in row).replace('0', ' ')} |")
    print("    " + bottom_line)
    if (time_elasped_str):
        print(f"Time Elasped Since the Start of the Game: {time_elasped_str}")


def print_edit_and_original_sudoku_board(
        unedited_board: Board,
        playing_board: Board,
        board_size: int,
        column_references: Column_References,
        **kwargs
):
    should_clear_screen = kwargs.get(
        "should_clear_screen",
        True
    )
    time_elasped_str = kwargs.get(
        "time_elasped_str",
        None
    )
    if should_clear_screen:
        clear_screen()

    column_keys = "   ".join([str(x) for x in range(1, (board_size + 1))])

    top_line = "_" + "____" * board_size
    bottom_line = "¯" + "¯¯¯¯" * board_size
    print(
        "      " + "Original Board" +
        ("    " + "   " * board_size) +
        "Playing Board"
         )
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
    if (time_elasped_str):
        print(f"Time Elasped Since the Start of the Game: {time_elasped_str}")


def print_edit_and_original_sudoku_board_with_hints(
    unedited_board: Board,
    playing_board: Board,
    board_size: int,
    column_references: Column_References,
    **kwargs
):
    hints = kwargs.get("hints", {})
    should_clear_screen = kwargs.get(
        "should_clear_screen",
        True
    )
    time_elasped_str = kwargs.get(
        "time_elasped_str",
        None
    )
    if should_clear_screen:
        clear_screen()

    column_keys = "   ".join([str(x) for x in range(1, (board_size + 1))])

    top_line = "_" + "____" * board_size
    bottom_line = "¯" + "¯¯¯¯" * board_size

    print(
        "      " + "Original Board" +
        ("    " + "   " * board_size) +
        "Playing Board"
         )
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
              f"{'| '.join(str(item) + hints.get((str(row_index) + str(col_index)), ' ') for col_index, item in enumerate(playing_row)).replace('0', ' ')}|"
              )
    print("    " + bottom_line + "        " + bottom_line)
    if (time_elasped_str):
        print(f"Time Elasped Since the Start of the Game: {time_elasped_str}")
