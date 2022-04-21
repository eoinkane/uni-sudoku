from typing import Tuple
from utils.user_input_helpers import (
    select_hints_enabled,
    select_stats_enabled
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
from utils.custom_types import Turn


def welcome():
    """a helper function to display a welcome message"""
    clear_screen()
    print("Welcome to the Python Sudoku Game")
    display_help_message()
    print("\nPress enter to continue")
    input()


def show_help(hints_enabled: bool, stats_enabled: bool) -> Tuple[bool, bool]:
    """a helper function to display the help screen

    Args:
        hints_enabled (bool): _description_
        stats_enabled (bool): _description_

    Returns:
        Tuple[bool, bool]: the updated hints enabled and stats enabled
    """
    # create string with bold text
    hints_enabled_str = (
        f"\033[1m{('enabled' if hints_enabled else 'disabled')}\033[0m"
    )
    stats_enabled_str = (
        f"\033[1m{('enabled' if stats_enabled else 'disabled')}\033[0m"
    )

    clear_screen()
    display_help_message()
    # allow the user to reselect whether hints should be enabled
    print(
        f"\nHints are {hints_enabled_str} for this game."
        "\nYou can now change if hints should be enabled"
    )
    hints_enabled = select_hints_enabled()

    # allow the user to reselect whether stats should be enabled
    print(
        f"Stats are {stats_enabled_str} for this game."
        "\nYou can now change if stats should be enabled"
    )
    stats_enabled = select_stats_enabled()

    print(
        "\nPress enter to continue"
        )
    input()
    return (hints_enabled, stats_enabled)


def display_help_message():
    """a helper function to display a help message"""
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
    """a helper function to display a welcome message

    Args:
        save_file_name (str): the saved game file name
    """
    # get the difficulty and created time of current game
    game_difficulty_level_str = get_difficulty_from_save_file_name(
        save_file_name
    ).name
    game_created_time_str = format_datetime_to_string(
            get_datetime_from_save_file_name(save_file_name)
        )
    # display a message closing the game and how the user can continue it later on # noqa
    print(
        "\nThis Python Sudoku Game will now close. "
        "Your game is saved and can be continued at any time. "
        "\nSaved Games can be selected by their "
        "Difficulty and Created time. \n"
        f"\n * Your difficulty level was: {game_difficulty_level_str} "
        f"\n * Your game was created on: {game_created_time_str}"
    )


def display_undo_turn_message(turn_no: int, turn: Turn):
    """a helper function to display what is being undone in a turn

    Args:
        turn_no (int): the turn number being undone
        turn (Turn): the turn being undone
    """

    # calculate the display grid ref from the turn's matrix ref
    grid_ref = convert_matrix_reference_to_grid_reference(
        turn["row_index"],
        turn["col_index"]
    )

    # create a conditional string depending on if the new value is 0
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
    """a helper function to display a warning saying that no turns can be undone""" # noqa
    print(
        "\nNo turns can be undone. The Original Board is identical to "
        "the Playing Board. First, take a turn, then you can undo."
        "\nPlease press enter to continue"
    )
    input()


def display_redo_turn_message(turn_no: int, turn: Turn):
    """a helper function to display what is being redone in a turn

    Args:
        turn_no (int): the turn number being redone
        turn (Turn): the turn being redone
    """

    # calculate the display grid ref from the turn's matrix ref
    grid_ref = convert_matrix_reference_to_grid_reference(
        turn["row_index"],
        turn["col_index"]
    )
    # create a conditional string depending on if the previous value is 0
    modification_str = (
        f"changing {grid_ref} from "
        f"{turn['previous_value']} to {turn['new_value']}"
    ) if turn["previous_value"] != 0 else (
        f"filling {grid_ref} with {turn['new_value']}"
    )
    print(
        f"\nRedoing turn {turn_no + 2}, "
        + modification_str +
        "\nPlease press enter to continue"
    )
    input()


def display_unable_to_redo_turn_message():
    """a helper function to display a warning saying that no turns can be redone""" # noqa
    print(
        "\nNo turns can be redone. No turns have been undone. "
        "First, undo a turn, then you can redo."
        "\nPlease press enter to continue"
    )
    input()
