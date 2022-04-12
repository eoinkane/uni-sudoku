import json
from copy import deepcopy
from itertools import chain
from data.game1 import data
from typing import Dict, Tuple, Union
from utils.custom_types import Board, Column_References, Generation, Flat_Board
from utils.screen import (
    clear_screen,
    print_sudoku_board,
    print_edit_and_original_sudoku_board
)
from utils.board import get_column_references, update_board
from utils.enums import Difficulty, Action
from generators.board_generator import generate_board


def validate_grid_reference_input(
      raw_grid_reference: str,
        column_references: Column_References) -> bool:
    return (
        len(raw_grid_reference) == 2 and
        raw_grid_reference[0].lower().isalpha() and
        raw_grid_reference[1].isdigit() and
        raw_grid_reference[0].upper() in column_references
    )


def convert_grid_reference_to_matrix_reference(grid_reference: str):
    return (ord(grid_reference[0].lower()) - 97, (int(grid_reference[1]) - 1))


def select_grid_reference(column_references: Column_References
                          ) -> Tuple[Tuple[int, int], str]:
    print("Please input the A1 grid reference you would like to select "
          "and then press enter")
    recieved_grid_reference = False
    while not recieved_grid_reference:
        raw_grid_reference = input()
        if (validate_grid_reference_input(
            raw_grid_reference,
            column_references
                )):
            recieved_grid_reference = True
            # return convert_grid_reference_to_matrix_reference(
            #     raw_grid_reference
            #     ), raw_grid_reference
        else:
            print(f"'{raw_grid_reference}' is not a valid A1 grid " +
                  "reference. You can use the column and row values " +
                  "displayed above. Please try again.")
    return convert_grid_reference_to_matrix_reference(
            raw_grid_reference
            ), raw_grid_reference


def select_difficulty() -> Difficulty:
    print("Please select a difficulty level: \n"
          + " \n".join([f"{difficulty.value} - {difficulty.name}" for difficulty in Difficulty]))
    print("Please input the number next to the difficulty you would like "
          "to select and then press enter")
    recieved_difficulty = False
    while not recieved_difficulty:
        raw_difficulty = input()
        if (
            raw_difficulty.isdigit() and
            int(raw_difficulty)
            in [difficulty.value for difficulty in Difficulty]
        ):
            recieved_difficulty = True
            # return Difficulty(int(raw_difficulty))
        else:
            print(f"'{raw_difficulty}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return Difficulty(int(raw_difficulty))


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
        "However, there are rules about placing what "
        "numbers can be placed and where."
    )
    print(
        "There can be no repeatition of numbers in any column, row or sub "
        "grid. If there is already a number 1 in position A1, then 1 cannot "
        "be repeated in row A and column 1 or the first sub grid."
    )


def welcome():
    clear_screen()
    print("Welcome to the Python Sudoku Game")
    help()
    print("\nPress enter to continue")
    input()


def change_position_value(
        selected_position_row_index: int,
        selected_position_col_index: int,
        raw_grid_ref: str,
        board_size: int,
        playing_full_board: Board,
        playing_flat_board: Flat_Board):
    print(f"Please input the number you would like to enter at {raw_grid_ref} "
          f"between 1 and {board_size} and then press enter"
          )
    recieved_number = False
    while not recieved_number:
        raw_number = input()
        if (
            len(raw_number) == 1 and
            raw_number[0].isdigit() and
            int(raw_number[0]) in [x for x in range(0, (board_size + 1))]
        ):
            recieved_number = True
        else:
            print(
                f"{raw_number} is not a valid input. "
                f"Please enter a number between 1 and {board_size}"
            )
    return update_board(
            playing_full_board,
            playing_flat_board,
            selected_position_row_index,
            selected_position_col_index,
            board_size,
            int(raw_number)
        )
    # quit()
    # pass


def take_turn(
    unedited_full_board: Board,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    column_references: Column_References
) -> Dict[str, Union[Board, Flat_Board]]:
    # print_edit_and_original_sudoku_board(
    #         unedited_full_board,
    #         playing_full_board,
    #         board_size,
    #         column_references
    #         )
    # print_sudoku_board(empty_full_board, column_references)
    row_index: int = None
    col_index: int = None
    raw_grid_ref: str = None

    user_selected_a_editable_grid_ref = False
    while not user_selected_a_editable_grid_ref:
        (row_index, col_index), raw_grid_ref = select_grid_reference(
            column_references
        )
        if (unedited_full_board[row_index][col_index] == 0):
            user_selected_a_editable_grid_ref = True
        else:
            print("That grid ref is populated by the original board. Please see the board on the left and reselect a grid ref")
    # print(f"selected {empty_full_board[row_index][col_index]}")
    playing_full_board, playing_flat_board = change_position_value(
        row_index,
        col_index,
        raw_grid_ref,
        board_size,
        playing_full_board,
        playing_flat_board
    )
    return (
        # "unedited_full_board": unedited_full_board,
        playing_full_board,
        playing_flat_board
    )


def decide_action() -> Action:
    print("\nPlease select the next action you would like to take: \n"
          + " \n".join(
              [f"{action.value} - {action.name}" for action in Action]
            )
          )
    print("Please input the number next to the difficulty you would like "
          "to select and then press enter")
    recieved_action = False
    while not recieved_action:
        raw_action = input()
        if (
            raw_action.isdigit() and
            int(raw_action)
            in [action.value for action in Action]
        ):
            recieved_action = True
        else:
            print(f"'{raw_action}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return Action(int(raw_action))


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


def game(generation: Board, board_size: int):
    # solution_full_board: Board = deepcopy(generation["filled_full_board"])
    unedited_full_board: Board = deepcopy(generation["empty_full_board"])
    playing_full_board: Board = deepcopy(generation["empty_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))

    game_completed = False

    column_references = get_column_references(unedited_full_board)

    while not game_completed:
        print_edit_and_original_sudoku_board(
            unedited_full_board,
            playing_full_board,
            board_size,
            column_references
        )
        action = decide_action()

        if (action == Action.TAKE_TURN):
            print_edit_and_original_sudoku_board(
                unedited_full_board,
                playing_full_board,
                board_size,
                column_references
            )
            playing_full_board, playing_flat_board = take_turn(
                unedited_full_board,
                playing_full_board,
                playing_flat_board,
                board_size,
                column_references
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
    generation: Generation = generate_board(board_size, difficulty)

    game(generation, board_size)


if __name__ == "__main__":
    main()
