from random import choice, sample
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


def get_column(flat, board_size, col_index) -> list[int]:
    return [
        val for ind, val in
        enumerate(flat)
        if ind % board_size == col_index
    ]


def get_row_and_column(
    full_board,
    flat,
    board_size,
    row_index,
    col_index
        ):
    return (
        get_row(full_board, row_index),
        get_column(flat, board_size, col_index)
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


def make_loop_config(
    iterations: int,
    randomed_positions: list[int],
    board_size: int,
    full_board: list[list[int]],
    flat: list[int],
    do_not_use
        ):
    index = iterations
    random_position = randomed_positions[index]
    iterations += 1

    row_index, col_index = get_matrix_references(
        random_position,
        board_size
    )

    existing_row, existing_column = get_row_and_column(
        full_board,
        flat,
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
    # assert flat[random_position] in list(chain(*sub_grid))

    # assert flat[random_position] in sub_grid

    allowed_values = [
        x for x in range(1, 10)
        if x not in existing_row
        and x not in existing_column
        and x not in list(chain(*sub_grid))
        and x not in [
            y for y in (
                do_not_use[index]
                if index in do_not_use
                else []
            )
        ]
    ]
    return {
        'index': index,
        'iterations': iterations,
        'random_position': random_position,
        'row_index': row_index,
        'col_index': col_index,
        'existing_row': existing_row,
        'existing_column': existing_column,
        'sub_grid_col': sub_grid_col,
        'sub_grid_row': sub_grid_row,
        'sub_grid_id': sub_grid_id,
        'sub_grid_indexes': sub_grid_indexes,
        'sub_grid': sub_grid,
        'allowed_values': allowed_values
    }


def do_not_use_append(
    do_not_use: dict[int, list[int]],
    index: int,
    append_value: int
        ):
    if ((index - 1) not in do_not_use):
        do_not_use[index - 1] = []
    do_not_use[index - 1].append(append_value)
    return do_not_use


def cannot_redo_indexes_append(
    cannot_redo_indexes: list[int],
    index: int
        ):
    cannot_redo_indexes.append(index)
    return cannot_redo_indexes


def undo_generation(
    board_size: int,
    cannot_redo_indexes: list[int],
    do_not_use: dict[int, list[int]],
    flat: list[int],
    full_board: list[list[int]],
    index: int,
    iterations: int,
    randomed_positions: list[int],
    retry_counter: int
        ):


    previous_random_position = randomed_positions[
        index - retry_counter
    ]

    previous_row_index, previous_col_index = get_matrix_references(
        previous_random_position, board_size
    )

    do_not_use = do_not_use_append(
        do_not_use=do_not_use,
        index=index,
        append_value=flat[previous_random_position]
    )

    cannot_redo_indexes = cannot_redo_indexes_append(
        cannot_redo_indexes=cannot_redo_indexes,
        index=index
    )

    print(
        "line22 resetting vals - previous_random_position" +
        f"{previous_random_position} row - {previous_row_index} " +
        f"col - {previous_col_index}\n"
    )
    flat[previous_random_position] = 0
    full_board[previous_row_index][previous_col_index] = 0
    iterations -= (retry_counter + 1)
    # iterations -= retry_counter
    return {
        'previous_random_position': previous_random_position,
        'previous_row_index': previous_row_index,
        'previous_col_index': previous_col_index,
        'do_not_use': do_not_use,
        'cannot_redo_indexes': cannot_redo_indexes,
        'flat': flat,
        'full_board': full_board,
        'iterations': iterations
    }


def main():
    board_size = 9
    full_board = generate_empty_board(board_size)
    # full_board = [
    #     sample([j+i*9 for j in range(1, 10)],
    #            board_size)
    #     for i in range(board_size)
    # ]
    flat = list(chain(*full_board))
    no_of_positions = len(flat)
    positions = [x for x in range(len(flat))]
    randomed_positions = sample(positions, 81)

    print_board(full_board)

    iterations = 0
    retry = False
    previous_retry_counter = 0
    retry_counter = 0
    do_not_use: dict[int, list[int]] = {}
    cannot_redo_indexes: list[int] = []

    while iterations < no_of_positions:
        loop_config = make_loop_config(
            iterations=iterations,
            randomed_positions=randomed_positions,
            board_size=board_size,
            full_board=full_board,
            flat=flat,
            do_not_use=do_not_use,
        )
        index = loop_config['index']
        random_position = loop_config['random_position']
        iterations = loop_config['iterations']

        print(f"\n---\nrandom position - {random_position}")
        print(f"iteration - {iterations}")
        print(f"index - {index}")
        print(f"current value - {flat[random_position]}")
        row_index = loop_config['row_index']
        col_index = loop_config['col_index']
        print(f"col_index - {col_index} row_index - {row_index}")

        existing_row = loop_config['existing_row']
        existing_column = loop_config['existing_column']

        sub_grid_col = loop_config['sub_grid_col']
        print(f"sub_grid_col - {sub_grid_col}")

        sub_grid_row = loop_config['sub_grid_row']
        print(f"sub_grid_row - {sub_grid_row}")

        sub_grid_id = loop_config['sub_grid_id']
        print(f"sub_grid_id - {sub_grid_id}")

        sub_grid_indexes = loop_config['sub_grid_indexes']
        sub_grid = loop_config['sub_grid']

        allowed_values = loop_config['allowed_values']

        print('\nrow')
        print(existing_row)

        print('\ncolumn')
        print(existing_column)

        print(f"\ndo not use - do_not_use[{index}]")
        print(
            do_not_use[index]
            if index in do_not_use
            else []
        )

        print('\nallowed_values')

        if (len(allowed_values) > 0):
            r_int = choice(allowed_values)
            print(allowed_values, f" chosen value {r_int}")
            flat[random_position] = r_int
            full_board[row_index][col_index] = r_int
            print('\nnewboard:')
            print_board_diff(full_board, row_index, col_index)
            if (retry is True):
                print("resetting retry")
                # do_not_use = []

                retry = False
                previous_retry_counter = retry_counter
                retry_counter = 0
                # if (index in cannot_redo_indexes):
                #     cannot_redo_indexes.remove(index)
        else:
            print(allowed_values)
            print()
            """
            if (index in cannot_redo_indexes):
                print("need to redo")
                print(f"retry counter = {retry_counter}")
                print(f"previous retry counter = {previous_retry_counter}")
                print(f"index = {index}")
                print(f"cannot_redo_indexes = {cannot_redo_indexes}")
                for i in range(1, (previous_retry_counter + 1)):
                    print(f"theoritcally undoing  {i}")

                print(f"should be back to {iterations - previous_retry_counter}")
                quit()
                break
            else:
            """
            print(f"\nfailed at index - {index}\n")
            print('undoing once')
            # iterations, full_board, flat = reset_generation(board_size)
            # break
            print(f"current iter - {iterations} ")

            retry = True
            retry_counter += 1

            undo_config = undo_generation(
                board_size=board_size,
                cannot_redo_indexes=cannot_redo_indexes,
                do_not_use=do_not_use,
                flat=flat,
                full_board=full_board,
                index=index,
                iterations=iterations,
                randomed_positions=randomed_positions,
                retry_counter=retry_counter,
            )

            previous_random_position = (
                undo_config['previous_random_position']
            )
            print(f"previous_random_position - {previous_random_position}")

            previous_row_index = undo_config['previous_row_index']
            previous_col_index = undo_config['previous_col_index']

            print("value of previous generation - " +
                    f"{full_board[previous_row_index][previous_col_index]}"
                    )

            do_not_use = undo_config['do_not_use']

            # if ((index - 1) not in do_not_use):
            #     do_not_use[index - 1] = []
            # do_not_use[index - 1].append(flat[previous_random_position])
            # cannot_redo_indexes.append(index)
            cannot_redo_indexes = undo_config['cannot_redo_indexes']
            flat = undo_config['flat']
            full_board = undo_config['full_board']
            iterations = undo_config['iterations']
            # break
            # print(f"should do redo position ? next maybe - {iterations} ")
            # quit()

    return full_board


if __name__ == '__main__':
    board = main()
    print_board(board)
