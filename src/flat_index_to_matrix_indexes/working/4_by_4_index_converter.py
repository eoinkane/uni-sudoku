from itertools import chain
import decimal

full = [[2, 3, 1, 4], [4, 1, 3, 2], [3, 4, 2, 1], [1, 2, 4, 3]]  # grid 1
# full = [[2, 1, 3, 4], [4, 3, 1, 2], [1, 2, 4, 3], [3, 4, 2, 1]]  # grid 2
# flat = [2, 3, 1, 4, 4, 1, 3, 2, 3, 4, 2, 1, 1, 2, 4, 3]
flat = list(chain(*full))
# positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
positions = [x for x in range(len(flat))]
randomed_positions = [5, 3, 8, 0, 3, 2, 6, 4, 7, 10, 14, 11, 9, 12, 15, 13]

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


for index, position in enumerate(randomed_positions):
    # if (index > 0):
    #    break
    print(f"index {index} - random position {position}")
    flat_list_value = flat[position]
    print(f"flat list value {flat_list_value}")
    position_modulus = position % 4
    print(f"position modulus {position_modulus}")
    # print(f" nearest {round(position/3)}")

    # nearest = (round(position/4))
    nearest = int(decimal.Decimal(position / 4).to_integral_value())
    nearest_modulus = nearest % 4
    if (position_modulus == 3):
        row_index = nearest - 1
        print("assigning col_index - line 13")
        col_index = nearest
        if (nearest_modulus == 0):
            col_index -= 1
        elif (nearest_modulus == 1):
            col_index += 2
        elif (nearest_modulus == 2):
            col_index += 1
    else:
        row_index = nearest
        if (position_modulus == 0):
            print("assigning col_index - line 18")
            if (nearest_modulus == 0):
                col_index = nearest
            elif (nearest_modulus == 2):
                col_index -= 3
            elif (nearest_modulus == 3):
                print('line 47')
                col_index -= 1
            else:
                col_index = nearest - 1
        else:
            print("assigning col_index - line 21")
            col_index = nearest
            # if (nearest_modulus == 2):
            #     col_index -= 1
            if (nearest_modulus == 0):
                print('line 54')
                col_index -= 2
                row_index -= 1
            elif (nearest_modulus == 2 and position_modulus == 2):
                print("line 58")
                row_index -= 1
            elif (nearest_modulus == 3 and position_modulus == 2):
                print("line 61")
                row_index -= 1
                col_index -= 1
            elif (nearest_modulus == 2):
                col_index -= 1
            elif (nearest_modulus == 3):
                col_index -= 2
                # print(f"row index post modify {row_index}")
    # if (col_index == 3):
    #     col_index = col_index - 1
    print(f"col_index = {col_index}")
    print(f"row_index = {row_index}")
    print(f"nearest = {nearest} | (nearest % 3) = {nearest_modulus}")
    print("\n\n")
    assert flat_list_value in full[row_index]
    assert flat_list_value == full[row_index][col_index]
