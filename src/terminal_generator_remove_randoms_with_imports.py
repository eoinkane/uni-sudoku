from random import choice, shuffle
from itertools import chain
# from typing import Tuple
from utils.board import (
    # get_sub_grid_indexes,
    # get_sub_grid,
    generate_empty_board,
    get_matrix_references,
    # get_column,
    # get_row,
    get_row_and_column,
    update_board,
    generate_allowed_values,
    # local_undo_one_value,
    return_to_last_choice
    )


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


def main():
    global_board_size = 9
    do_not_use = {}
    test_obj = {}
    global_full_board = generate_empty_board(global_board_size)
    global_flat_board = list(chain(*global_full_board))
    no_of_positions = global_board_size ** 2
    positions = [x for x in range(no_of_positions)]

    i = 0

    while (i < no_of_positions):
        row_index, col_index = get_matrix_references(
            i, global_board_size
        )
        allowed_values = generate_allowed_values(
            global_full_board,
            row_index,
            col_index,
            global_board_size,
            do_not_use
        )
        shuffle(allowed_values)
        if (len(allowed_values) > 0):
            global_full_board, global_flat_board, = update_board(
                global_full_board,
                global_flat_board,
                row_index,
                col_index,
                global_board_size,
                allowed_values[0]
            )
            i += 1
        else:
            existing_row, existing_column = get_row_and_column(
                global_full_board,
                row_index,
                col_index
            )

            undone = return_to_last_choice(
                global_full_board,
                global_board_size,
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

    print_board(global_full_board)
    print(len([x for x in list(chain(*global_full_board)) if x == 0]))

    empty_levels = {
        "EASY":  choice([x for x in range(40, 46)]),
        "MEDIUM": choice([x for x in range(46, 50)]),
        "HARD": choice([x for x in range(50, 54)])
    }

    for i in range(empty_levels["EASY"]):
        changed = False
        while not changed:
            row_index, col_index = get_matrix_references(
                choice(positions),
                global_board_size
                )
            if (global_full_board[row_index][col_index] != 0):
                global_full_board[row_index][col_index] = 0
                changed = True

    print_board(global_full_board)
    print(len([x for x in list(chain(*global_full_board)) if x == 0]))


if __name__ == "__main__":
    main()
