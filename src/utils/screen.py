from datetime import timedelta
from itertools import chain
import platform
import os
from .custom_types import (
    Board,
    Column_References,
    Hints,
    Flat_Board,
    Row
)

SETUP_COMPLETED = False
COLUMN_KEYS = None
TOP_LINE = None
BOTTOM_LINE = None
COLUMN_REFERENCES = None
BOARD_SIZE = None
HINTS_ENABLED = None
STATS_ENABLED = None
SOLUTION_FLAT_BOARD = None
NO_INITIAL_FILLED_POSITIONS = None
TIMER_ENABLED = None
TIMER_DURATION = None


def clear_screen():
    """a helper function that can clear the screen while being platform agnostic""" # noqa
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    print()


def setup_screen_config(
    board_size: int,
    hints_enabled: bool,
    stats_enabled: bool,
    column_references: Column_References,
    initial_flat_board: Flat_Board,
    solution_flat_board: Flat_Board,
    timer_enabled: bool,
    timer_duration: timedelta
):
    """initialise the global variables need to display a sudoku board so, 
    that they do not need to be passed on every sudoku board printcall.
    this function must be called before any of the custom print functions.

    Args:
        board_size (int): size of the sudoku board
        hints_enabled (bool): should the hints be enabled
        stats_enabled (bool): should the stats be enabled
        column_references (Column_References): Column References to be used when displaying the sudoku boards
        initial_flat_board (Flat_Board): 1-D version of the initial sudoku board
        solution_flat_board (Flat_Board): 1-D version of the sudoku board solution
        timer_enabled (bool): should the time be enabled
        timer_duration (timedelta): Duration of the timer
    """ # noqa
    global BOARD_SIZE
    BOARD_SIZE = board_size

    global HINTS_ENABLED
    HINTS_ENABLED = hints_enabled

    global STATS_ENABLED
    STATS_ENABLED = stats_enabled

    global COLUMN_KEYS
    COLUMN_KEYS = "   ".join([str(x) for x in range(1, (BOARD_SIZE + 1))])

    global TOP_LINE
    TOP_LINE = "_" + "____" * BOARD_SIZE

    global BOTTOM_LINE
    BOTTOM_LINE = "¯" + "¯¯¯¯" * BOARD_SIZE

    global COLUMN_REFERENCES
    COLUMN_REFERENCES = column_references

    global NO_INITIAL_FILLED_POSITIONS
    NO_INITIAL_FILLED_POSITIONS = len(
        [x for x in initial_flat_board if x != 0]
    )

    global SOLUTION_FLAT_BOARD
    SOLUTION_FLAT_BOARD = solution_flat_board

    global TIMER_ENABLED
    TIMER_ENABLED = timer_enabled

    if (TIMER_ENABLED):
        global TIMER_DURATION
        TIMER_DURATION = timer_duration

    global SETUP_COMPLETED
    SETUP_COMPLETED = True


def print_sudoku_board(
    board: Board,
    **kwargs
):
    """display a single sudoku board

    Args:
        board (Board): 2-D version (matrix) of the current sudoku board

    Raises:
        Exception: when the setup_screen_config function has not been called

    Keyword Args:
        should_clear_screen (bool): should the screen be cleared before printing. default: True
        time_elasped_str (str): the time elapsed for the current game. default: None
        remaining_timer_duration_str (str): the time remaining in the current game. default: None
    """ # noqa
    if (not SETUP_COMPLETED):
        raise Exception(
            "print_sudoku_board used before setup_screen_config was called"
        )

    # get the keyword args
    should_clear_screen = kwargs.get(
        "should_clear_screen",
        True
    )
    time_elasped_str = kwargs.get(
        "time_elasped_str",
        None
    )
    remaining_timer_duration_str = kwargs.get(
        "remaining_timer_duration_str",
        None
    )

    # clear the screen if the option is set to True
    if should_clear_screen:
        clear_screen()

    # to only not call print for every line and not be limited by,
    #  fstrings add every line to a list and then print the list
    output = []

    output.append("      " + COLUMN_KEYS)
    output.append("    " + TOP_LINE)
    for row_index in range(BOARD_SIZE):
        row = board[row_index]
        row_key = f"{COLUMN_REFERENCES[row_index]} - | "

        output.append(
            row_key +
            build_unedited_row(row)
        )
    output.append("    " + BOTTOM_LINE)

    print("\n".join(output))

    if (remaining_timer_duration_str):
        print(f"Time Remaining In The Timer: f{remaining_timer_duration_str}")
    if (time_elasped_str):
        print(f"Time Elapsed Since the Start of the Game: {time_elasped_str}")


def build_unedited_row(unedited_row: Row) -> str:
    """helper function to build a display line for a unedited board row

    Args:
        unedited_row (Row): the row to be displayed

    Returns:
        str: the line to display this unedited board row
    """
    return (
        " | ".join(
            str(item) for item in unedited_row
        ).replace("0", " ") +
        " |"
    )


def build_playing_row(
    playing_row: Row,
    row_index: int,
    hints: Hints
) -> str:
    """helper function to build a display line for a playing board row

    Args:
        playing_row (Row): the row to be displayed
        row_index (int): the row index of the row to be displayed
        hints (Hints): the hints for the current sudoku game

    Returns:
        str: the line to display this playing board row
    """
    return (
        "| ".join(
            str(item) + (
                " " if not HINTS_ENABLED
                else hints.get((str(row_index) + str(col_index)), ' ')
            ) for col_index, item in enumerate(playing_row)
        ).replace("0", " ") +
        "|"
    )


def print_edit_and_original_sudoku_board(
        unedited_board: Board,
        playing_board: Board,
        **kwargs
):
    """display a two sudoku boards side by side

    Args:
        unedited_board (Board): 2-D version (matrix) of the initial sudoku board
        playing_board (Board): 2-D version (matrix) of the current sudoku board
    
    Keyword Args:
        hints (Hints): the hints for the current sudoku game
        should_clear_screen (bool): should the screen be cleared before printing. default: True
        time_elasped_str (str): the time elapsed for the current game. default: None
        remaining_timer_duration_str (str): the time remaining in the current game. default: None
    """ # noqa

    # get the keyword args
    hints = kwargs.get("hints", {})
    should_clear_screen = kwargs.get(
        "should_clear_screen",
        True
    )
    time_elasped_str = kwargs.get(
        "time_elasped_str",
        None
    )
    remaining_timer_duration_str = kwargs.get(
        "remaining_timer_duration_str",
        None
    )

    # clear the screen if the option is set to True
    if should_clear_screen:
        clear_screen()

    # to only call print once and not be limited by,
    #  fstrings add every line to a list and then print the list
    output = []

    output.append(
        "      " + "Original Board" +
        ("    " + "   " * BOARD_SIZE) +
        "Playing Board"
         )
    output.append("      " + COLUMN_KEYS + "            " + COLUMN_KEYS)
    output.append("    " + TOP_LINE + "        " + TOP_LINE)
    for row_index in range(BOARD_SIZE):
        unedited_row = unedited_board[row_index]
        playing_row = playing_board[row_index]

        row_key = f"{COLUMN_REFERENCES[row_index]} - | "

        output.append(
            row_key +
            build_unedited_row(unedited_row) +
            "    " +
            row_key +
            build_playing_row(
                playing_row,
                row_index,
                hints
            )
        )
    output.append("    " + BOTTOM_LINE + "        " + BOTTOM_LINE)

    flat_playing_board = list(chain(*playing_board))
    flat_unedited_board = list(chain(*unedited_board))
    if (STATS_ENABLED):
        if HINTS_ENABLED:
            output.append(
                "Stats\n" +
                "Percentage of board correctly filled "
                + str(
                    round(
                        (
                            len(
                                [
                                    playing_value
                                    for (original_value, playing_value),
                                    solution_value in zip(zip(
                                        flat_unedited_board, flat_playing_board
                                    ), SOLUTION_FLAT_BOARD)
                                    if (
                                        original_value == 0 and
                                        playing_value == solution_value
                                    ) or original_value != 0
                                ]
                            )
                            / (BOARD_SIZE ** 2)
                        )
                        * 100,
                        2,
                    )
                ) +
                "%"
            )
        else:
            output.append(
                "Stats\n" +
                "Percentage of board filled (irregardless of correct value) "
                + str(
                    round(
                        (
                            len(
                                [
                                    playing_value
                                    for original_value, playing_value in zip(
                                        flat_unedited_board, flat_playing_board
                                    )
                                    if (
                                        original_value == 0 and
                                        playing_value != 0
                                    ) or original_value != 0
                                ]
                            )
                            / (BOARD_SIZE ** 2)
                        )
                        * 100,
                        2,
                    )
                ) +
                "%"
            )
        if (TIMER_ENABLED):
            output.append(
                f"Time Remaining in the Timer: {remaining_timer_duration_str}"
            )
        output.append(
            f"Time Elasped Since the Start of the Game: {time_elasped_str}"
        )

    print("\n".join(output))
