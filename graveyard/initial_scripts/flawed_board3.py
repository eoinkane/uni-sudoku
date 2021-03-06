from itertools import chain
from random import randint, sample, choice


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
    full_board = [[0 for x in range(9)] for x in range(9)]
    # first_three_in_column = sample(
    #     [x for x in range(1, 10) if x not in full_board[0][0:3]], 2
    # )
    # first_column = [full_board[0][0], *first_three_in_column, *sample(
    #     [x for x in range(1, 10) if x not in first_three_in_column], 6
    # )]
    # full_board.append([first_column[0], *sample([x for x in range(1, 10) if x != first_column[0]], 8)])
    # for i in range(1, 9):
    #     full_board.append([first_column[i], *[x - x for x in range(8)]])

    transposed_full_board = [list(sublist) for sublist in list(zip(*full_board))]

    # first sub grid section
    # sub_grid_indexes1 = get_sub_grid_indexes(1)
    # sub_grid1 = get_sub_grid(sub_grid_indexes1, full_board, 1)
    # flattened_sub_grid = list(chain(*sub_grid))

    try:
        for row_index, row in enumerate(full_board):
            for column_index, value in enumerate(row):
                current_area = 3 * round((column_index + 2) / 3)
                sub_grid_id = int(current_area / 3)
                sub_grid_indexes = get_sub_grid_indexes(sub_grid_id)
                print(sub_grid_indexes)
                print(sub_grid_id)
                sub_grid = get_sub_grid(sub_grid_indexes, full_board, sub_grid_id)
                existing_row = row[0:current_area]
                existing_column = transposed_full_board[column_index][0:current_area]
                incrementations = 0
                allowed_values = [x for x in range(1, 10) if x not in existing_row and x not in existing_column and x not in list(chain(*sub_grid))]
                while value == 0:
                    print(f"re running while - row_index = {row_index}" +
                          f" column_index - {column_index}")
                    print(len(allowed_values))
                    print(allowed_values)
                    r_int = choice(allowed_values)
                    print(f"generated random = {r_int}")
                    if r_int not in list(chain(*sub_grid)) and r_int not in existing_row:
                        # print(existing_row)
                        sub_grid[row_index % 3][column_index % 3] = r_int
                        full_board[row_index][column_index] = r_int
                        transposed_full_board[column_index][row_index] = r_int
                    incrementations += 1
                    if (incrementations >= 9):
                        print('debug')
                        print([x for x in range(1, 10) if x not in existing_row and x not in existing_column and x not in list(chain(*sub_grid))])
                        print(randint(6, 6))
                        print(existing_row)
                        print(get_sub_grid(sub_grid_indexes, full_board, 2))
                        print(list(chain(*get_sub_grid(sub_grid_indexes, full_board, sub_grid_id))))
                        break
    except Exception:
        print('except')
        if (len([x for x in [full_board[3]] if x != 0]) - 1) > 0:
            print('generated into the 3rd row')

    # flattened_board = list(chain(*full_board))

    # print(flattened_board)
    print("    _____________________________________")
    for row_index, row in enumerate(full_board):
        print(f"{row_index + 1} - | {' | '.join(str(item) for item in row)} |")
    print("    ??????????????????????????????????????????????????????????????????????????")

    # print(sub_grid[0])
    # print(first_column[0:3])

    return None


if __name__ == "__main__":
    main()
