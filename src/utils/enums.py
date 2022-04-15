from enum import Enum, auto


class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class Action(Enum):
    TAKE_TURN = auto()
    QUIT = auto()
