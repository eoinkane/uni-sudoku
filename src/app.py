from copy import deepcopy
from datetime import datetime, timedelta
from itertools import chain
from data.game1 import data
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
    unedited_full_board: Board = deepcopy(generation["initial_full_board"])
    playing_full_board: Board = deepcopy(generation["playing_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))
    turns = list(generation["turns"])
    on_turn_no = generation["on_turn_no"]

    game_completed = False

    column_references = get_column_references(unedited_full_board)

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

    starting_date_time = None
    if ((save_time_elapsed := generation["time_elapsed"]) is None):
        starting_date_time = datetime.now()
    else:
        starting_date_time = datetime.now() - save_time_elapsed

    while not game_completed:
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
        print_board_func(
            unedited_full_board,
            playing_full_board,
            starting_date_time,
            hints=hints
        )
        action = decide_action()

        if (action == Action.TAKE_TURN):
            print_board_func(
                unedited_full_board,
                playing_full_board,
                starting_date_time,
                hints=hints
            )
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
            print_board_func(
                unedited_full_board,
                playing_full_board,
                starting_date_time,
                hints=hints
            )
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
            on_turn_no -= 1
        elif (action == Action.UNDO and on_turn_no == -1):
            display_unable_to_undo_turn_message()
        elif (action == Action.REDO and on_turn_no < (len(turns) - 1)):
            print_board_func(
                unedited_full_board,
                playing_full_board,
                starting_date_time,
                hints=hints
            )
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
            on_turn_no += 1
        elif (action == Action.REDO and on_turn_no == (len(turns) - 1)):
            display_unable_to_redo_turn_message()
        elif (action == Action.SHOW_HELP):
            new_hints_enabled, new_stats_enabled = show_help(
                hints_enabled,
                stats_enabled
            )
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
            return display_quit_message(save_file_name)

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
        if (
            len([x for x in playing_flat_board if x == 0]) == 0 and
            playing_flat_board == generation["solution_flat_board"]
        ):
            game_completed = True
            complete_save(save_file_name)
            complete_game(
                playing_full_board,
                starting_date_time
            )


def main():
    board_size = 9
    welcome()

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
