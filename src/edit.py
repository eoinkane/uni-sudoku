from typing import Tuple

flat = [1, 2, 3, 4, 5, 6, 7, 8, 9]
positions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
randomed_positions = [5, 3, 8, 0, 3, 2, 6, 4, 7]
full = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def get_matrix_reference(position: int) -> Tuple[int, int]:
    position_modulus = position % 3
    nearest = (round(position/3))
    nearest_modulus = nearest % 3
    if (position_modulus == 2):
        row_index = nearest - 1
        col_index = nearest
        if (nearest_modulus == 0):
            col_index -= 1
        elif (nearest_modulus == 1):
            col_index += 1
    else:
        if (position_modulus == 0):
            if (nearest_modulus == 0):
                col_index = nearest
            elif (nearest_modulus == 2):
                col_index = nearest - 2
            else:
                col_index = nearest - 1
        else:
            col_index = nearest
            if (nearest_modulus == 2):
                col_index -= 1
        row_index = nearest
    return (row_index, col_index)


for index, position in enumerate(randomed_positions):
    row_index, col_index = get_matrix_reference(position)
    assert flat[position] in full[row_index]
    assert flat[position] == full[row_index][col_index]

print("can successfully generate matrix refs")
