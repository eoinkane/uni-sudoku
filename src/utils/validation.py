from utils.custom_types import Column_References


def validate_grid_reference_input(
        raw_grid_reference: str,
        column_references: Column_References,
        board_size: int
) -> bool:
    return (
        len(raw_grid_reference) == 2 and
        raw_grid_reference[0].lower().isalpha() and
        raw_grid_reference[1].isdigit() and
        raw_grid_reference[0].upper() in column_references and
        int(raw_grid_reference[1]) in [x for x in range(1, (board_size + 1))]
    )
