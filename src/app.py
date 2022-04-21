from copy import deepcopy
from datetime import datetime, timedelta
from itertools import chain
from utils.player_experience import (
    show_help,
    welcome,
    display_quit_message,
    display_unable_to_undo_turn_message,
    display_unable_to_redo_turn_message
)
from utils.game import (
    create_game_config,
    take_turn,
    complete_game,
    undo_turn,
    redo_turn
)
from utils.custom_types import (
    Board,
    Generation,
    Flat_Board,
    Hints,
    Column_References
)
from utils.screen import (
    clear_screen,
    print_edit_and_original_sudoku_board,
    setup_screen_config,
    print_sudoku_board
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
from utils.time import (
    format_time_elapsed_timedelta_to_string,
    calculate_time_elapsed
)


def assign_print_board_func(
    hints_enabled: bool,
    stats_enabled: bool,
    board_size: int,
    column_references: Column_References,
    initial_flat_board: Flat_Board,
    solution_flat_board: Flat_Board,
    timer_enabled: bool,
    timer_duration: timedelta
):
    """Setup the display config and return a curried function that
    removes the need to pass unchanged args to
    print_edit_and_original_sudoku_board every call.

    Args:
        hints_enabled (bool): should the hints be enabled
        stats_enabled (bool): should the stats be enabled
        board_size (int): Size of the sudoku board
        column_references (Column_References): Column References to be used when displaying the sudoku boards
        initial_flat_board (Flat_Board): 1-D version of the initial sudoku board
        solution_flat_board (Flat_Board): 1-D version of the sudoku board solution
        timer_enabled (bool): should the time be enabled
        timer_duration (timedelta): Duration of the timer

    Returns:
        (unedited_board: Board, playing_board: Board, starting_time: datetime, **kwargs: Any) -> None: A wrapper function that will print the sudoku board.
    """ # noqa

    # Initialise the display config so that args do not,
    #  need to be passed every time the board prints.
    setup_screen_config(
        board_size,
        hints_enabled,
        stats_enabled,
        column_references,
        initial_flat_board,
        solution_flat_board,
        timer_enabled,
        timer_duration
    )

    # define the function in the local scope so that the function can be curried # noqa
    def print_board_func(
        unedited_board: Board,
        playing_board: Board,
        starting_time: datetime,
        **kwargs
    ):
        time_elasped = calculate_time_elapsed(starting_time)
        remaining_timer_duration = None
        if (timer_enabled):
            remaining_timer_duration = timer_duration - time_elasped
        return print_edit_and_original_sudoku_board(
            unedited_board,
            playing_board,
            time_elasped_str=format_time_elapsed_timedelta_to_string(
                time_elasped
            ),
            remaining_timer_duration_str=(
                format_time_elapsed_timedelta_to_string(
                    remaining_timer_duration
                )
            ),
            **kwargs
        )
    return print_board_func


def game(
    generation: Generation,
    board_size: int,
    hints_enabled: bool,
    stats_enabled: bool,
    save_file_name: str,
    hints: Hints,
    timer_enabled: bool,
    timer_duration: timedelta
):
    """The game runner. This function is called with everything to run a game and will loop until the game is quit or completed

    Args:
        generation (Generation): the generated board and board config. Could be from a saved game file or a created generation
        board_size (int): size of the sudoku board
        hints_enabled (bool): should the hints be enabled
        stats_enabled (bool): should the stats be enabled
        save_file_name (str): the reference to the saved game file to update the game as it progresses
        hints (Hints): the datastore to represent the hints for the player
        timer_enabled (bool): should the time be enabled
        timer_duration (timedelta): Duration of the timer

    Returns:
        None
    """ # noqa

    # Pull the game config out of the generation
    unedited_full_board: Board = deepcopy(generation["initial_full_board"])
    playing_full_board: Board = deepcopy(generation["playing_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))
    turns = list(generation["turns"])
    on_turn_no = generation["on_turn_no"]

    game_completed = False

    # Get the Column References for displaying the sudoku board
    column_references = get_column_references(unedited_full_board)

    # Assign a print sudoku board function wrapper to simplify calls
    print_board_func = assign_print_board_func(
        hints_enabled,
        stats_enabled,
        board_size,
        column_references,
        generation["initial_flat_board"],
        generation["solution_flat_board"],
        timer_enabled,
        timer_duration
    )

    # calculate the datetime to be used as the starting time
    # a saved game stores how long the game has gone on for
    # uses that duration to create a datetime object that long ago
    starting_date_time = None
    if ((save_time_elapsed := generation["time_elapsed"]) is None):
        starting_date_time = datetime.now()
    else:
        starting_date_time = datetime.now() - save_time_elapsed

    # loop to keep running a round of the game until it is completed or the player quits # noqa
    while not game_completed:
        # check if the player has gone over the time limit
        if (
            timer_enabled and
            (
                time_elapsed := calculate_time_elapsed(starting_date_time)
            ) > timer_duration
        ):
            clear_screen()
            print(
                "The timer has ran out. You did not manage "
                "to complete the sudoku board in time."
            )
            print_sudoku_board(
                playing_full_board,
                should_clear_screen=False,
                time_elasped_str=(
                    format_time_elapsed_timedelta_to_string(time_elapsed)
                )
            )
            break

        # display the sudoku board
        print_board_func(
            unedited_full_board,
            playing_full_board,
            starting_date_time,
            hints=hints
        )

        # let the player decide what action to take this round
        action = decide_action()

        if (action == Action.TAKE_TURN):
            # display the sudoku board
            print_board_func(
                unedited_full_board,
                playing_full_board,
                starting_date_time,
                hints=hints
            )
            # take a turn and update the sudoku board, hints and turns 
            (
                (playing_full_board, playing_flat_board),
                (hints, (on_turn_no, turns))
            ) = take_turn(
                unedited_full_board,
                playing_full_board,
                playing_flat_board,
                board_size,
                column_references,
                hints,
                on_turn_no,
                turns
            )
        elif (action == Action.UNDO and on_turn_no > -1):
            # display the sudoku board
            print_board_func(
                unedited_full_board,
                playing_full_board,
                starting_date_time,
                hints=hints
            )
            # undo a turn and update the sudoku board
            (
                (playing_full_board, playing_flat_board),
                (hints, turns)
            ) = undo_turn(
                on_turn_no,
                playing_full_board,
                playing_flat_board,
                board_size,
                hints,
                turns
            )
            # decrease the turn counter as a turn has been undone
            on_turn_no -= 1
        elif (action == Action.UNDO and on_turn_no == -1):
            # explain to the player that there is nothing to undo
            display_unable_to_undo_turn_message()
        elif (action == Action.REDO and on_turn_no < (len(turns) - 1)):
            # display the sudoku board
            print_board_func(
                unedited_full_board,
                playing_full_board,
                starting_date_time,
                hints=hints
            )
            # redo a turn and update the sudoku board
            (
                (playing_full_board, playing_flat_board),
                (hints, turns)
            ) = redo_turn(
                on_turn_no,
                playing_full_board,
                playing_flat_board,
                board_size,
                hints,
                turns
            )
            # increase the turn counter as a turn has been redone
            on_turn_no += 1
        elif (action == Action.REDO and on_turn_no == (len(turns) - 1)):
            # explain to the player that there is nothing to redo
            display_unable_to_redo_turn_message()
        elif (action == Action.SHOW_HELP):
            # display the help message and allow the user to modify hints_enabled and stats_enabled # noqa
            new_hints_enabled, new_stats_enabled = show_help(
                hints_enabled,
                stats_enabled
            )
            # if hints_enabled or stats_enabled has been changed then the print sudoku board wrapper needs to be updated
            if (
                new_hints_enabled != hints_enabled or
                new_stats_enabled != stats_enabled
            ):
                print_board_func = assign_print_board_func(
                    new_hints_enabled,
                    new_stats_enabled,
                    board_size,
                    column_references,
                    generation["initial_flat_board"],
                    generation["solution_flat_board"],
                    timer_enabled,
                    timer_duration
                )
                hints_enabled = new_hints_enabled
                stats_enabled = new_stats_enabled
        elif (action == Action.QUIT):
            # quit the game
            return display_quit_message(save_file_name)

        # update the saved game file with the new sudoku board and config at the end of the round # noqa
        update_save(
            save_file_name,
            playing_full_board,
            hints_enabled,
            stats_enabled,
            hints,
            on_turn_no,
            turns,
            starting_date_time
        )

        # check if the game is completed
        if (
            len([x for x in playing_flat_board if x == 0]) == 0 and
            playing_flat_board == generation["solution_flat_board"]
        ):
            game_completed = True
            complete_save(save_file_name)
            # display the completed board and a success message to the player
            complete_game(
                playing_full_board,
                starting_date_time
            )


def main():
    """A function to start the game. This is the root function triggered from the command line""" # noqa
    board_size = 9
    welcome()

    # create or load the game config to play the game
    generation, (
        save_file_name,
        (
            stats_enabled,
            (
                (
                    timer_enabled,
                    timer_duration
                ),
                (
                    hints_enabled,
                    hints
                )
            )
        )
    ) = (
        create_game_config(board_size)
    )

    # run the game with the created or loaded game config
    game(
        generation,
        board_size,
        hints_enabled,
        stats_enabled,
        save_file_name,
        hints,
        timer_enabled,
        timer_duration
    )


if __name__ == "__main__":
    main()
