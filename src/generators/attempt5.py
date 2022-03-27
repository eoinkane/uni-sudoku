from random import choice, sample, shuffle
from itertools import chain


def print_board(full_board):
    print("    ______________________________________________")
    for print_row_index, print_row in enumerate(full_board):
        print(f"{print_row_index + 1} - | {' | '.join(stg if len(stg) == 2 else stg.zfill(2) for stg in [str(item) for item in print_row])} |")
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
    print("33")
    print(col_index)
    print_board_diff(full_board, 0, col_index)
    print(list(list(zip(*full_board))[col_index]))
    # quit()
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
    full_board[row_index][col_index] = value
    flat_board[(row_index * board_size) + col_index]


def generate_allowed_values(row_index, col_index, board_size):
    existing_row, existing_column = get_row_and_column(
        full_board,
        flat_board,
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
    sub_grid = get_sub_grid(sub_grid_indexes, full_board, sub_grid_id)
    allowed_values = [
        x for x in range(1, 10)
        if x not in existing_row
        and x not in existing_column
        and x not in list(chain(*sub_grid))
    ]
    return allowed_values


def is_valid_update(row_index, col_index, value, board_size,  **kwargs):
    allowed_values = kwargs.get('allowed_values', generate_allowed_values(
        row_index, col_index, board_size
        ))
    return value in allowed_values


global_board_size = 9
global_full_board = []
global_flat_board = []

if __name__ == "__main__":
    full_board = generate_empty_board(global_board_size)
    # full_board[0] = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    flat_board = list(chain(*full_board))
    no_of_positions = global_board_size ** 2
    positions = [x for x in range(no_of_positions)]
    randomed_positions = [4, 54, 48, 25, 5, 59, 78, 58, 20, 49, 53, 27, 62, 21, 22, 41, 32, 79, 66, 0, 46, 45, 13, 68, 67, 26, 12, 47, 39, 51, 42, 37, 52, 14, 11, 72, 69, 65, 75, 44, 23, 50, 24, 17, 28, 31, 63, 73, 56, 34, 7, 18, 74, 33, 57, 71, 15, 8, 2, 1, 30, 60, 9, 38, 29, 3, 16, 43, 70, 61, 35, 10, 64, 80, 55, 19, 77, 36, 40, 6, 76]
    # randomed_positions = sample(positions, no_of_positions)

    print_board(full_board)
    # print(flat_board)
    # print(positions)
    # print(randomed_positions)

    for i in range(no_of_positions):
        # if i == 1:
        #     break
        print(f"running for i {i}")
        row_index, col_index = get_matrix_references(
            i, global_board_size
        )
        print(f"row {row_index} col {col_index}")
        allowed_values = generate_allowed_values(row_index, col_index, global_board_size)
        print(allowed_values)
        numbers = [x for x in range(1, 10)]
        shuffle(allowed_values)
        if (len(allowed_values) > 0):
            update_board(row_index, col_index, global_board_size, allowed_values[0])
        if (i == 71):
            print_board(full_board)
            existing_row, existing_column = get_row_and_column(
                full_board,
                flat_board,
                global_board_size,
                row_index,
                col_index
            )
            print("debug line")
            print(existing_row)
            print(f"row {row_index + 1} col {col_index + 1}")
            # quit()
        print("-----\n")
    print_board(full_board)
    print(len([x for x in list(chain(*full_board)) if x == 0]))
