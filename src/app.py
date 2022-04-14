import json
from datetime import datetime
from copy import deepcopy
from itertools import chain
from data.game1 import data
from typing import Dict, Tuple
from utils.custom_types import Board, Column_References, Generation, Flat_Board
from utils.screen import (
    clear_screen,
    print_sudoku_board,
    print_edit_and_original_sudoku_board,
    print_edit_and_original_sudoku_board_with_hints
)
from utils.board import (
    get_column_references,
    update_board,
    generate_allowed_values
)
from utils.user_input_helpers import (
    decide_action,
    select_position_value,
    select_hints_enabled,
    select_difficulty,
    select_grid_reference
)
from utils.enums import Action
from generators.board_generator import generate_board


def help():
    print(
        "To complete a game of Sudoku you must fill all "
        "the empty positions on the board with a number between 1 and 9."
    )
    print(
        "This Python Sudoku game represents the board using A1 notation, "
        "similar to Battleships."
    )
    print(
        "Dependening on the difficulty level you select, a varying amount of "
        "board positions will be pre-populated. "
        "These positions cannot be edited."
    )
    print(
        "However, there are rules about placing what "
        "numbers can be placed and where."
    )
    print(
        "To complete the game there can be no repeatition of numbers in any "
        "column, row or sub grid. If there is already a number 1 in position "
        "A1, then 1 cannot be repeated in row A and column 1 "
        "or the first sub grid."
    )
    print(
        "You can decide if you want to enable hints at the start of this game."
        " If hints are enabled and you enter an invalid number then a '?' will"
        "appear on the board next to that number, if hints are disabled "
        "then you will not be shown where your mistake is."
    )


def welcome():
    clear_screen()
    print("Welcome to the Python Sudoku Game")
    help()
    print("\nPress enter to continue")
    input()


def take_turn(
    unedited_full_board: Board,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    column_references: Column_References,
    hints_enabled: bool,
    hints: Dict[str, str]
) -> Tuple[Tuple[Board, Flat_Board], Dict[str, str]]:
    row_index: int = None
    col_index: int = None
    raw_grid_ref: str = None

    user_selected_a_editable_grid_ref = False
    while not user_selected_a_editable_grid_ref:
        (row_index, col_index), raw_grid_ref = select_grid_reference(
            column_references,
            board_size
        )
        if (unedited_full_board[row_index][col_index] == 0):
            user_selected_a_editable_grid_ref = True
        else:
            print("That grid ref is populated by the original board."
                  " Please see the board on the left and reselect a grid ref"
                  )
    position_value = select_position_value(
        raw_grid_ref,
        board_size,
    )

    if hints_enabled:
        hint_key = f"{row_index}{col_index}"
        allowed_values = generate_allowed_values(
            playing_full_board,
            row_index,
            col_index,
            board_size,
            {}
        )
        if (
            position_value != 0 and
            position_value not in allowed_values
           ):
            hints[hint_key] = "?"
        elif (
            (hint_key in hints and position_value == 0) or
            (hint_key in hints and position_value in allowed_values)
        ):
            del hints[hint_key]

    playing_full_board, playing_flat_board = update_board(
            playing_full_board,
            playing_flat_board,
            row_index,
            col_index,
            board_size,
            int(position_value)
        )
    return ((
        playing_full_board,
        playing_flat_board
        ),
        hints
    )


def complete_game(
    completed_board: Board,
    board_size: int,
    column_references: Column_References
):
    clear_screen()
    print("Congratulations, you completed the sudoku game! "
          "Here is the completed board")
    print_sudoku_board(
        completed_board,
        board_size,
        column_references,
        should_clear_screen=False
    )


def game(generation: Board, board_size: int, hints_enabled: bool):
    unedited_full_board: Board = deepcopy(generation["empty_full_board"])
    playing_full_board: Board = deepcopy(generation["empty_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))

    game_completed = False
    hints = {}

    column_references = get_column_references(unedited_full_board)

    print_board_func = (
        print_edit_and_original_sudoku_board if not hints_enabled
        else print_edit_and_original_sudoku_board_with_hints
    )

    while not game_completed:
        print_board_func(
            unedited_full_board,
            playing_full_board,
            board_size,
            column_references,
            hints=hints
        )
        action = decide_action()

        if (action == Action.TAKE_TURN):
            print_board_func(
                unedited_full_board,
                playing_full_board,
                board_size,
                column_references,
                hints=hints
            )
            (playing_full_board, playing_flat_board), hints = take_turn(
                unedited_full_board,
                playing_full_board,
                playing_flat_board,
                board_size,
                column_references,
                hints_enabled,
                hints
            )
        if (
            len([x for x in playing_flat_board if x == 0]) == 0 and
            playing_flat_board == generation["filled_flat_board"]
        ):
            game_completed = True
            complete_game(playing_full_board, board_size, column_references)


def main():
    board_size = 9
    welcome()
    difficulty = select_difficulty()
    hints_enabled = select_hints_enabled()
    generation: Generation = generate_board(board_size, difficulty)

    game(generation, board_size, hints_enabled)


if __name__ == "__main__":
    main()
