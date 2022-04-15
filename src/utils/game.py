from typing import Dict, Tuple
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
)
from utils.custom_types import (
    Board,
    Column_References,
    Generation,
    Flat_Board,
    Hints
)
from utils.board import (
    update_board,
    generate_allowed_values
)
from utils.screen import clear_screen, print_sudoku_board
from utils.player_experience import (
    display_undo_turn_message
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
            "turns": save["turns"]
        }
        return generation, (
            save_file_path,
            (
                save["hints_enabled"],
                save["hints"]
            ),
        )
    else:
        if (use_saved_game):
            print(
                "\nThere are no saved games available for you to continue. "
                "Please create a new one."
            )
        difficulty = select_difficulty()
        hints_enabled = select_hints_enabled()
        generation: Generation = generate_board(board_size, difficulty)

        save_file_name = create_save(
            generation["solution_full_board"],
            generation["playing_full_board"],
            generation["initial_full_board"],
            board_size,
            difficulty,
            hints_enabled
        )
        return generation, (
            save_file_name,
            (
                hints_enabled,
                {}
            )
        )


def handle_hints(
    playing_full_board: Board,
    board_size: int,
    row_index: int,
    col_index: int,
    hints: Hints,
    position_value: int
):
    hint_key = f"{row_index}{col_index}"
    allowed_values = generate_allowed_values(
        playing_full_board,
        row_index,
        col_index,
        board_size,
        {}
    )
    if (
        position_value != 0 and
        position_value not in allowed_values
    ):
        hints[hint_key] = "?"
    elif (
        (hint_key in hints and position_value == 0) or
        (hint_key in hints and position_value in allowed_values)
    ):
        del hints[hint_key]
    return hints


def take_turn(
    unedited_full_board: Board,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    column_references: Column_References,
    hints: Hints,
    turns
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
        turns.append({
            "row_index": row_index,
            "col_index": col_index,
            "new_value": position_value,
            "previous_value": playing_full_board[row_index][col_index]
        })

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
            turns
        )
    )


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


def undo_turn(
    turn_no: int,
    playing_full_board,
    playing_flat_board,
    board_size,
    hints,
    turns: list
):
    turn = turns.pop(turn_no)
    row_index = turn["row_index"]
    col_index = turn["col_index"]

    display_undo_turn_message(turn_no, turn)

    affected_hints = {
        key: value for key, value
        in hints.items()
        if key[0] == str(row_index) or key[1] == str(col_index)
    }
    for affected_hint_key in affected_hints.keys():
        affected_hint_row_index = int(affected_hint_key[0])
        affected_hint_col_index = int(affected_hint_key[1])

        affected_board_value = (
            (
                playing_full_board[affected_hint_row_index]
            )[affected_hint_col_index]
        )

        if (
            affected_board_value == 0
            or affected_board_value in generate_allowed_values(
                playing_full_board,
                affected_hint_row_index,
                affected_hint_col_index,
                board_size,
                {}
            )
        ):
            del hints[affected_hint_key]

    hints = handle_hints(
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
