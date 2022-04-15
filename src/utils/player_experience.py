from utils.user_input_helpers import (
    select_hints_enabled
)
from utils.screen import (
    clear_screen
)
from save_handlers.save_handlers import (
    get_datetime_from_save_file_name,
    get_difficulty_from_save_file_name
)
from utils.time import format_datetime_to_string
from utils.board import (
    convert_matrix_reference_to_grid_reference
)


def welcome():
    clear_screen()
    print("Welcome to the Python Sudoku Game")
    display_help_message()
    print("\nPress enter to continue")
    input()


def show_help(hints_enabled) -> bool:
    hints_enabled_str = (
        f"\033[1m{('enabled' if hints_enabled else 'disabled')}\033[0m"
    )

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


def display_undo_turn_message(turn_no, turn):
    grid_ref = convert_matrix_reference_to_grid_reference(
        turn["row_index"],
        turn["col_index"]
    )
    modification_str = (
        f"changing {grid_ref} from "
        f"{turn['new_value']} to {turn['previous_value']}"
    ) if turn["previous_value"] != 0 else (
        f"emptying {grid_ref}"
    )
    print(
        f"\nUndoing turn {turn_no + 1}, "
        + modification_str +
        "\nPlease press enter to continue"
    )
    input()


def display_unable_to_undo_turn_message():
    print(
        "\nNo turns can be undone. The Original Board is identical to "
        "the Playing Board. First, take a turn, then you can undo."
        "\nPlease press enter to continue"
    )
    input()
