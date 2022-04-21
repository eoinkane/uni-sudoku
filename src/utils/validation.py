from utils.custom_types import Column_References


def validate_grid_reference_input(
        raw_grid_reference: str,
        column_references: Column_References,
        board_size: int
) -> bool:
    """helper function to check if a string is a valid grid reference

    Args:
        raw_grid_reference (str): the raw grid ref to validate
        column_references (Column_References): the list of column references for the current game
        board_size (int): size of the sudoku board

    Returns:
        bool: is the given grid reference valid
    """ # noqa
    return (
        len(raw_grid_reference) == 2 and
        raw_grid_reference[0].lower().isalpha() and
        raw_grid_reference[1].isdigit() and
        raw_grid_reference[0].upper() in column_references and
        int(raw_grid_reference[1]) in [x for x in range(1, (board_size + 1))]
    )
