from copy import deepcopy
from itertools import chain
from data.game1 import data
from utils.player_experience import (
    show_help,
    welcome,
    display_quit_message,
    display_unable_to_undo_turn_message,
    display_unable_to_redo_turn_message
)
from utils.game import (
    create_game_config,
    take_turn,
    complete_game,
    undo_turn,
    redo_turn
)
from utils.custom_types import (
    Board,
    Generation,
    Flat_Board,
    Hints
)
from utils.screen import (
    print_edit_and_original_sudoku_board,
    print_edit_and_original_sudoku_board_with_hints
)
from utils.board import (
    get_column_references
)
from utils.user_input_helpers import (
    decide_action,
)
from utils.enums import Action
from save_handlers.save_handlers import (
    complete_save,
    update_save,
)


def assign_print_board_func(hints_enabled):
    return (
        print_edit_and_original_sudoku_board if not hints_enabled
        else print_edit_and_original_sudoku_board_with_hints
    )


def game(
    generation: Generation,
    board_size: int,
    hints_enabled: bool,
    save_file_name: str,
    hints: Hints
):
    unedited_full_board: Board = deepcopy(generation["initial_full_board"])
    playing_full_board: Board = deepcopy(generation["playing_full_board"])
    playing_flat_board: Flat_Board = list(chain(*playing_full_board))
    turns = list(generation["turns"])
    on_turn_no = generation["on_turn_no"]

    game_completed = False

    column_references = get_column_references(unedited_full_board)

    print_board_func = assign_print_board_func(hints_enabled)

    while not game_completed:
        print(f"\non_turn_no {on_turn_no} \nturns")
        print(turns)
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
            (
                (playing_full_board, playing_flat_board),
                (hints, (on_turn_no, turns))
            ) = take_turn(
                unedited_full_board,
                playing_full_board,
                playing_flat_board,
                board_size,
                column_references,
                hints,
                on_turn_no,
                turns
            )
        elif (action == Action.UNDO and on_turn_no > -1):
            print_board_func(
                unedited_full_board,
                playing_full_board,
                board_size,
                column_references,
                hints=hints
            )
            (
                (playing_full_board, playing_flat_board),
                (hints, turns)
            ) = undo_turn(
                on_turn_no,
                playing_full_board,
                playing_flat_board,
                board_size,
                hints,
                turns
            )
            on_turn_no -= 1
        elif (action == Action.UNDO and on_turn_no == -1):
            display_unable_to_undo_turn_message()
        elif (action == Action.REDO and on_turn_no < (len(turns) - 1)):
            print_board_func(
                unedited_full_board,
                playing_full_board,
                board_size,
                column_references,
                hints=hints
            )
            (
                (playing_full_board, playing_flat_board),
                (hints, turns)
            ) = redo_turn(
                on_turn_no,
                playing_full_board,
                playing_flat_board,
                board_size,
                hints,
                turns
            )
            on_turn_no += 1
        elif (action == Action.REDO and on_turn_no == (len(turns) - 1)):
            display_unable_to_redo_turn_message()
        elif (action == Action.SHOW_HELP):
            new_hints_enabled = show_help(hints_enabled)
            if (new_hints_enabled != hints_enabled):
                print_board_func = assign_print_board_func(new_hints_enabled)
                hints_enabled = new_hints_enabled
        elif (action == Action.QUIT):
            return display_quit_message(save_file_name)

        update_save(
            save_file_name,
            playing_full_board,
            hints_enabled,
            hints,
            on_turn_no,
            turns
        )
        if (
            len([x for x in playing_flat_board if x == 0]) == 0 and
            playing_flat_board == generation["solution_flat_board"]
        ):
            game_completed = True
            complete_save(save_file_name)
            complete_game(playing_full_board, board_size, column_references)


def main():
    board_size = 9
    welcome()

    generation, (save_file_name, (hints_enabled, hints)) = (
        create_game_config(board_size)
    )

    game(generation, board_size, hints_enabled, save_file_name, hints)


if __name__ == "__main__":
    main()
