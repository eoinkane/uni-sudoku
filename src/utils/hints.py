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
) -> Hints:
    """_summary_

    Args:
        playing_full_board (Board): 2-D version (matrix) of the current sudoku board
        board_size (int): size of the sudoku board
        row_index (int): the row index of the position to calculate for
        col_index (int): the row index of the position to calculate for
        hints (Hints): the already existing hints for the player
        position_value (int): the value being put into the sudoku board

    Returns:
        Hints: the updated hints for the game
    """ # noqa
    # construct the key for given matrix position in the hints dict
    hint_key = f"{row_index}{col_index}"

    # calculate the allowed values at the current position
    allowed_values = generate_allowed_values(
        playing_full_board,
        row_index,
        col_index,
        board_size,
        {}
    )
    # if the new value is not allowed and is not equal to previous value at that position # noqa
    if (
        position_value != 0 and
        position_value not in allowed_values and
        playing_full_board[row_index][col_index] != position_value
    ):
        # update the hints dict at the hint key to show a hint for this position # noqa
        hints[hint_key] = "?"
    # otherwise, if the position already has a hint and either,
    #  the new value is 0 or the new value is allowed
    elif (
        (hint_key in hints and position_value == 0) or
        (hint_key in hints and position_value in allowed_values)
    ):
        # remove the hint for the current position
        del hints[hint_key]
    return hints


def handle_hints_for_an_undo_or_redo(
    playing_full_board: Board,
    board_size: int,
    row_index: int,
    col_index: int,
    hints: Hints,
    updated_position_value: int
) -> Hints:
    """_summary_

    Args:
        playing_full_board (Board): 2-D version (matrix) of the current sudoku board
        board_size (int): size of the sudoku board
        row_index (int): the row index of the position to calculate for
        col_index (int): the row index of the position to calculate for
        hints (Hints): the already existing hints for the player
        updated_position_value (int): the value being put into the sudoku board

    Returns:
        Hints: the recalculated hints
    """ # noqa

    # calculate which hints need to be rechecked
    affected_hints = {
        key: value for key, value
        in hints.items()
        if key[0] == str(row_index) or key[1] == str(col_index)
    }

    # for each affected hint check if it needs to be deleted
    for affected_hint_key in affected_hints.keys():
        # get the row and column index of the affected hint
        affected_hint_row_index = int(affected_hint_key[0])
        affected_hint_col_index = int(affected_hint_key[1])

        # get the board value for the affected hint
        affected_board_value = (
            (
                playing_full_board[affected_hint_row_index]
            )[affected_hint_col_index]
        )

        # if the value of the affected hint is now in the allowed values then delete the hint # noqa 
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

    # recalculate the hints for the position being undone or redone
    hints = handle_hints(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        updated_position_value
    )

    # return the updated hints
    return hints
