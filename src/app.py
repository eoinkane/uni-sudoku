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
    Hints
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
    get_datetime_from_save_file_name,
    get_difficulty_from_save_file_name
)
from utils.time import format_datetime_to_string
from utils.user_input_helpers import (
    select_hints_enabled
)


def display_help_message():
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
    display_help_message()
    print("\nPress enter to continue")
    input()


def display_quit_message(save_file_name: str):
    game_difficulty_level_str = get_difficulty_from_save_file_name(
        save_file_name
    ).name
    game_created_time_str = format_datetime_to_string(
            get_datetime_from_save_file_name(save_file_name)
        )
    print(
        "\nThis Python Sudoku Game will now close. "
        "Your game is saved and can be continued at any time. "
        "\nSaved Games can be selected by their "
        "Difficulty and Created time. \n"
        f"\n * Your difficulty level was: {game_difficulty_level_str} "
        f"\n * Your game was created on: {game_created_time_str}"
    )


def show_help(hints_enabled) -> bool:
    hints_enabled_str = "enabled" if hints_enabled else "disabled"

    clear_screen()
    display_help_message()
    print(
        f"\nHints are {hints_enabled_str} for this game."
        "\nYou can now change if hints should be enabled"
    )
    hints_enabled = select_hints_enabled()

    print(
        "\nPress enter to continue"
        )
    input()
    return hints_enabled


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


def assign_print_board_func(hints_enabled):
    return (
        print_edit_and_original_sudoku_board if not hints_enabled
        else print_edit_and_original_sudoku_board_with_hints
    )


def game(
    generation: Generation,
    board_size: int,
    hints_enabled: bool,
    save_file_name: str,
    hints: Hints
):
    unedited_full_board: Board = deepcopy(generation["initial_full_board"])
    playing_full_board: Board = deepcopy(generation["playing_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))

    game_completed = False

    column_references = get_column_references(unedited_full_board)

    print_board_func = assign_print_board_func(hints_enabled)

    while not game_completed:
        print(hints)
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
        elif (action == Action.SHOW_HELP):
            new_hints_enabled = show_help(hints_enabled)
            if (new_hints_enabled != hints_enabled):
                print_board_func = assign_print_board_func(new_hints_enabled)
                hints_enabled = new_hints_enabled
        elif (action == Action.QUIT):
            return display_quit_message(save_file_name)

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

    generation, (save_file_name, (hints_enabled, hints)) = (
        create_game_config(board_size)
    )

    game(generation, board_size, hints_enabled, save_file_name, hints)


if __name__ == "__main__":
    main()
