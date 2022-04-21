from typing import Tuple
from datetime import datetime, timedelta
from utils.validation import validate_grid_reference_input
from utils.board import convert_grid_reference_to_matrix_reference
from utils.custom_types import Column_References
from utils.enums import Difficulty, Action, TimerDuration
from utils.time import figure_out_time_difference, format_datetime_to_string
from save_handlers.save_handlers import list_saves


def decide_action() -> Action:
    """Allow the player to select an action to take

    Returns:
        Action: the selected action that the player chose
    """

    # Display all the allowed options and ask for input
    print("\nPlease select the next action you would like to take: \n"
          + " \n".join(
              [f"{action.value} - {action.name}" for action in Action]
            )
          )
    print("Please input the number next to the action you would like "
          "to take and then press enter")

    # Loop until a valid input is received
    recieved_action = False
    while not recieved_action:
        # recieve the input
        raw_action = input()
        # check if the input is valid
        if (
            len(raw_action) == len(str(len(Action))) and
            raw_action.isdigit() and
            int(raw_action)
            in [action.value for action in Action]
        ):
            # allow the code to exit the loop
            recieved_action = True
        else:
            # display a message asking for valid input
            print(f"'{raw_action}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    # return the enum that the player chose
    return Action(int(raw_action))


def select_difficulty() -> Difficulty:
    """Allow the player to select the difficulty to play

    Returns:
        Difficulty: the selected difficulty that the player chose
    """
    # Display all the allowed options and ask for input
    print("\nPlease select a difficulty level: \n"
          + " \n".join(
              [
                  f"{diff.value} - {diff.name}" for diff in Difficulty
              ]
            ))
    print("Please input the number next to the difficulty you would like "
          "to select and then press enter")

    # Loop until a valid input is received
    recieved_difficulty = False
    while not recieved_difficulty:
        # recieve the input
        raw_difficulty = input()
        # check if the input is valid
        if (
            raw_difficulty.isdigit() and
            int(raw_difficulty)
            in [difficulty.value for difficulty in Difficulty]
        ):
            # allow the code to exit the loop
            recieved_difficulty = True
        else:
            # display a message asking for valid input
            print(f"'{raw_difficulty}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    # return the enum that the player chose
    return Difficulty(int(raw_difficulty))


def select_grid_reference(
    column_references: Column_References,
    board_size: int
) -> Tuple[Tuple[int, int], str]:
    """Allow the player to select a grid reference

    Args:
        column_references (Column_References): the display columns (letters)
        board_size (int): size of the sudoku board

    Returns:
        Tuple[Tuple[int, int], str]: A tuple containing the row_index & col_index in a nested tuple and the display grid reference
    """ # noqa
    # Explain what input is needed and ask for input
    print("\nPlease input the A1 grid reference you would like to select "
          "and then press enter")

    # Loop until a valid input is received
    recieved_grid_reference = False
    while not recieved_grid_reference:
        # recieve the input
        raw_grid_reference = input()
        # check if the input is valid
        if (validate_grid_reference_input(
            raw_grid_reference,
            column_references,
            board_size
                )):
            # allow the code to exit the loop
            recieved_grid_reference = True
        else:
            # display a message asking for valid input
            print(f"'{raw_grid_reference}' is not a valid A1 grid " +
                  "reference. You can use the column and row values " +
                  "displayed above. Please try again.")
    # return the grid_reference that the player chose
    return convert_grid_reference_to_matrix_reference(
            raw_grid_reference
            ), raw_grid_reference


def select_stats_enabled() -> bool:
    """Allow the player to select if stats should be enabled

    Returns:
        bool: should the stats be enabled
    """

    # Display all the allowed options and ask for input
    print("\nPlease select if stats should be enabled: \n"
          + " \n".join(
              [
                  "1 - Stats Disabled",
                  "2 - Stats Enabled"
              ]
            ))
    print("Please input the number next to the option you would like "
          "to select and then press enter")

    # Loop until a valid input is received
    recieved_stats_enabled = False
    while not recieved_stats_enabled:
        # recieve the input
        raw_stats_enabled = input()
        # check if the input is valid
        if (
            raw_stats_enabled.isdigit() and
            int(raw_stats_enabled)
            in [1, 2]
        ):
            # allow the code to exit the loop
            recieved_stats_enabled = True
        else:
            # display a message asking for valid input
            print(f"'{raw_stats_enabled}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    # return whether the player chose to enable stats
    return bool(int(raw_stats_enabled) - 1)


def select_hints_enabled() -> bool:
    """Allow the player to select if hints should be enabled

    Returns:
        bool: should the hints be enabled
    """

    # Display all the allowed options and ask for input
    print("\nPlease select if hints should be enabled: \n"
          + " \n".join(
              [
                  "1 - Hints Disabled",
                  "2 - Hints Enabled"
              ]
            ))
    print("Please input the number next to the option you would like "
          "to select and then press enter")

    # Loop until a valid input is received
    recieved_hints_enabled = False
    while not recieved_hints_enabled:
        # recieve the input
        raw_hints_enabled = input()
        # check if the input is valid
        if (
            raw_hints_enabled.isdigit() and
            int(raw_hints_enabled)
            in [1, 2]
        ):
            # allow the code to exit the loop
            recieved_hints_enabled = True
        else:
            # display a message asking for valid input
            print(f"'{raw_hints_enabled}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    # return whether the player chose to enable hints
    return bool(int(raw_hints_enabled) - 1)


def select_timer_enabled(selected_difficulty: Difficulty) -> bool:
    """Allow the player to select if the timer should be enabled

    Args:
        selected_difficulty (Difficulty): the difficulty level to figure out the corresponding timer duration

    Returns:
        bool: should the timer be enabled
    """ # noqa

    # get the corresponding timer duration for the given difficulty
    difficulty_name = selected_difficulty.name
    difficulty_timer = TimerDuration[difficulty_name]

    # Display all the allowed options and ask for input
    print("\nPlease select if the timer should be enabled: \n" +
          f"Since you selected {difficulty_name} difficulty the " +
          f"timer would be {difficulty_timer.value} minutes\n" +
          " \n".join(
              [
                  "1 - Timer Disabled",
                  "2 - Timer Enabled"
              ]
            ))
    print(
        "The game will automatically end after this time.\n"
        "Please input the number next to the option you would like "
        "to select and then press enter"
    )

    # Loop until a valid input is received
    recieved_timer_enabled = False
    while not recieved_timer_enabled:
        # recieve the input
        raw_timer_enabled = input()
        # check if the input is valid
        if (
            raw_timer_enabled.isdigit() and
            int(raw_timer_enabled)
            in [1, 2]
        ):
            # allow the code to exit the loop
            recieved_timer_enabled = True
        else:
            # display a message asking for valid input
            print(f"'{raw_timer_enabled}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")

    # return whether the player chose to enable the timer and if so also return the timer duration # noqa
    if (int(raw_timer_enabled) == 1):
        return False, None
    else:
        return True, timedelta(minutes=difficulty_timer.value)


def select_position_value(
        raw_grid_ref: str,
        board_size: int) -> int:
    """Allow the player to input a number to insert at the selected position

    Args:
        raw_grid_ref (str): the display string for grid reference
        board_size (int): size of the sudoku board

    Returns:
        int: the number selected by the player
    """

    # Explain what input is needed and ask for input
    print(f"Please input the number you would like to enter at {raw_grid_ref} "
          f"between 1 and {board_size} and then press enter"
          )

    # Loop until a valid input is received
    recieved_number = False
    while not recieved_number:
        # recieve the input
        raw_number = input()
        # check if the input is valid
        if (
            len(raw_number) == 1 and
            raw_number[0].isdigit() and
            int(raw_number[0]) in [x for x in range(0, (board_size + 1))]
        ):
            # allow the code to exit the loop
            recieved_number = True
        else:
            # display a message asking for valid input
            print(
                f"{raw_number} is not a valid input. "
                f"Please enter a number between 1 and {board_size}"
            )
    # return the chosen number
    return int(raw_number)


def decide_whether_to_play_saved_game() -> bool:
    """Allow the player to select if a saved game should be continued

    Returns:
        bool: should a saved game be continued
    """

    # Display all the allowed options and ask for input
    print("\nPlease select if you want to play a saved game: \n"
          + " \n".join(
              [
                  "1 - Start a New Game",
                  "2 - Continue a Saved Game"
              ]
            ))
    print("Please input the number next to the option you would like "
          "to select and then press enter")

    # Loop until a valid input is received
    recieved_use_saved_game = False
    while not recieved_use_saved_game:
        # recieve the input
        raw_use_saved_game = input()
        # check if the input is valid
        if (
            len(raw_use_saved_game) == 1 and
            raw_use_saved_game.isdigit() and
            int(raw_use_saved_game)
            in [1, 2]
        ):
            # allow the code to exit the loop
            recieved_use_saved_game = True
        else:
            # display a message asking for valid input
            print(f"'{raw_use_saved_game}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    # return whether the player chose to continue a saved game
    return bool(int(raw_use_saved_game) - 1)


def select_saved_game() -> str:
    """Allow the player to select a saved game to continue

    Returns:
        str: the saved game file path the player chose
    """

    # figure out the time differences between now and created dates
    now = datetime.now()
    saved_games = list_saves()
    time_differences = [
        figure_out_time_difference(
            saved_game["timestamp"],
            now
        ) for saved_game in saved_games
    ]

    # create a dynamic max option length for validation
    option_index_max_length = len(str(saved_games.index(saved_games[-1])))

    # Display all the allowed options and ask for input
    saved_games_display_list = [
        (
            f"{index + 1} - Difficulty: {saved_game['difficulty'].name} "
            f"Created: "
            f"{format_datetime_to_string(saved_game['timestamp'])},"
            f" {difference}")
        for index, (saved_game, difference) in enumerate(
            zip(saved_games, time_differences)
        )
    ]
    print("\nPlease select the saved game you would like to continue: \n"
          + " \n".join(saved_games_display_list))
    print("Please input the number next to the option you would like "
          "to select and then press enter")

    # Loop until a valid input is received
    recieved_use_saved_game = False
    while not recieved_use_saved_game:
        # recieve the input
        raw_saved_game = input()
        if (
            len(raw_saved_game) == option_index_max_length and
            raw_saved_game.isdigit() and
            int(raw_saved_game)
            in [x for x in range(0, (len(saved_games) + 1))]
        ):
            # allow the code to exit the loop
            recieved_use_saved_game = True
        else:
            # display a message asking for valid input
            print(f"'{raw_saved_game}' is not a valid selection " +
                  "You can select the numbers displayed " +
                  "above. Please try again.")
    # return the saved game the player chose
    return saved_games[int(raw_saved_game) - 1]['file_path']
