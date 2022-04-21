import json
import os
from datetime import datetime, timedelta
from typing import Dict, Union
from utils.enums import Difficulty
from utils.custom_types import Board, Hints
from utils.time import calculate_seconds_elapsed


def create_save(
    solution_board: Board,
    playing_board: Board,
    initial_board: Board,
    board_size: int,
    difficulty: Difficulty,
    hints_enabled: bool,
    stats_enabled: bool,
    timer_enabled: bool,
    timer_duration: timedelta
) -> str:
    """This function creates a saved game file to represent the sudoku game and allow the player to continue at a later date

    Args:
        solution_board (Board): 2-D version (matrix) of the sudoku board solution
        playing_board (Board): 2-D version (matrix) of the current sudoku board
        initial_board (Board): 2-D version (matrix) of the initial sudoku board
        board_size (int): size of the sudoku board
        difficulty (Difficulty): difficulty level the game has been created using
        hints_enabled (bool): should the hints be enabled
        stats_enabled (bool): should the stats be enabled
        timer_enabled (bool): should the timer be enabled
        timer_duration (timedelta): Duration of the timer

    Returns:
        str: the filename that points to the saved game just created
    """ # noqa

    # save the file by the created date and time as well as the difficulty
    save_file_name = f"{datetime.now().isoformat()}_{difficulty.name}.json"
    print()

    # write out to that file
    with open(f"saves/{save_file_name}", 'w', encoding='utf-8') as f:
        # save the data in JSON format
        json.dump({
            "solution_board": solution_board,
            "initial_board": initial_board,
            "playing_board": playing_board,
            "board_size": board_size,
            "difficulty": difficulty.value,
            "turns": [],
            "on_turn_no": -1,
            "time_elapsed_secs": 0,
            "hints_enabled": hints_enabled,
            "stats_enabled": stats_enabled,
            "game_completed": False,
            "hints": {},
            "timer_enabled": timer_enabled,
            "timer_duration_secs": timer_duration.seconds
        }, f)
    return save_file_name


def read_save(save_file_name: str):
    """Read a given saved game file by key

    Args:
        save_file_name (str): saved game file key

    Returns:
        Dict: saved game data
    """
    # read the given saved game file
    with open(f"saves/{save_file_name}", 'r', encoding='utf-8') as f:
        # convert the raw json to a python dictionary
        return json.load(f)


def write_save(
    save_file_name: str,
    save: Dict
):
    """Write out to a given saved game file by key

    Args:
        save_file_name (str): saved game file key
        save (Dict): a python dictionary to output to the JSON file
    """
    with open(f"saves/{save_file_name}", 'w', encoding='utf-8') as f:
        json.dump(save, f)


def update_save(
    save_file_name: str,
    playing_board: Board,
    hints_enabled: bool,
    stats_enabled: bool,
    hints: Hints,
    on_turn_no: int,
    turns,
    starting_time: datetime
):
    """update an already created save

    Args:
        save_file_name (str): saved game file key
        playing_board (Board): 2-D version (matrix) of the current sudoku board
        hints_enabled (bool): should the hints be enabled
        stats_enabled (bool): should the stats be enabled
        hints (Hints): the datastore to represent the hints for the player
        on_turn_no (int): the number of turns that have been made by the player
        turns (list): the turns that have been made by the player
        starting_time (datetime): the datetime representation of when the game started
    """ # noqa

    # read the save from the file
    previous_save = read_save(save_file_name)

    # update the values within the save
    previous_save["playing_board"] = playing_board
    previous_save["hints_enabled"] = hints_enabled
    previous_save["stats_enabled"] = stats_enabled
    previous_save["hints"] = hints
    previous_save["on_turn_no"] = on_turn_no
    previous_save["turns"] = turns
    previous_save["time_elapsed_secs"] = calculate_seconds_elapsed(
        starting_time
    )

    # write the save back to file now that the values have been updated
    write_save(save_file_name, previous_save)


def complete_save(save_file_name: str):
    """Mark a saved game file as completed

    Args:
        save_file_name (str): saved game file key
    """

    # read the save from the file
    previous_save = read_save(save_file_name)

    # update the value within the save
    previous_save["game_completed"] = True

    # write the save back to file now that the value have been updated
    write_save(save_file_name, previous_save)


def check_if_there_are_saved_games() -> bool:
    """Figure out if any saved games can be continued

    Returns:
        bool: Can any saved games be continued
    """
    return len(
        [
            file_path for file_path
            in os.listdir("./saves")
            if file_path.endswith(".json")]
    ) > 0


def split_up_file_path(file_path: str):
    """Split the file path by its seperators

    Args:
        file_path (str): saved game file key

    Returns:
        List: A list containing the saved game difficulty and created datetime
    """
    return (file_path.split(".j")[0]).split('_')


def list_saves() -> Dict[str, Union[str, Difficulty]]:
    """Read the saves folder to list the existing saved game files

    Returns:
        Dict[str, Union[str, Difficulty]]: a list of the saved game files
    """
    file_paths = []
    saved_games = []
    for file_path in os.listdir("./saves"):
        if file_path.endswith(".json"):
            # make a list of all the saved game files in the saves folder
            file_paths.append(file_path)

    # construct a dictionary of the saved game file properties for each file path # noqa
    for file_path in file_paths:
        split_file_path = split_up_file_path(file_path)
        timestamp = datetime.fromisoformat(split_file_path[0])
        difficulty = Difficulty[split_file_path[1]]
        saved_games.append({
            "difficulty": difficulty,
            "timestamp": timestamp,
            "file_path": file_path
        })

    # sort the saved games by created datetime
    saved_games.sort(key=lambda x: x["timestamp"], reverse=True)
    return saved_games


def get_difficulty_from_save_file_name(
    save_file_name: str
) -> Difficulty:
    """Split a given saved game file key and return the Difficulty enum of that saved game file

    Args:
        save_file_name (str): saved game file key

    Returns:
        Difficulty: Difficulty level of a saved game file
    """ # noqa
    return Difficulty[split_up_file_path(save_file_name)[1]]


def get_datetime_from_save_file_name(
    save_file_name: str
) -> str:
    """Split a given saved game file key and return the created datetime of that saved game file

    Args:
        save_file_name (str): saved game file key

    Returns:
        str: created datetime of a given saved game file
    """ # noqa
    return datetime.fromisoformat(
        split_up_file_path(save_file_name)[0]
    )
