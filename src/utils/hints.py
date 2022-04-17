from utils.custom_types import (
    Board,
    Hints
)
from utils.board import generate_allowed_values


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
        position_value not in allowed_values and
        playing_full_board[row_index][col_index] != position_value
    ):
        hints[hint_key] = "?"
    elif (
        (hint_key in hints and position_value == 0) or
        (hint_key in hints and position_value in allowed_values)
    ):
        del hints[hint_key]
    return hints


def handle_hints_for_an_undo_or_redo(
    playing_full_board: Board,
    board_size: int,
    row_index: int,
    col_index: int,
    hints: Hints,
    updated_position_value: int
):
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
        updated_position_value
    )

    return hints
