import json
import os
from datetime import datetime
from typing import Dict, Union
from utils.enums import Difficulty
from utils.custom_types import Board, Hints


def create_save(
    solution_board: Board,
    playing_board: Board,
    initial_board: Board,
    board_size: int,
    difficulty: Difficulty,
    hints_enabled: bool
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
            "hints_enabled": hints_enabled,
            "game_completed": False,
            "hints": {}
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
    hints: Hints
):
    previous_save = read_save(save_file_name)
    previous_save["playing_board"] = playing_board
    if (hints_enabled):
        previous_save["hints"] = hints
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


def list_saves() -> Dict[str, Union[str, Difficulty]]:
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
    return saved_games
