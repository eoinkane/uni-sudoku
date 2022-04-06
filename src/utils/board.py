
import string
from typing import Tuple
from itertools import chain
from .custom_types import Board, Column_References, Flat_Board, Row, Column


def get_column_references(board: Board) -> Column_References:
    return list(string.ascii_lowercase[0:len(board[0])].upper())


def get_sub_grid_indexes(grid_id: int):
    if (grid_id < 1 or grid_id > 9):
        raise Exception("invalid input to get_sub_grid_indexes")

    column_indexes = None
    if (grid_id <= 3):
        column_indexes = [
            x - 1 for x in [x + (3 * (grid_id - 1)) for x in range(1, 4)]
        ]
        row_indexes = [x for x in range(3)]
    elif (grid_id % 3 == 1):
        row_indexes = [x for x in range(grid_id - 1, grid_id + 2)]
    elif (grid_id % 3 == 2):
        row_indexes = [x for x in range(grid_id - 2, grid_id + 1)]
    else:
        row_indexes = [x for x in range(grid_id - 3, grid_id)]

    if (column_indexes is None):
        column_indexes = [
            x - 1 for x in [
                x + (3 * ((grid_id - 1) % 3)) for x in range(1, 4)
            ]]

    return {
        "row_indexes": row_indexes,
        "column_indexes": column_indexes
    }


def get_sub_grid(sub_grid_indexes, board: Board, grid_id: int) -> Board:
    sub_grid_indexes = get_sub_grid_indexes(grid_id)
    return [
        item[
            sub_grid_indexes["column_indexes"][0]:
            sub_grid_indexes["column_indexes"][-1] + 1
        ]
        for item in board[
            sub_grid_indexes["row_indexes"][0]:
            sub_grid_indexes["row_indexes"][-1] + 1
        ]
    ]


def generate_empty_board(board_size: int) -> Board:
    return [
        [0 for j in range(board_size)]
        for i in range(board_size)
    ]


def get_matrix_references(flat_position: int, board_size: int):
    if (flat_position > (board_size ** 2)):
        raise Exception('Position greater than sample')
    row_index, col_index = divmod(flat_position, 9)
    return row_index, col_index


def get_row(full_board: Board, row_index: int) -> Row:
    return full_board[row_index]


def get_column(full_board, col_index) -> Column:
    return list(list(zip(*full_board))[col_index])


def get_row_and_column(
    full_board: Board,
    row_index: int,
    col_index: int
        ):
    return (
        get_row(full_board, row_index),
        get_column(full_board, col_index)
    )


def reset_board_generation(board_size: int) -> (
    Tuple[int, list[list[int]], list[int]]
        ):
    board = generate_empty_board(board_size)
    flat_board = list(chain(*board))
    return 0, board, flat_board


def update_board(
    full_board: Board,
    flat_board: Flat_Board,
    row_index, col_index, board_size, value
        ) -> Tuple[list[list[int], list[int]]]:
    full_board[row_index][col_index] = value
    flat_board[(row_index * board_size) + col_index]
    return (full_board, flat_board)


def generate_allowed_values(
    local_full_board,
    row_index,
    col_index,
    board_size,
    do_not_use
        ):
    existing_row, existing_column = get_row_and_column(
        local_full_board,
        row_index,
        col_index
    )

    sub_grid_col = ((col_index // 3) + 1)

    sub_grid_row = ((row_index // 3) + 1)

    if (sub_grid_row == 1):
        sub_grid_id = sub_grid_col * sub_grid_row
    elif (sub_grid_row == 2):
        sub_grid_id = sub_grid_col + 3
    elif (sub_grid_row == 3):
        sub_grid_id = sub_grid_col + 6

    sub_grid_indexes = get_sub_grid_indexes(sub_grid_id)
    sub_grid = get_sub_grid(sub_grid_indexes, local_full_board, sub_grid_id)

    local_do_not_use = []
    if (((row_index * board_size) + col_index) in do_not_use):
        local_do_not_use = do_not_use[((row_index * board_size) + col_index)]

    allowed_values = [
        x for x in range(1, 10)
        if x not in existing_row
        and x not in existing_column
        and x not in local_do_not_use
        and x not in list(chain(*sub_grid))
    ]
    return allowed_values


def local_undo_one_value(
        flat_index,
        local_full_board,
        local_flat_board,
        board_size,
        do_not_use,
        **kwargs
        ):
    row_index, col_index = kwargs.get(
        "row_and_col_index",
        get_matrix_references(
            flat_index, board_size
        )
    )
    if ((flat_index) not in do_not_use):
        do_not_use[flat_index] = []
    do_not_use[flat_index].append(local_flat_board[flat_index])
    local_full_board[row_index][col_index] = 0
    local_flat_board[flat_index] = 0
    return (local_full_board, local_flat_board)


def return_to_last_choice(full_board, board_size, flat_index, do_not_use):
    local_full_board = full_board
    local_flat_board = list(chain(*local_full_board))
    for undoing_index in range(flat_index, -1, -1):
        row_index, col_index = get_matrix_references(
            undoing_index, board_size
        )
        undone_full_board, undone_flat_board = local_undo_one_value(
            undoing_index,
            local_full_board,
            local_flat_board,
            board_size,
            do_not_use,

            row_and_col_index=(row_index, col_index)
        )
        allowed_values = generate_allowed_values(
            undone_full_board,
            row_index,
            col_index,
            board_size,
            do_not_use
        )

        if (len(allowed_values) > 1):
            return {
                "row_index": row_index,
                "col_index": col_index,
                "full_board": local_full_board,
                "flat_board": local_flat_board,
                "undone_index": undoing_index
            }
    empty_board = generate_empty_board(board_size)
    return {
        "row_index": 0,
        "col_index": 0,
        "full_board": empty_board,
        "flat_board": list(chain(*empty_board)),
        "undone_index": 0
    }
