
import string
from .custom_types import Board, Column_References


def get_column_references(board: Board) -> Column_References:
    return list(string.ascii_lowercase[0:len(board[0])].upper())
