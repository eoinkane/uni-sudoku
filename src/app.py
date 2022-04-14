import os
from datetime import datetime
from copy import deepcopy
from itertools import chain
from data.game1 import data
from typing import Dict, Tuple
from utils.custom_types import (
    Board,
    Column_References,
    Generation,
    Flat_Board,
    Hints
)
from utils.screen import (
    clear_screen,
    print_sudoku_board,
    print_edit_and_original_sudoku_board,
    print_edit_and_original_sudoku_board_with_hints
)
from utils.board import (
    get_column_references,
    update_board,
    generate_allowed_values
)
from utils.user_input_helpers import (
    decide_action,
    select_position_value,
    select_hints_enabled,
    select_difficulty,
    select_grid_reference
)
from utils.enums import Action, Difficulty
from generators.board_generator import generate_board
from save_handlers.save_handlers import (
    complete_save,
    create_save,
    update_save,
    read_save
)
from utils.time import figure_out_time_difference


def help():
    print(
        "To complete a game of Sudoku you must fill all "
        "the empty positions on the board with a number between 1 and 9."
    )
    print(
        "This Python Sudoku game represents the board using A1 notation, "
        "similar to Battleships."
    )
    print(
        "Dependening on the difficulty level you select, a varying amount of "
        "board positions will be pre-populated. "
        "These positions cannot be edited."
    )
    print(
        "However, there are rules about placing what "
        "numbers can be placed and where."
    )
    print(
        "To complete the game there can be no repeatition of numbers in any "
        "column, row or sub grid. If there is already a number 1 in position "
        "A1, then 1 cannot be repeated in row A and column 1 "
        "or the first sub grid."
    )
    print(
        "You can decide if you want to enable hints at the start of this game."
        " If hints are enabled and you enter an invalid number then a '?' will"
        "appear on the board next to that number, if hints are disabled "
        "then you will not be shown where your mistake is."
    )


def welcome():
    clear_screen()
    print("Welcome to the Python Sudoku Game")
    help()
    print("\nPress enter to continue")
    input()


def take_turn(
    unedited_full_board: Board,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    column_references: Column_References,
    hints_enabled: bool,
    hints: Hints
) -> Tuple[Tuple[Board, Flat_Board], Dict[str, str]]:
    row_index: int = None
    col_index: int = None
    raw_grid_ref: str = None

    user_selected_a_editable_grid_ref = False
    while not user_selected_a_editable_grid_ref:
        (row_index, col_index), raw_grid_ref = select_grid_reference(
            column_references,
            board_size
        )
        if (unedited_full_board[row_index][col_index] == 0):
            user_selected_a_editable_grid_ref = True
        else:
            print("That grid ref is populated by the original board."
                  " Please see the board on the left and reselect a grid ref"
                  )
    position_value = select_position_value(
        raw_grid_ref,
        board_size,
    )

    if hints_enabled:
        hint_key = f"{row_index}{col_index}"
        allowed_values = generate_allowed_values(
            playing_full_board,
            row_index,
            col_index,
            board_size,
            {}
        )
        if (
            position_value != 0 and
            position_value not in allowed_values
           ):
            hints[hint_key] = "?"
        elif (
            (hint_key in hints and position_value == 0) or
            (hint_key in hints and position_value in allowed_values)
        ):
            del hints[hint_key]

    playing_full_board, playing_flat_board = update_board(
            playing_full_board,
            playing_flat_board,
            row_index,
            col_index,
            board_size,
            int(position_value)
        )
    return ((
        playing_full_board,
        playing_flat_board
        ),
        hints
    )


def complete_game(
    completed_board: Board,
    board_size: int,
    column_references: Column_References
):
    clear_screen()
    print("Congratulations, you completed the sudoku game! "
          "Here is the completed board")
    print_sudoku_board(
        completed_board,
        board_size,
        column_references,
        should_clear_screen=False
    )


def game(
    generation: Board,
    board_size: int,
    hints_enabled: bool,
    save_file_name: str
):
    unedited_full_board: Board = deepcopy(generation["empty_full_board"])
    playing_full_board: Board = deepcopy(generation["empty_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))

    game_completed = False
    hints = {}

    column_references = get_column_references(unedited_full_board)

    print_board_func = (
        print_edit_and_original_sudoku_board if not hints_enabled
        else print_edit_and_original_sudoku_board_with_hints
    )

    while not game_completed:
        print_board_func(
            unedited_full_board,
            playing_full_board,
            board_size,
            column_references,
            hints=hints
        )
        action = decide_action()

        if (action == Action.TAKE_TURN):
            print_board_func(
                unedited_full_board,
                playing_full_board,
                board_size,
                column_references,
                hints=hints
            )
            (playing_full_board, playing_flat_board), hints = take_turn(
                unedited_full_board,
                playing_full_board,
                playing_flat_board,
                board_size,
                column_references,
                hints_enabled,
                hints
            )
        update_save(
            save_file_name,
            playing_full_board,
            hints_enabled,
            hints
        )
        if (
            len([x for x in playing_flat_board if x == 0]) == 0 and
            playing_flat_board == generation["filled_flat_board"]
        ):
            game_completed = True
            complete_save(save_file_name)
            complete_game(playing_full_board, board_size, column_references)


def decide_whether_to_play_new_or_saved_game(board_size: int):
    use_saved_game = decide_whether_to_play_saved_game()

    if check_if_there_are_saved_games() and use_saved_game:
        save_file_path = select_saved_game()
        save = read_save(save_file_path)
        generation = {
            "filled_full_board": save["solution_board"],
            "filled_flat_board": list(chain(*save["solution_board"])),
            "empty_full_board": save["playing_board"],
            "empty_flat_board": list(chain(*save["playing_board"]))
        }
        return generation, (
            save["hints_enabled"],
            save_file_path
        )
    else:
        if (use_saved_game):
            print(
                "\nThere are no saved games available for you to continue. "
                "Please create a new one."
            )
        difficulty = select_difficulty()
        hints_enabled = select_hints_enabled()
        generation: Generation = generate_board(board_size, difficulty)

        save_file_name = create_save(
            generation["filled_full_board"],
            generation["empty_full_board"],
            board_size,
            difficulty,
            hints_enabled
        )
        return generation, (
            hints_enabled,
            save_file_name
        )


def decide_whether_to_play_saved_game() -> bool:
    print("\nPlease select if you want to play a saved game: \n"
          + " \n".join(
              [
                  "1 - Start a New Game",
                  "2 - Continue a Saved Game"
              ]
            ))
    print("Please input the number next to the option you would like "
          "to select and then press enter")
    recieved_use_saved_game = False
    while not recieved_use_saved_game:
        raw_use_saved_game = input()
        if (
            len(raw_use_saved_game) == 1 and
            raw_use_saved_game.isdigit() and
            int(raw_use_saved_game)
            in [1, 2]
        ):
            recieved_use_saved_game = True
        else:
            print(f"'{raw_use_saved_game}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return bool(int(raw_use_saved_game) - 1)


def check_if_there_are_saved_games():
    return len([file_path for file_path in os.listdir("./saves") if file_path.endswith(".json")]) > 0


def select_saved_game() -> str:
    now = datetime.now()
    file_paths = []
    saved_games = []
    for file_path in os.listdir("./saves"):
        if file_path.endswith(".json"):
            file_paths.append(file_path)
    for file_path in file_paths:
        split_file_path = (file_path.split(".j")[0]).split('_')
        timestamp = datetime.fromisoformat(split_file_path[0])
        difficulty = Difficulty[split_file_path[1]]
        saved_games.append({
            "difficulty": difficulty,
            "timestamp": timestamp,
            "file_path": file_path
        })
    saved_games.sort(key=lambda x: x["timestamp"], reverse=True)
    time_differences = [
        figure_out_time_difference(
            saved_game["timestamp"],
            now
        ) for saved_game in saved_games
    ]
    option_index_max_length = len(str(saved_games.index(saved_games[-1])))
    saved_games_display_list = [
        (
            f"{index + 1} - Difficulty: {saved_game['difficulty'].name} "
            f"Created: "
            f"{saved_game['timestamp'].strftime('%m/%d/%Y, %H:%M:%S')},"
            f" {difference}")
        for index, (saved_game, difference) in enumerate(
            zip(saved_games, time_differences)
        )
    ]
    print("\nPlease select the saved game you would like to continue: \n"
          + " \n".join(saved_games_display_list))
    print("Please input the number next to the option you would like "
          "to select and then press enter")
    recieved_use_saved_game = False
    while not recieved_use_saved_game:
        raw_saved_game = input()
        if (
            len(raw_saved_game) == option_index_max_length and
            raw_saved_game.isdigit() and
            int(raw_saved_game)
            in [x for x in range(0, (len(saved_games) + 1))]
        ):
            recieved_use_saved_game = True
        else:
            print(f"'{raw_saved_game}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return saved_games[int(raw_saved_game) - 1]['file_path']


def main():
    board_size = 9
    welcome()

    generation, (hints_enabled, save_file_name) = (
        decide_whether_to_play_new_or_saved_game(board_size)
    )

    game(generation, board_size, hints_enabled, save_file_name)


if __name__ == "__main__":
    main()
    # if (decide_whether_to_play_saved_game()):
    #     print(select_saved_game())
    # else:
    #     print("creating new")
