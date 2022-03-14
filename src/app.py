
from data.game1 import data
from utils.custom_types import Board, Column_References
from utils.screen import clear_screen, print_sudoku_board
from utils.board import get_column_references


def validate_grid_reference_input(raw_grid_reference: str, column_references: Column_References) -> bool:
	return (
		len(raw_grid_reference) == 2 and
		raw_grid_reference[0].lower().isalpha() and 
		raw_grid_reference[1].lower().isdigit() and
		raw_grid_reference[0] in column_references 
	)


def select_grid_reference(column_references: Column_References):
	recieved_grid_reference = False
	while not recieved_grid_reference:
		print("Please input the A1 grid reference you would like to retrieve")
		raw_grid_reference = input()
		print("is valid " + str(validate_grid_reference_input(raw_grid_reference)))
		if (validate_grid_reference_input(raw_grid_reference)):
			recieved_grid_reference = True


def game(board: Board):
	board_height = len(board)
	board_width = len(board[0])
	column_references = get_column_references(board)
	print_sudoku_board(board, column_references)
	select_grid_reference(column_references)
	print()
		

if __name__ == "__main__":
	board: Board = data["board"]
	clear_screen()
	game(board)
