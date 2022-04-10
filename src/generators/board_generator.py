from random import choice, shuffle
from itertools import chain
from typing import Tuple
from copy import deepcopy
from utils.board import (
    generate_empty_board,
    get_matrix_references,
    update_board,
    generate_allowed_values,
    )
from utils.enums import Difficulty


def print_board(full_board):
    print("      1    2    3    4    5    6    7    8    9")
    print("    ______________________________________________")
    for print_row_index, print_row in enumerate(full_board):
        print(f"{print_row_index + 1} - | {' | '.join(stg if len(stg) == 2 else stg.zfill(2) for stg in [str(item) for item in print_row]).replace('00', '  ')} |")
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


def print_board_diff(full_board, changed_row_index, changed_col_index):
    changed_txt = '+'
    un_changed_txt = ' '
    print("    _______________________________________________________")
    for print_row_index, print_row in enumerate(full_board):
        print(f"{print_row_index + 1} - | {' | '.join((stg if len(stg) == 2 else stg.zfill(2)) + f'{changed_txt if (print_row_index == changed_row_index) and (stg_index == changed_col_index) else un_changed_txt}' for stg_index, stg in enumerate([str(item) for item in print_row]))} |")
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


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


def reset_board_generation(board_size: int) -> (
    Tuple[int, list[list[int]], list[int]]
        ):
    board = generate_empty_board(board_size)
    flat_board = list(chain(*board))
    return 0, board, flat_board


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


def generate_board(board_size: int, difficulty: Difficulty):
    do_not_use = {}
    test_obj = {}
    global_full_board = generate_empty_board(board_size)
    global_flat_board = list(chain(*global_full_board))
    no_of_positions = board_size ** 2
    positions = [x for x in range(no_of_positions)]

    i = 0

    while (i < no_of_positions):
        row_index, col_index = get_matrix_references(
            i, board_size
        )
        allowed_values = generate_allowed_values(
            global_full_board,
            row_index,
            col_index,
            board_size,
            do_not_use
        )
        shuffle(allowed_values)
        if (len(allowed_values) > 0):
            global_full_board, global_flat_board, = update_board(
                global_full_board,
                global_flat_board,
                row_index,
                col_index,
                board_size,
                allowed_values[0]
            )
            i += 1
        else:
            # existing_row, existing_column = get_row_and_column(
            #     global_full_board,
            #     row_index,
            #     col_index
            # )

            undone = return_to_last_choice(
                global_full_board,
                board_size,
                i,
                do_not_use
            )

            global_full_board = undone["full_board"]
            global_flat_board = undone["flat_board"]
            i = undone["undone_index"]
            if (i == 0):
                do_not_use = {}

        if (len(allowed_values) == 1):
            test_obj[i] = ((row_index, col_index))
        elif (i in test_obj):
            del test_obj[i]

    empty_full_board = deepcopy(global_full_board)

    empty_levels = {
        Difficulty.EASY:  choice([x for x in range(40, 46)]),
        Difficulty.MEDIUM: choice([x for x in range(46, 50)]),
        Difficulty.HARD: choice([x for x in range(50, 54)])
    }

    for i in range(empty_levels[difficulty]):
        changed = False
        while not changed:
            row_index, col_index = get_matrix_references(
                choice(positions),
                board_size
                )
            if (empty_full_board[row_index][col_index] != 0):
                empty_full_board[row_index][col_index] = 0
                changed = True

    return {
        "filled_full_board": global_full_board,
        "filled_flat_board": list(chain(*global_full_board)),
        "empty_full_board": empty_full_board,
        "empty_flat_board": list(chain(*empty_full_board))
    }


if __name__ == "__main__":
    generation = generate_board(9)
    filled_full_board = generation["filled_full_board"]
    empty_full_board = generation["empty_full_board"]

    print_board(filled_full_board)
    print(len([x for x in list(chain(*filled_full_board)) if x == 0]))
    print_board(empty_full_board)
    print(len([x for x in list(chain(*empty_full_board)) if x == 0]))
