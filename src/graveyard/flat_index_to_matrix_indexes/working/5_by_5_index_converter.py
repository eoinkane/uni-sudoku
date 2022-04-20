from itertools import chain
import decimal

full = [[2, 5, 1, 3, 4], [5, 1, 4, 2, 3], [5, 2, 4, 1, 3], [4, 5, 3, 1, 2], [2, 5, 4, 1, 3]]  # grid 1
# full = [[1, 4, 3, 5, 2], [1, 3, 4, 2, 5], [4, 2, 1, 3, 5], [3, 2, 5, 4, 1], [2, 3, 1, 5, 4]]  # grid 2
flat = list(chain(*full))
# positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
positions = [x for x in range(len(flat))]
randomed_positions = [21, 12, 13, 8, 10, 14, 18, 3, 15, 23, 22, 0, 24, 20, 17, 2, 7, 9, 6, 4, 1, 16, 5, 19, 11]

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


for index, position in enumerate(randomed_positions):
    print(f"index {index} - random position {position}")
    flat_list_value = flat[position]
    print(f"flat list value {flat_list_value}")
    position_modulus = position % 5
    print(f"position modulus {position_modulus}")

    nearest = int(decimal.Decimal(position / 5).to_integral_value())
    nearest_modulus = nearest % 5
    if (position_modulus == 4):
        row_index = nearest - 1
        print("assigning col_index - line 29 - used")
        col_index = nearest
        if (nearest_modulus == 0):
            # print("line 32 - used')
            col_index -= 1
        elif (nearest_modulus == 1):
            # print("line 35 - used')
            col_index += 3
        elif (nearest_modulus == 2):
            # print("line 38 - used')
            col_index += 2
        elif (nearest_modulus == 3):
            # print("line 41 - used')
            col_index += 1
    else:
        row_index = nearest
        if (position_modulus == 0):
            print("assigning col_index - line 40 - used")
            if (nearest_modulus == 0):
                # print("line 48 - used')
                col_index = nearest
            elif (nearest_modulus == 2):
                # print("line 51 - used')
                col_index -= 1
            elif (nearest_modulus == 3):
                # print("line 55 - used')
                col_index -= 3
            elif (nearest_modulus == 4):
                # print("line 58 - used')
                col_index -= 4
            else:
                col_index = nearest - 1
        else:
            print("assigning col_index - line 60 - used")
            col_index = nearest
            if (nearest_modulus == 0 and position_modulus == 3):
                # print("line 68 - used')
                col_index -= 2
                row_index -= 1
            elif (nearest_modulus == 0 and position_modulus == 1):
                # print("line 72 - used')
                col_index += 1
            elif (nearest_modulus == 0):
                # print("line 74 - used')
                col_index += 2
            elif (nearest_modulus == 1 and position_modulus == 3):
                # print("line 78 - used')
                col_index += 2
                row_index -= 1
            elif (nearest_modulus == 1 and position_modulus == 2):
                # print("line 82 - used')
                col_index += 1
            elif (nearest_modulus == 2 and position_modulus == 2):
                # print("line 85")
                row_index -= 1
            elif (nearest_modulus == 3 and position_modulus == 1):
                # print("line 97 - used')
                col_index -= 2
            elif (nearest_modulus == 3 and position_modulus == 2):
                # print("line 84 - used")
                col_index -= 1
            elif (nearest_modulus == 4 and position_modulus == 1):
                # print("line 99 - used')
                col_index -= 3
            elif (nearest_modulus == 4 and position_modulus == 3):
                # print("line 102 - used')
                row_index -= 1
                col_index -= 1
            elif (nearest_modulus == 2):
                # print("line 106 - used')
                col_index -= 1
            elif (nearest_modulus == 4):
                # print("line 109 - used')
                col_index -= 2
    print(f"col_index = {col_index}")
    print(f"row_index = {row_index}")
    print(f"nearest = {nearest} | (nearest % 5) = {nearest_modulus}")
    print("\n\n")
    assert row_index >= 0 and col_index >= 0
    assert flat_list_value in full[row_index]
    assert flat_list_value == full[row_index][col_index]
