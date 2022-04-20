from itertools import chain
from random import randint, sample


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
    full_board = [sample([x for x in range(1, 10)], 9)]
    first_three_in_column = sample(
        [x for x in range(1, 10) if x not in full_board[0][0:3]], 2
    )
    first_column = [full_board[0][0], *first_three_in_column, *sample(
        [x for x in range(1, 10) if x not in first_three_in_column], 6
    )]
    # full_board.append([first_column[0], *sample([x for x in range(1, 10) if x != first_column[0]], 8)])
    for i in range(1, 9):
        full_board.append([first_column[i], *[x - x for x in range(8)]])

    # first sub grid section
    sub_grid_indexes1 = get_sub_grid_indexes(1)
    sub_grid1 = get_sub_grid(sub_grid_indexes1, full_board, 1)
    # flattened_sub_grid = list(chain(*sub_grid))

    for row_index in sub_grid_indexes1["row_indexes"]:
        for column_index in sub_grid_indexes1["column_indexes"]:
            while full_board[row_index][column_index] == 0:
                # print(f"re running while - row_index = {row_index}" +
                #       f" column_index - {column_index}")
                r_int = randint(1, 9)
                print(f"generated random = {r_int}")
                if r_int not in list(chain(*sub_grid1)):
                    sub_grid1[row_index][column_index] = r_int
                    full_board[row_index][column_index] = r_int

    sub_grid_indexes2 = get_sub_grid_indexes(2)
    sub_grid2 = get_sub_grid(sub_grid_indexes2, full_board, 2)

    for row_index in sub_grid_indexes2["row_indexes"]:
        existing_row = full_board[row_index][0:sub_grid_indexes2["column_indexes"][0]]
        for column_index in sub_grid_indexes2["column_indexes"]:
            incrementations = 0
            while full_board[row_index][column_index] == 0:
                print(f"re running while - row_index = {row_index}" +
                      f" column_index - {column_index}")
                r_int = randint(1, 9)
                print(f"generated random = {r_int}")
                if r_int not in list(chain(*get_sub_grid(sub_grid_indexes2, full_board, 2))) and r_int not in existing_row:
                    print(existing_row)
                    sub_grid2[row_index % 3][column_index % 3] = r_int
                    full_board[row_index][column_index] = r_int
                incrementations += 1
                if (incrementations >= 9):
                    print([x for x in range(1, 10) if x not in existing_row and x not in list(chain(*get_sub_grid(sub_grid_indexes2, full_board, 2)))])
                    print(randint(6, 6))
                    print(existing_row)
                    print(get_sub_grid(sub_grid_indexes2, full_board, 2))
                    print(list(chain(*get_sub_grid(sub_grid_indexes2, full_board, 2))))
                    break

    # iterations = 0
    # number_of_filled_cells_target = randint(36, 41)
    # while (
    #     len(
    #         [x for x in flattened_board if x == 0]
    #       ) >= number_of_filled_cells_target):
    #     iterations += 1
    #     print(f"generating a number {iterations} random int: {randint(1,9)}")
    #     flattened_board[iterations] = iterations

    # for i in range(8):
    #     if i <= 2:
    #         first_row_deque.rotate(3)
    #     elif i >= 3 and i <= 5:
    #         first_row_deque.rotate(4)
    #     else:
    #         first_row_deque.rotate(5)
    #     full_board.append(list(first_row_deque))

    # flattened_board = list(chain(*full_board))

    # print(flattened_board)
    print("    _____________________________________")
    for row_index, row in enumerate(full_board):
        print(f"{row_index + 1} - | {' | '.join(str(item) for item in row)} |")
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

    # print(sub_grid[0])
    # print(first_column[0:3])

    return None


if __name__ == "__main__":
    main()
