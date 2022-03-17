flat = [1, 2, 3, 4, 5, 6, 7, 8, 9]
positions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
randomed_positions = [5, 3, 8, 0, 3, 2, 6, 4, 7]
full = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


for index, position in enumerate(randomed_positions):
    # if (index > 0):
    #    break
    print(f"index {index} - random position {position}")
    flat_list_value = flat[position]
    print(f"flat list value {flat_list_value}")
    position_modulus = position % 3
    print(f"position modulus {position_modulus}")
    # print(f" nearest {round(position/3)}")
    nearest = (round(position/3))
    nearest_modulus = nearest % 3
    if (position_modulus == 2):
        row_index = nearest - 1
        print(f"assigning col_index - line 13 - len {(len(flat) - 1)}")
        col_index = nearest
        if (nearest_modulus == 0):
            col_index -= 1
        elif (nearest_modulus == 1):
            col_index += 1
    else:
        if (position_modulus == 0):
            print("assigning col_index - line 18")
            if (nearest_modulus == 0):
                col_index = nearest
            elif (nearest_modulus == 2):
                col_index -= 2
            else:
                col_index = nearest - 1
        else:
            print("assigning col_index - line 21")
            col_index = nearest
            if (nearest_modulus == 2):
                col_index -= 1
        row_index = nearest
    # if (col_index == 3):
    #     col_index = col_index - 1
    print(f"col_index = {col_index}")
    print(f"nearest = {nearest} | (nearest % 3) = {nearest_modulus}")
    print("\n\n")
    assert flat_list_value in full[row_index]
    assert flat_list_value == full[row_index][col_index]
