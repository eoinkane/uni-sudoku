from datetime import timedelta
from typing import Dict, List, Union, Tuple

Board = List[List[int]]

Flat_Board = List[int]

Column_References = List[str]

Row = List[int]

Column = List[int]

Generation = Dict[str, Union[Board, Flat_Board, timedelta]]

Hints = Dict[str, str]

Game_Config = Tuple[
    Generation,
    Tuple[str, Tuple[str, Tuple[Tuple[bool, timedelta], Tuple[bool, Hints]]]],
]

Turn = Dict[str, int]

Turns = List[Turn]

Do_Not_Use = Dict[str, list[int]]
