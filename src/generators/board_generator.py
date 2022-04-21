from random import choice, shuffle
from itertools import chain
from typing import Dict, Tuple, Union
from copy import deepcopy
from utils.board import (
    generate_empty_board,
    get_matrix_references,
    update_board,
    generate_allowed_values,
    )
from utils.enums import Difficulty
from utils.custom_types import (
    Board,
    Flat_Board,
    Do_Not_Use,
    Turns
)


def print_board(full_board: Board):
    """a debugging display function that was used while developing this board generator

    Args:
        full_board (Board): the board to print out to the screen
    """ # noqa
    print("      1    2    3    4    5    6    7    8    9")
    print("    ______________________________________________")
    for print_row_index, print_row in enumerate(full_board):
        print(f"{print_row_index + 1} - | {' | '.join(stg if len(stg) == 2 else stg.zfill(2) for stg in [str(item) for item in print_row]).replace('00', '  ')} |")
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


def print_board_diff(
    full_board: Board,
    changed_row_index: int,
    changed_col_index: int
):
    """a debugging display function that was used while developing this board generator

    Args:
        full_board (Board): the board to print out to the screen
        changed_row_index (int): the row index to highlight
        changed_col_index (int): the column index to highlight
    """ # noqa
    changed_txt = '+'
    un_changed_txt = ' '
    print("    _______________________________________________________")
    for print_row_index, print_row in enumerate(full_board):
        print(f"{print_row_index + 1} - | {' | '.join((stg if len(stg) == 2 else stg.zfill(2)) + f'{changed_txt if (print_row_index == changed_row_index) and (stg_index == changed_col_index) else un_changed_txt}' for stg_index, stg in enumerate([str(item) for item in print_row]))} |")
    print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


def local_undo_one_value(
        flat_index: int,
        local_full_board: Board,
        local_flat_board: Flat_Board,
        board_size: int,
        do_not_use: Do_Not_Use,
        **kwargs
) -> Tuple[Board, Flat_Board]:
    """a helper function to undo a value that was generated.
    this function is used when a no more valid values,
    can be filled in a sudoku board so some previous values have to be removed.

    Args:
        flat_index (int): the position being reset
        local_full_board (Board): 2-D version (matrix) of the sudoku board being generated
        local_flat_board (Flat_Board): 1-D version of the sudoku board being generated
        board_size (int): size of the sudoku board
        do_not_use (Do_Not_Use): a dictionary of values not to use for a board position

    Keyword Args:
        row_and_col_index (Tuple[int, int]): the row and column index to undo.
            default: is calculated from the flat index

    Returns:
        Tuple[Board, Flat_Board]: _description_
    """ # noqa

    # get the row and column index from the kwargs
    row_index, col_index = kwargs.get(
        "row_and_col_index",
        get_matrix_references(
            flat_index, board_size
        )
    )

    # record the value that lead to a dead end,
    # sudoku generation in the do not use dict
    if ((flat_index) not in do_not_use):
        do_not_use[flat_index] = []
    do_not_use[flat_index].append(local_flat_board[flat_index])

    # reset the sudoku board position to 0
    local_full_board[row_index][col_index] = 0
    local_flat_board[flat_index] = 0
    return (local_full_board, local_flat_board)


def return_to_last_choice(
    full_board: Board,
    board_size: int,
    flat_index: int,
    do_not_use: Do_Not_Use
) -> Dict[str, Union[int, Board, Flat_Board]]:
    """a function to figure out the last position that had multiple allowed values.
    this function is used when a no more valid values,
    can be filled in a sudoku board so some generated values have to be reset.

    Args:
        full_board (Board): 2-D version (matrix) of the sudoku board being generated
        board_size (int): size of the sudoku board
        flat_index (int): the postion that could not be generated past
        do_not_use (Do_Not_Use): a dictionary of values not to use for a board position

    Returns:
        Dict[str, Union[int, Board, Flat_Board]]: the most recent position
            that was generated with a choice of values
    """ # noqa

    # create the variabled for the function
    local_full_board = full_board
    local_flat_board = list(chain(*local_full_board))

    # loop with a decreasing counter from the current position
    for undoing_index in range(flat_index, -1, -1):
        # get the row and column index for the current loop iteration
        row_index, col_index = get_matrix_references(
            undoing_index, board_size
        )
        # reset the value generated at the matrix ref
        undone_full_board, undone_flat_board = local_undo_one_value(
            undoing_index,
            local_full_board,
            local_flat_board,
            board_size,
            do_not_use,

            row_and_col_index=(row_index, col_index)
        )
        # figure out the allowed values for the matrix ref
        allowed_values = generate_allowed_values(
            undone_full_board,
            row_index,
            col_index,
            board_size,
            do_not_use
        )

        # if there is more than one allowed value for the matrix ref,
        # then the board generator can return to this position and try again
        if (len(allowed_values) > 1):
            return {
                "row_index": row_index,
                "col_index": col_index,
                "full_board": local_full_board,
                "flat_board": local_flat_board,
                "undone_index": undoing_index
            }
    # if the loop exits without returning,
    #  then there are no positions that had multiple choices
    # when this happens then the board generator,
    #  has to restart and use a blank board
    empty_board = generate_empty_board(board_size)
    return {
        "row_index": 0,
        "col_index": 0,
        "full_board": empty_board,
        "flat_board": list(chain(*empty_board)),
        "undone_index": 0
    }


def generate_board(
    board_size: int,
    difficulty: Difficulty
) -> Dict[str, Union[Board, Flat_Board, int, Turns, None]]:
    """a function to generate a random sudoku board,
    with a solution and board with positions emptied

    Args:
        board_size (int): size of the sudoku board to generate
        difficulty (Difficulty): difficulty level to create the sudoku board with

    Returns:
        Dict[str, Union[Board, Flat_Board, int, Turns, None]]: the generation of the sudoku board
    """ # noqa

    # create the initial values for the function
    do_not_use = {}
    global_full_board = generate_empty_board(board_size)
    global_flat_board = list(chain(*global_full_board))
    no_of_positions = board_size ** 2
    positions = [x for x in range(no_of_positions)]

    # loop through the positions on the board
    # use a while loop with a manual counter,
    # so that the loop counter can be increased and decreased
    i = 0

    while (i < no_of_positions):
        # get the row and column index for the current position
        row_index, col_index = get_matrix_references(
            i, board_size
        )
        # get the allowed values for the current position
        allowed_values = generate_allowed_values(
            global_full_board,
            row_index,
            col_index,
            board_size,
            do_not_use
        )
        # randomise the allowed values
        shuffle(allowed_values)
        # if there is more than one allowed value,
        # then the generator can continue and increment the loop counter
        if (len(allowed_values) > 0):
            # update the sudoku board with the randomly selected value
            global_full_board, global_flat_board, = update_board(
                global_full_board,
                global_flat_board,
                row_index,
                col_index,
                board_size,
                allowed_values[0]
            )
            i += 1
        # otherwise there is no valid values to continue the generator with,
        # so the generator must return to the last iteration with multiple
        # allowed values and make a different choice
        else:
            # get the config for the last iteration with either,
            #  multiple allowed value or an empty board to restart with
            undone = return_to_last_choice(
                global_full_board,
                board_size,
                i,
                do_not_use
            )

            # reassign the variables from the undone config
            global_full_board = undone["full_board"]
            global_flat_board = undone["flat_board"]
            i = undone["undone_index"]
            # if the generated has been restarted,
            #  then the do_not_use values can be reset
            if (i == 0):
                do_not_use = {}
    # the loop exits once a fully random,
    #  and valid sudoku board has been generated

    # create a copy of the full sudoku board
    empty_full_board = deepcopy(global_full_board)

    # pick a random amount of empty levels for each difficulty
    empty_levels = {
        Difficulty.EASY:  choice([x for x in range(40, 46)]),
        Difficulty.MEDIUM: choice([x for x in range(46, 50)]),
        Difficulty.HARD: choice([x for x in range(50, 54)])
    }

    # empty random positions on the sudoku board
    for i in range(empty_levels[difficulty]):
        # loop until a position has been emptied
        changed = False
        while not changed:
            # select a random position and get the matrix ref
            row_index, col_index = get_matrix_references(
                choice(positions),
                board_size
                )
            # empty that random position if not already
            if (empty_full_board[row_index][col_index] != 0):
                empty_full_board[row_index][col_index] = 0
                changed = True

    # return the generated full, initial and solution sudoku board,
    #  and other game config
    return {
        "solution_full_board": global_full_board,
        "solution_flat_board": list(chain(*global_full_board)),
        "initial_full_board": empty_full_board,
        "initial_flat_board": list(chain(*empty_full_board)),
        "playing_full_board": empty_full_board,
        "playing_flat_board": list(chain(*empty_full_board)),
        "on_turn_no": -1,
        "turns": [],
        "time_elapsed": None
    }


# a script section that was use to enable development of the board generator
if __name__ == "__main__":
    generation = generate_board(9)
    filled_full_board = generation["filled_full_board"]
    empty_full_board = generation["empty_full_board"]

    print_board(filled_full_board)
    print(len([x for x in list(chain(*filled_full_board)) if x == 0]))
    print_board(empty_full_board)
    print(len([x for x in list(chain(*empty_full_board)) if x == 0]))
