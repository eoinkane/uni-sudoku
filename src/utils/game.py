from datetime import datetime, timedelta
from typing import Dict, Tuple, List
from itertools import chain
from save_handlers.save_handlers import (
    check_if_there_are_saved_games,
    read_save,
    create_save
)
from generators.board_generator import generate_board
from utils.user_input_helpers import (
    decide_whether_to_play_saved_game,
    select_difficulty,
    select_hints_enabled,
    select_saved_game,
    select_position_value,
    select_grid_reference,
    select_stats_enabled,
)
from utils.custom_types import (
    Board,
    Column_References,
    Generation,
    Flat_Board,
    Hints
)
from utils.board import (
    update_board
)
from utils.screen import clear_screen, print_sudoku_board
from utils.player_experience import (
    display_undo_turn_message,
    display_redo_turn_message
)
from utils.hints import (
    handle_hints,
    handle_hints_for_an_undo_or_redo
)
from utils.time import (
    format_time_elapsed_timedelta_to_string,
    calculate_time_elapsed
)


def create_game_config(board_size: int):
    use_saved_game = decide_whether_to_play_saved_game()

    if use_saved_game and check_if_there_are_saved_games():
        save_file_path = select_saved_game()
        save = read_save(save_file_path)
        generation = {
            "solution_full_board": save["solution_board"],
            "solution_flat_board": list(chain(*save["solution_board"])),
            "initial_full_board": save["initial_board"],
            "initial_flat_board": list(chain(*save["initial_board"])),
            "playing_full_board": save["playing_board"],
            "playing_flat_board": list(chain(*save["playing_board"])),
            "on_turn_no": save["on_turn_no"],
            "turns": save["turns"],
            "time_elapsed": timedelta(seconds=save["time_elapsed_secs"])
        }
        return generation, (
            save_file_path,
            (
                save["stats_enabled"],
                (
                    save["hints_enabled"],
                    save["hints"]
                ),
            )
        )
    else:
        if (use_saved_game):
            print(
                "\nThere are no saved games available for you to continue. "
                "Please create a new one."
            )
        difficulty = select_difficulty()
        hints_enabled = select_hints_enabled()
        stats_enabled = select_stats_enabled()
        generation: Generation = generate_board(board_size, difficulty)

        save_file_name = create_save(
            generation["solution_full_board"],
            generation["playing_full_board"],
            generation["initial_full_board"],
            board_size,
            difficulty,
            hints_enabled,
            stats_enabled
        )
        return generation, (
            save_file_name,
            (
                stats_enabled,
                (
                    hints_enabled,
                    {}
                )
            )
        )


def take_turn(
    unedited_full_board: Board,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    column_references: Column_References,
    hints: Hints,
    on_turn_no: int,
    turns: List
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

    hints = handle_hints(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        position_value
    )

    previous_value = playing_full_board[row_index][col_index]
    if (position_value != previous_value):
        if (on_turn_no < (len(turns) - 1)):
            turns = turns[0:(on_turn_no + 1)]
        turns.append({
            "row_index": row_index,
            "col_index": col_index,
            "new_value": position_value,
            "previous_value": playing_full_board[row_index][col_index]
        })
        on_turn_no += 1

    playing_full_board, playing_flat_board = update_board(
            playing_full_board,
            playing_flat_board,
            row_index,
            col_index,
            board_size,
            int(position_value)
        )
    return (
        (
            playing_full_board,
            playing_flat_board
        ),
        (
            hints,
            (
                on_turn_no,
                turns
            )
        )
    )


def complete_game(
    completed_board: Board,
    board_size: int,
    column_references: Column_References,
    starting_time: datetime
):
    clear_screen()
    time_taken_to_complete_game_str = format_time_elapsed_timedelta_to_string(
        calculate_time_elapsed(starting_time)
    )

    print(
        "Congratulations, you completed the sudoku game! "
        f"\nIt took you {time_taken_to_complete_game_str} to complete the game"
        "\nHere is the completed board"
    )
    print_sudoku_board(
        completed_board,
        board_size,
        column_references,
        should_clear_screen=False
    )


def undo_turn(
    turn_no: int,
    playing_full_board,
    playing_flat_board,
    board_size,
    hints,
    turns: list
):
    turn = turns[turn_no]
    row_index = turn["row_index"]
    col_index = turn["col_index"]

    display_undo_turn_message(turn_no, turn)

    hints = handle_hints_for_an_undo_or_redo(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        turn["previous_value"]
    )

    playing_full_board, playing_flat_board = update_board(
        playing_full_board,
        playing_flat_board,
        row_index,
        col_index,
        board_size,
        turn["previous_value"]
    )

    return (
        (
            playing_full_board,
            playing_flat_board
        ),
        (
            hints,
            turns
        )
    )


def redo_turn(
    turn_no: int,
    playing_full_board,
    playing_flat_board,
    board_size,
    hints,
    turns: list
):
    turn = turns[turn_no + 1]
    row_index = turn["row_index"]
    col_index = turn["col_index"]

    display_redo_turn_message(turn_no, turn)

    hints = handle_hints_for_an_undo_or_redo(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        turn["new_value"]
    )

    playing_full_board, playing_flat_board = update_board(
        playing_full_board,
        playing_flat_board,
        row_index,
        col_index,
        board_size,
        turn["new_value"]
    )

    return (
        (
            playing_full_board,
            playing_flat_board
        ),
        (
            hints,
            turns
        )
    )
