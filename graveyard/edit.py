from typing import Tuple
from itertools import chain
from random import sample
from .data.game1 import data
# import os

board = data["solution"]
# full = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
full = board
# flat = [1, 2, 3, 4, 5, 6, 7, 8, 9]
flat = list(chain(*full))
# positions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
positions = [x for x in range(len(flat))]
# randomed_positions = [5, 3, 8, 0, 3, 2, 6, 4, 7]
randomed_positions = sample(positions, len(positions))
# randomed_positions = [78, 20, 61, 7, 38, 33, 1, 47, 21, 75, 67, 19, 70, 74, 60, 42, 43, 79, 35, 24, 52, 30, 59, 22, 49, 13, 6, 4, 63, 18, 56, 71, 44, 11, 37, 68, 64, 50, 45, 16, 48, 57, 65, 14, 17, 58, 29, 27, 2, 15, 23, 5, 77, 51, 41, 54, 28, 66, 31, 53, 9, 73, 36, 69, 46, 32, 25, 10, 80, 8, 0, 3, 40, 12, 76, 39, 34, 72, 26, 55, 62] # row and column index is 9 not 9


def get_matrix_indexes(position: int) -> Tuple[int, int]:
    # os.system("clear")
    print("\n")
    position_modulus = position % 9
    nearest = (round(position/9))
    nearest_modulus = nearest % 9
    if position == 0:
        return (0, 0, position_modulus, nearest_modulus, nearest)
    if (position_modulus == 8):
        print('line 27')
        row_index = nearest - 1
        col_index = nearest
        if (nearest_modulus == 0):
            print('line 31 this works')
            col_index -= 1
        elif (nearest_modulus == 1):
            print('line 34')
            col_index += 1
    else:
        print('line 31')
        if (position_modulus == 0):
            print('line 33')
            if (nearest_modulus == 0):
                col_index = nearest
            elif (nearest_modulus == 2):
                col_index = nearest - 2
            else:
                col_index = nearest - 1
        else:
            print('line 41')
            # print(f"nearest modulus {nearest_modulus}")
            # print(f"position modulus {position_modulus}")
            col_index = nearest
            if (nearest_modulus == 0 and position_modulus == 1):
                print('line 52')
                col_index += 1
            elif (nearest_modulus == 2):
                print('line 55 this works')
                col_index -= 1
        row_index = nearest
    # return (row_index, col_index)
    return (row_index, col_index, position_modulus, nearest_modulus, nearest)


for index, position in enumerate(randomed_positions):
    row_index, col_index, position_modulus, nearest_modulus, nearest = get_matrix_indexes(position)
    try:
        assert flat[position] in full[row_index]
        assert flat[position] == full[row_index][col_index]
    except Exception as err:
        print("err:")
        print(err)
        print("flat:")
        print(flat)
        print("randomed_positions:")
        print(randomed_positions)
        print("    _____________________________________")
        for print_row_index, print_row in enumerate(full):
            print(f"{print_row_index + 1} - | {' | '.join(str(item) for item in print_row)} |")
        print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print(
            f"index {index} | " +
            f"position {position} | " +
            f"position modulus {position_modulus} | " +
            f"nearest {nearest} | " +
            f"nearest modulus {nearest_modulus} | " +
            f"value at flat[position] {flat[position]} | " +
            f"row index - {row_index} | " +
            f"col index {col_index}"
        )
        print('should be row index - 8 and col index - 6')
        exit(1)


print("can successfully generate matrix refs")
