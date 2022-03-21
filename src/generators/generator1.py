from random import choice, sample
from itertools import chain

def print_board(full_board):
    print("    ______________________________________________")
    for print_row_index, print_row in enumerate(full_board):
        print(f"{print_row_index + 1} - | {' | '.join(stg if len(stg) == 2 else stg.zfill(2) for stg in [str(item) for item in print_row])} |")
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


def get_matrix_references(flat_position: int, board_size: int):
    if (flat_position > (board_size ** 2)):
        raise Exception('Position greater than sample')
    row_index, col_index = divmod(flat_position, 9)
    return row_index, col_index


def get_row(full_board, row_index):
    return full_board[row_index]


def get_column(flat, board_size, col_index):
    return [val for ind, val in enumerate(flat) if ind % board_size == col_index]


def get_row_and_column(full_board, flat, board_size, row_index, col_index):
    return get_row(full_board, row_index), get_column(flat, board_size, col_index)


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


def main():
    board_size = 9
    # full_board = [sample([j+i*9 for j in range(1, 10)], 9) for i in range(9)]
    full_board = [sample([0 for j in range(1, 10)], 9) for i in range(9)]
    flat = list(chain(*full_board))
    no_of_positions = len(flat)
    positions = [x for x in range(len(flat))]
    randomed_positions = sample(positions, 81)

    print_board(full_board)
    # assert len(flat) == len(set(flat))

    iterations = 0
    # retry = False
    # do_not_use = []

    while iterations < no_of_positions:
        index = iterations
        random_position = randomed_positions[index]
        iterations += 1
        # if index > 0:
        #     break
        print(f"---\nrandom position - {random_position}")
        print(f"index - {index}")
        print(f"current value - {flat[random_position]}")
        row_index, col_index = get_matrix_references(random_position, board_size)
        print(f"col_index - {col_index} row_index - {row_index}")

        existing_row, existing_column = get_row_and_column(full_board, flat, board_size, row_index, col_index)

        sub_grid_id = ((col_index // 3) + 1) * (row_index // 3 + 1)
        print(f"sub_grid_id - {sub_grid_id}")

        sub_grid_indexes = get_sub_grid_indexes(sub_grid_id)
        sub_grid = get_sub_grid(sub_grid_indexes, full_board, sub_grid_id)

        allowed_values = [x for x in range(1, 10) if x not in existing_row and x not in existing_column and x not in list(chain(*sub_grid))]
        # allowed_values = [x for x in range(1, 10) if x not in existing_row and x not in existing_column and x not in list(chain(*sub_grid)) and x not in do_not_use]

        print('\nrow')
        print(existing_row)

        print('\ncolumn')
        print(existing_column)

        print('\nallowed_values')
        print(allowed_values)

        if (len(allowed_values) > 0):
            r_int = choice(allowed_values)
            flat[random_position] = r_int
            full_board[row_index][col_index] = r_int
            # if (retry is True):
            #     do_not_use = []
            #     retry = False
        else:
            print(f"\nfailed at index - {index}\n")
            break
        #     retry = True
        #     previous_random_position = randomed_positions[index - 1]
        #     print(previous_random_position)
        #     print(flat[previous_random_position])
        #     previous_row_index, previous_col_index = get_matrix_references(previous_random_position, board_size)

        #     do_not_use.append(flat[previous_random_position])
        #     flat[previous_random_position] = 0
        #     full_board[previous_row_index][previous_col_index] = 0
        #     iterations -= 2
        #     break

        # print(f"sub grid id - {sub_grid_id}")

    return full_board


if __name__ == '__main__':
    board = main()
    print_board(board)
