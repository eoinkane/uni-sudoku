from datetime import timedelta
from itertools import chain
import platform
import os
from .custom_types import (
    Board,
    Column_References,
    Hints,
    Flat_Board
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
    if (not SETUP_COMPLETED):
        raise Exception(
            "print_sudoku_board used before setup_screen_config was called"
        )

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
    if should_clear_screen:
        clear_screen()

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


def build_unedited_row(unedited_row):
    return (
        " | ".join(
            str(item) for item in unedited_row
        ).replace("0", " ") +
        " |"
    )


def build_playing_row(
    playing_row: list[int],
    row_index: int,
    hints: Hints
):
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

    if should_clear_screen:
        clear_screen()

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
