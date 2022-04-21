
import string
from typing import Tuple, Dict
from itertools import chain
from .custom_types import (
    Board,
    Column_References,
    Flat_Board,
    Row,
    Column,
    Do_Not_Use
)


def get_column_references(board: Board) -> Column_References:
    """create the column references for the given board 

    Args:
        board (Board): 2-D version (matrix) of the current sudoku board

    Returns:
        Column_References: a list of the letters to represent the columns on the board
    """ # noqa
    return list(string.ascii_lowercase[0:len(board[0])].upper())


def get_sub_grid_indexes(grid_id: int) -> Dict[str, list[int]]:
    """calculate the column and row indexes for a given sub grid id

    Args:
        grid_id (int): the sub grid id to calculate for

    Raises:
        Exception: when an invalid grid id is given

    Returns:
        Dict[str, list[int]]: the column and row indexes for the sub grid id
    """
    # raise an exception if an invalid grid id is received
    if (grid_id < 1 or grid_id > 9):
        raise Exception("invalid input to get_sub_grid_indexes")

    # initialise the variable
    column_indexes = None
    # handle the sub grids on the first sub grids row (the 1st 3 sub grids)
    if (grid_id <= 3):
        # calculate the sub grid indexes
        column_indexes = [
            x - 1 for x in [x + (3 * (grid_id - 1)) for x in range(1, 4)]
        ]
        row_indexes = [x for x in range(3)]
    elif (grid_id % 3 == 1):
        # calculate the row indexes
        row_indexes = [x for x in range(grid_id - 1, grid_id + 2)]
    elif (grid_id % 3 == 2):
        # calculate the row indexes
        row_indexes = [x for x in range(grid_id - 2, grid_id + 1)]
    else:
        # calculate the row indexes
        row_indexes = [x for x in range(grid_id - 3, grid_id)]

    # calculate the column indexes if they haven't been already
    if (column_indexes is None):
        column_indexes = [
            x - 1 for x in [
                x + (3 * ((grid_id - 1) % 3)) for x in range(1, 4)
            ]]

    # return a dictionary containing the sub grid indexes
    return {
        "row_indexes": row_indexes,
        "column_indexes": column_indexes
    }


def get_sub_grid(sub_grid_indexes, board: Board, grid_id: int) -> Board:
    """get a sub grid from within a sudoku board

    Args:
        sub_grid_indexes (Dict[str, list[int]]): the sub grid indexes
        board (Board): 2-D version (matrix) of the current sudoku board
        grid_id (int): the selected sub grid id

    Returns:
        Board: the sub grid of the given board
    """
    # get the sub grid indexes for the given id
    sub_grid_indexes = get_sub_grid_indexes(grid_id)
    # return the values from the board that are within the sub grid indexes
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
    """generate an empty 2-D version (matrix) of a sudoku board

    Args:
        board_size (int): size of the sudoku board

    Returns:
        Board: 2-D version (matrix) empty sudoku board
    """
    return [
        [0 for j in range(board_size)]
        for i in range(board_size)
    ]


def get_matrix_references(
    flat_position: int,
    board_size: int
) -> Tuple[int, int]:
    """get the row and column index for a given flat position

    Args:
        flat_position (int): the flat position on the 1-D sudoku board
        board_size (int): size of the sudoku board

    Raises:
        Exception: when the given flat position is out of range of the suodku board size

    Returns:
        Tuple(int, int): the row and column index for the flat position
    """ # noqa
    # raise an exception if an invalid flat position is received
    if (flat_position > (board_size ** 2)):
        raise Exception('Position greater than sample')
    # calculate the row and column index
    row_index, col_index = divmod(flat_position, 9)
    # return the row and column index
    return row_index, col_index


def get_row(full_board: Board, row_index: int) -> Row:
    """get a row from within a sudoku board

    Args:
        full_board (Board): 2-D version (matrix) of the current sudoku board
        row_index (int): the row to get

    Returns:
        Row: the subset of values from the sudoku board in the given row
    """
    return full_board[row_index]


def get_column(full_board, col_index) -> Column:
    """get a column from within a sudoku board

    Args:
        full_board (_type_): 2-D version (matrix) of the current sudoku board
        col_index (_type_): the column to get

    Returns:
        Column: the subset of values from the sudoku board in the given column
    """
    return list(list(zip(*full_board))[col_index])


def get_row_and_column(
    full_board: Board,
    row_index: int,
    col_index: int
) -> Tuple[Row, Column]:
    """get a row and column from within the sudoku board

    Args:
        full_board (Board): 2-D version (matrix) of the current sudoku board
        row_index (int): the row to get
        col_index (int): the column to get

    Returns:
        Tuple[Row, Column]: the given row and column from within the board
    """
    return (
        get_row(full_board, row_index),
        get_column(full_board, col_index)
    )


def update_board(
    full_board: Board,
    flat_board: Flat_Board,
    row_index: int,
    col_index: int,
    board_size: int,
    value: int
        ) -> Tuple[Board, Flat_Board]:
    """update a sudoku board with a given value

    Args:
        full_board (Board): 2-D version (matrix) of the current sudoku board
        flat_board (Flat_Board): 1-D version of the current sudoku board
        row_index (int): the row index of the position to update
        col_index (int): the row index of the position to update
        board_size (int): size of the sudoku board
        value (int): the value to insert into the sudoku board

    Returns:
        Tuple[Board, Flat_Board]: _description_
    """
    # update the matrix sudoku board
    full_board[row_index][col_index] = value

    # update the flat 1-D suodku board
    # for some reason the following line was introducing a bug in the game,
    #  I think it was to do with copying by reference vs value but I couldn't resolve it, # noqa 
    #  so the flat board had to be recalculated every time
    # flat_board[(row_index * board_size) + col_index]
    flat_board = list(chain(*full_board))
    # return the updated sudoku board
    return (full_board, flat_board)


def generate_allowed_values(
    local_full_board: Board,
    row_index: int,
    col_index: int,
    board_size: int,
    do_not_use: Do_Not_Use
) -> list[int]:
    """calculate the allowed values for a given position on the sudoku board 

    Args:
        local_full_board (_type_): 2-D version (matrix) of the current sudoku board
        row_index (int): the row index of the position to update
        col_index (int): the row index of the position to update
        board_size (int): size of the sudoku board
        do_not_use (Do_Not_Use): a dictionary of values not to use for a board position

    Returns:
        list[int]: the allowed valus at the given position
    """ # noqa

    # get the row and column of the given position
    existing_row, existing_column = get_row_and_column(
        local_full_board,
        row_index,
        col_index
    )

    # get the sub grid of the given position
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

    # get the values that should not be used for the given position
    local_do_not_use = []
    if (((row_index * board_size) + col_index) in do_not_use):
        local_do_not_use = do_not_use[((row_index * board_size) + col_index)]

    # calculated values that can be allowed at the given position
    allowed_values = [
        x for x in range(1, (board_size + 1))
        if x not in existing_row
        and x not in existing_column
        and x not in local_do_not_use
        and x not in list(chain(*sub_grid))
    ]
    return allowed_values


def convert_grid_reference_to_matrix_reference(
    grid_reference: str
) -> Tuple[int, int]:
    """convert a display grid reference to a matrix reference

    Args:
        grid_reference (str): the grid reference, e.g. A1

    Returns:
        Tuple[int, int]: the row and column index for the given grid ref
    """
    return (ord(grid_reference[0].lower()) - 97, (int(grid_reference[1]) - 1))


def convert_matrix_reference_to_grid_reference(
    row_index: int,
    col_index: int
) -> str:
    """convert a matrix reference to a display grid reference

    Args:
        row_index (int): the row index of the position
        col_index (int): the row index of the position

    Returns:
        str: the grid reference for the given matrix ref e.g. A1
    """

    return f"{chr(row_index + 97).upper()}{col_index + 1}"
