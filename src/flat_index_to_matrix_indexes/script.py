from random import sample
from itertools import chain

full = [sample([x for x in range(1 * x, 10 * x)], 9) for x in range(1, 10)]

flat = list(chain(*full))

positions = [x for x in range(len(flat))]
randomed_positions = sample([x for x in range(81)], 81)

print("    ______________________________________________")
for print_row_index, print_row in enumerate(full):
    print(f"{print_row_index + 1} - | {' | '.join(stg if len(stg) == 2 else stg.zfill(2) for stg in [str(item) for item in print_row])} |")
print("    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


for index, position in enumerate(randomed_positions):
    quotient, remainder = divmod(position, 9)

    print(f"index {index} - random position {position}")
    flat_list_value = flat[position]
    print(f"target value {flat_list_value}")
    print(f"potential row {quotient}")
    print(f"potential col {remainder}")

    row_index = quotient
    col_index = remainder

    assert row_index >= 0 and col_index >= 0
    assert flat_list_value in full[row_index]
    assert flat_list_value == full[row_index][col_index]
