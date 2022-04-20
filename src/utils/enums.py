from enum import Enum, auto


class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class TimerDuration(Enum):
    EASY = 10
    MEDIUM = 15
    HARD = 20


class Action(Enum):
    TAKE_TURN = auto()
    UNDO = auto()
    REDO = auto()
    SHOW_HELP = auto()
    QUIT = auto()
