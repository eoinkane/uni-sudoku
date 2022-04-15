from copy import deepcopy
from itertools import chain
from data.game1 import data
from utils.game import (
    create_game_config,
    take_turn
)
from utils.custom_types import (
    Board,
    Column_References,
    Generation,
    Flat_Board,
)
from utils.screen import (
    clear_screen,
    print_sudoku_board,
    print_edit_and_original_sudoku_board,
    print_edit_and_original_sudoku_board_with_hints
)
from utils.board import (
    get_column_references
)
from utils.user_input_helpers import (
    decide_action,
)
from utils.enums import Action
from save_handlers.save_handlers import (
    complete_save,
    update_save,
)


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


def game(
    generation: Generation,
    board_size: int,
    hints_enabled: bool,
    save_file_name: str
):
    unedited_full_board: Board = deepcopy(generation["initial_full_board"])
    playing_full_board: Board = deepcopy(generation["playing_full_board"])
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
        update_save(
            save_file_name,
            playing_full_board,
            hints_enabled,
            hints
        )
        if (
            len([x for x in playing_flat_board if x == 0]) == 0 and
            playing_flat_board == generation["solution_flat_board"]
        ):
            game_completed = True
            complete_save(save_file_name)
            complete_game(playing_full_board, board_size, column_references)


def main():
    board_size = 9
    welcome()

    generation, (hints_enabled, save_file_name) = (
        create_game_config(board_size)
    )

    game(generation, board_size, hints_enabled, save_file_name)


if __name__ == "__main__":
    main()
