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
    save_file_name = f"{datetime.now().isoformat()}_{difficulty.name}.json"
    with open(f"saves/{save_file_name}", 'w', encoding='utf-8') as f:
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
    with open(f"saves/{save_file_name}", 'r', encoding='utf-8') as f:
        return json.load(f)


def write_save(save_file_name, save):
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
    previous_save = read_save(save_file_name)
    previous_save["playing_board"] = playing_board
    previous_save["hints_enabled"] = hints_enabled
    previous_save["stats_enabled"] = stats_enabled
    previous_save["hints"] = hints
    previous_save["on_turn_no"] = on_turn_no
    previous_save["turns"] = turns
    previous_save["time_elapsed_secs"] = calculate_seconds_elapsed(
        starting_time
    )
    write_save(save_file_name, previous_save)


def complete_save(save_file_name: str):
    previous_save = read_save(save_file_name)
    previous_save["game_completed"] = True
    write_save(save_file_name, previous_save)


def check_if_there_are_saved_games():
    return len(
        [
            file_path for file_path
            in os.listdir("./saves")
            if file_path.endswith(".json")]
    ) > 0


def split_up_file_path(file_path: str):
    return (file_path.split(".j")[0]).split('_')


def list_saves() -> Dict[str, Union[str, Difficulty]]:
    file_paths = []
    saved_games = []
    for file_path in os.listdir("./saves"):
        if file_path.endswith(".json"):
            file_paths.append(file_path)
    for file_path in file_paths:
        split_file_path = split_up_file_path(file_path)
        timestamp = datetime.fromisoformat(split_file_path[0])
        difficulty = Difficulty[split_file_path[1]]
        saved_games.append({
            "difficulty": difficulty,
            "timestamp": timestamp,
            "file_path": file_path
        })
    saved_games.sort(key=lambda x: x["timestamp"], reverse=True)
    return saved_games


def get_difficulty_from_save_file_name(
    save_file_name: str
) -> Difficulty:
    return Difficulty[split_up_file_path(save_file_name)[1]]


def get_datetime_from_save_file_name(
    save_file_name: str
) -> str:
    return datetime.fromisoformat(
        split_up_file_path(save_file_name)[0]
    )
