from typing import Tuple
from datetime import datetime
from utils.validation import validate_grid_reference_input
from utils.board import convert_grid_reference_to_matrix_reference
from utils.custom_types import Column_References
from utils.enums import Difficulty, Action
from utils.time import figure_out_time_difference
from save_handlers.save_handlers import list_saves


def decide_action() -> Action:
    print("\nPlease select the next action you would like to take: \n"
          + " \n".join(
              [f"{action.value} - {action.name}" for action in Action]
            )
          )
    print("Please input the number next to the difficulty you would like "
          "to select and then press enter")
    recieved_action = False
    while not recieved_action:
        raw_action = input()
        if (
            raw_action.isdigit() and
            int(raw_action)
            in [action.value for action in Action]
        ):
            recieved_action = True
        else:
            print(f"'{raw_action}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return Action(int(raw_action))


def select_difficulty() -> Difficulty:
    print("\nPlease select a difficulty level: \n"
          + " \n".join(
              [
                  f"{diff.value} - {diff.name}" for diff in Difficulty
              ]
            ))
    print("Please input the number next to the difficulty you would like "
          "to select and then press enter")
    recieved_difficulty = False
    while not recieved_difficulty:
        raw_difficulty = input()
        if (
            raw_difficulty.isdigit() and
            int(raw_difficulty)
            in [difficulty.value for difficulty in Difficulty]
        ):
            recieved_difficulty = True
        else:
            print(f"'{raw_difficulty}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return Difficulty(int(raw_difficulty))


def select_grid_reference(
    column_references: Column_References,
    board_size: int
) -> Tuple[Tuple[int, int], str]:
    print("Please input the A1 grid reference you would like to select "
          "and then press enter")
    recieved_grid_reference = False
    while not recieved_grid_reference:
        raw_grid_reference = input()
        if (validate_grid_reference_input(
            raw_grid_reference,
            column_references,
            board_size
                )):
            recieved_grid_reference = True
        else:
            print(f"'{raw_grid_reference}' is not a valid A1 grid " +
                  "reference. You can use the column and row values " +
                  "displayed above. Please try again.")
    return convert_grid_reference_to_matrix_reference(
            raw_grid_reference
            ), raw_grid_reference


def select_hints_enabled() -> bool:
    print("\nPlease select if hints should be enabled: \n"
          + " \n".join(
              [
                  "1 - Hints Disabled",
                  "2 - Hints Enabled"
              ]
            ))
    print("Please input the number next to the option you would like "
          "to select and then press enter")
    recieved_hints_enabled = False
    while not recieved_hints_enabled:
        raw_hints_enabled = input()
        if (
            raw_hints_enabled.isdigit() and
            int(raw_hints_enabled)
            in [1, 2]
        ):
            recieved_hints_enabled = True
        else:
            print(f"'{raw_hints_enabled}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    return bool(int(raw_hints_enabled) - 1)


def select_position_value(
        raw_grid_ref: str,
        board_size: int) -> int:
    print(f"Please input the number you would like to enter at {raw_grid_ref} "
          f"between 1 and {board_size} and then press enter"
          )
    recieved_number = False
    while not recieved_number:
        raw_number = input()
        if (
            len(raw_number) == 1 and
            raw_number[0].isdigit() and
            int(raw_number[0]) in [x for x in range(0, (board_size + 1))]
        ):
            recieved_number = True
        else:
            print(
                f"{raw_number} is not a valid input. "
                f"Please enter a number between 1 and {board_size}"
            )
    return int(raw_number)


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


def select_saved_game() -> str:
    now = datetime.now()
    saved_games = list_saves()
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
