from random import choice, sample, shuffle
from itertools import chain


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


def get_matrix_references(flat_position: int, board_size: int):
    if (flat_position > (board_size ** 2)):
        raise Exception('Position greater than sample')
    row_index, col_index = divmod(flat_position, 9)
    return row_index, col_index


def get_row(full_board, row_index) -> list[int]:
    return full_board[row_index]


def get_column(full_board, board_size, col_index) -> list[int]:
    return list(list(zip(*full_board))[col_index])
    # return [
    #     val for ind, val in
    #     enumerate(flat)
    #     if ind % board_size == col_index
    # ]


def get_row_and_column(
    full_board,
    flat,
    board_size,
    row_index,
    col_index
        ):
    return (
        get_row(full_board, row_index),
        get_column(full_board, board_size, col_index)
    )


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


def get_sub_grid(sub_grid_indexes, board, grid_id: int):
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


def generate_empty_board(board_size: int) -> list[list[int]]:
    return [
        [0 for j in range(board_size)]
        for i in range(board_size)
    ]


def reset_generation(board_size: int) -> (
    tuple[int, list[list[int]], list[int]]
        ):
    board = generate_empty_board(board_size)
    flat_board = list(chain(*board))
    return 0, board, flat_board


def update_board(row_index, col_index, board_size, value):
    global_full_board[row_index][col_index] = value
    global_flat_board[(row_index * board_size) + col_index]


def generate_allowed_values(
    local_full_board,
    local_flat_board,
    row_index,
    col_index,
    board_size
        ):
    existing_row, existing_column = get_row_and_column(
        local_full_board,
        local_flat_board,
        board_size,
        row_index,
        col_index
    )

    sub_grid_col = ((col_index // 3) + 1)

    sub_grid_row = ((row_index // 3) + 1)

    # sub_grid_id = 0
    if (sub_grid_row == 1):
        sub_grid_id = sub_grid_col * sub_grid_row
    elif (sub_grid_row == 2):
        sub_grid_id = sub_grid_col + 3
    elif (sub_grid_row == 3):
        sub_grid_id = sub_grid_col + 6

    sub_grid_indexes = get_sub_grid_indexes(sub_grid_id)
    sub_grid = get_sub_grid(sub_grid_indexes, global_full_board, sub_grid_id)

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


def is_valid_update(row_index, col_index, value, board_size,  **kwargs):
    allowed_values = kwargs.get('allowed_values', generate_allowed_values(
        row_index, col_index, board_size
        ))
    return value in allowed_values


def local_undo_one_value(
        flat_index,
        local_full_board,
        local_flat_board,
        **kwargs
        ):
    row_index, col_index = kwargs.get(
        "row_and_col_index",
        get_matrix_references(
            flat_index, global_board_size
        )
    )
    if ((flat_index) not in do_not_use):
        do_not_use[flat_index] = []
    do_not_use[flat_index].append(local_flat_board[flat_index])
    local_full_board[row_index][col_index] = 0
    local_flat_board[flat_index] = 0
    return (local_full_board, local_flat_board)


def return_to_last_choice(flat_index):
    local_full_board = global_full_board
    local_flat_board = list(chain(*local_full_board))
    for undoing_index in range(flat_index, -1, -1):
        row_index, col_index = get_matrix_references(
            undoing_index, global_board_size
        )
        undone_full_board, undone_flat_board = local_undo_one_value(
            undoing_index,
            local_full_board,
            local_flat_board,
            row_and_col_index=(row_index, col_index)
        )
        allowed_values = generate_allowed_values(
            undone_full_board,
            undone_flat_board,
            row_index,
            col_index,
            global_board_size
        )
        # print(local_flat_board[undoing_index])
        # print(f"running the local undo undoing_index- {undoing_index} human row_and_col_index={(row_index + 1, col_index + 1)}| allowed {allowed_values} | length {len(allowed_values)}\n")
        # print(get_row(local_full_board, row_index))
        # print(get_column(local_full_board, global_board_size, col_index))
        if (len(allowed_values) > 1):
            return {
                "row_index": row_index,
                "col_index": col_index,
                "full_board": local_full_board,
                "flat_board": local_flat_board,
                "undone_index": undoing_index
            }
    return {
        "row_index": 0,
        "col_index": 0,
        "full_board": generate_empty_board(global_board_size),
        "flat_board": list(chain(*generate_empty_board(global_board_size))),
        "undone_index": 0
    }


if __name__ == "__main__":
    global_board_size = 9
    do_not_use = {}
    test_obj = {}
    global_full_board = generate_empty_board(global_board_size)
    # full_board[0] = [0, 2, 3, 4, 5, 6, 7, 8, 9]
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
            global_flat_board,
            row_index,
            col_index,
            global_board_size
        )
        shuffle(allowed_values)
        if (len(allowed_values) > 0):
            update_board(
                row_index,
                col_index,
                global_board_size,
                allowed_values[0]
            )
            i += 1
        else:
            existing_row, existing_column = get_row_and_column(
                global_full_board,
                global_full_board,
                global_board_size,
                row_index,
                col_index
            )

            undone = return_to_last_choice(i)

            global_full_board = undone["full_board"]
            global_flat_board = undone["flat_board"]
            i = undone["undone_index"]
            if (i == 0):
                do_not_use = {}
                test_array = {}

        if (len(allowed_values) == 1):
            test_obj[i] = ((row_index, col_index))
        elif (i in test_obj):
            del test_obj[i]

    for key, (row_i, col_i) in test_obj.items():
        print(f"(row, col) ({row_i + 1}, {col_i + 1}) can be changed")
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
