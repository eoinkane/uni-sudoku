from datetime import datetime, timedelta
from typing import Tuple, List
from itertools import chain
from save_handlers.save_handlers import (
    check_if_there_are_saved_games,
    read_save,
    create_save
)
from generators.board_generator import generate_board
from utils.user_input_helpers import (
    decide_whether_to_play_saved_game,
    select_difficulty,
    select_hints_enabled,
    select_saved_game,
    select_position_value,
    select_grid_reference,
    select_stats_enabled,
    select_timer_enabled
)
from utils.custom_types import (
    Board,
    Column_References,
    Generation,
    Flat_Board,
    Hints,
    Game_Config
)
from utils.board import (
    update_board
)
from utils.screen import clear_screen, print_sudoku_board
from utils.player_experience import (
    display_undo_turn_message,
    display_redo_turn_message
)
from utils.hints import (
    handle_hints,
    handle_hints_for_an_undo_or_redo
)
from utils.time import (
    format_time_elapsed_timedelta_to_string,
    calculate_time_elapsed
)


def create_game_config(board_size: int) -> Game_Config:
    """This function creates the config need to start a suodku game.
    The config can come from a saved game file or be constructed afresh.

    Args:
        board_size (int): size of the sudoku board

    Returns:
        Game_Config: the config to start the game
    """

    # Check if the player wants to continue a saved game
    use_saved_game = decide_whether_to_play_saved_game()

    # Construct the game config from a saved game if the player wants,
    #  to continue a saved game and there are saved games available
    if use_saved_game and check_if_there_are_saved_games():
        # Ask the player to select the saved game to continue
        save_file_path = select_saved_game()
        # get the dictionary representation of the selected saved game
        save = read_save(save_file_path)
        # construct the board generation from the saved game
        generation = {
            "solution_full_board": save["solution_board"],
            "solution_flat_board": list(chain(*save["solution_board"])),
            "initial_full_board": save["initial_board"],
            "initial_flat_board": list(chain(*save["initial_board"])),
            "playing_full_board": save["playing_board"],
            "playing_flat_board": list(chain(*save["playing_board"])),
            "on_turn_no": save["on_turn_no"],
            "turns": save["turns"],
            "time_elapsed": timedelta(seconds=save["time_elapsed_secs"])
        }
        # return the board generation and the rest of the game config
        return generation, (
            save_file_path,
            (
                save["stats_enabled"],
                (
                    (
                        save["timer_enabled"],
                        timedelta(seconds=save["timer_duration_secs"])
                    ),
                    (
                        save["hints_enabled"],
                        save["hints"]
                    ),
                )
            )
        )
    # otherwise, create the game config from scratch
    else:
        # if the player selected to continue a saved game but,
        #  there was none available then display a messages
        if (use_saved_game):
            print(
                "\nThere are no saved games available for you to continue. "
                "Please create a new one."
            )
        # ask the player what options they would like to chose for the new game
        difficulty = select_difficulty()
        hints_enabled = select_hints_enabled()
        stats_enabled = select_stats_enabled()
        timer_enabled, timer_duration = select_timer_enabled(difficulty)

        # generate a random sudoku board and solution with the chosen options
        generation: Generation = generate_board(board_size, difficulty)

        # save the new game config so the player could continue at another time
        save_file_name = create_save(
            generation["solution_full_board"],
            generation["playing_full_board"],
            generation["initial_full_board"],
            board_size,
            difficulty,
            hints_enabled,
            stats_enabled,
            timer_enabled,
            timer_duration
        )
        # return the board generation and the rest of the game config
        return generation, (
            save_file_name,
            (
                stats_enabled,
                (
                    (
                        timer_enabled,
                        timer_duration
                    ),
                    (
                        hints_enabled,
                        {}
                    )
                )
            )
        )


def take_turn(
    unedited_full_board: Board,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    column_references: Column_References,
    hints: Hints,
    on_turn_no: int,
    turns: List
) -> Tuple[Tuple[Board, Flat_Board], Tuple[Hints, Tuple[int, list]]]:
    """Handle the player taking a turn. Let the player select the grid ref to update,
    the value to insert at the given grid ref, then calculate the updated turns and hints.

    Args:
        unedited_full_board (Board): 2-D version (matrix) of the initial sudoku board
        playing_full_board (Board): 2-D version (matrix) of the current sudoku board
        playing_flat_board (Flat_Board): 1-D version of the current sudoku board
        board_size (int): size of the sudoku board
        column_references (Column_References): Column References to be used when displaying the sudoku boards
        hints (Hints): the datastore to represent the hints for the player
        on_turn_no (int): the number of turns that have been made by the player
        turns (List): the turns that have been made by the player

    Returns:
        Tuple[Tuple[Board, Flat_Board], Tuple[Hints, Tuple[int, list]]]: the updated game values to play from
    """ # noqa

    # initialise the variables
    row_index: int = None
    col_index: int = None
    raw_grid_ref: str = None

    # Loop until a valid grid ref is selected
    user_selected_a_editable_grid_ref = False
    while not user_selected_a_editable_grid_ref:
        # recieve the selected grid ref
        (row_index, col_index), raw_grid_ref = select_grid_reference(
            column_references,
            board_size
        )
        # check if the selected grid ref is not populated by the inital board
        if (unedited_full_board[row_index][col_index] == 0):
            # allow the code to exit the loop
            user_selected_a_editable_grid_ref = True
        else:
            # display a message asking for valid input
            print("That grid ref is populated by the original board."
                  " Please see the board on the left and reselect a grid ref"
                  )

    # recieve the selected value to update the selected grid ref
    position_value = select_position_value(
        raw_grid_ref,
        board_size,
    )

    # recalculate the sudoku board hints with the new value the player selected
    hints = handle_hints(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        position_value
    )

    # recalculate the turns list for the turn the player is making
    # if the player is not changing any value then don't update turns
    previous_value = playing_full_board[row_index][col_index]
    if (position_value != previous_value):
        # if the player has previously undone then get rid of the,
        #  all the turns made ahead of the previous one
        if (on_turn_no < (len(turns) - 1)):
            turns = turns[0:(on_turn_no + 1)]
        # append the turn that the player has made to the list,
        #  and update the turn counter
        turns.append({
            "row_index": row_index,
            "col_index": col_index,
            "new_value": position_value,
            "previous_value": playing_full_board[row_index][col_index]
        })
        on_turn_no += 1

    # update the sudoku board with the new chosen value
    playing_full_board, playing_flat_board = update_board(
            playing_full_board,
            playing_flat_board,
            row_index,
            col_index,
            board_size,
            int(position_value)
        )
    # return the result of the players turn
    return (
        (
            playing_full_board,
            playing_flat_board
        ),
        (
            hints,
            (
                on_turn_no,
                turns
            )
        )
    )


def complete_game(
    completed_board: Board,
    starting_time: datetime
):
    """Handle a sudoku game that the player has completed.
    Display the completed sudoku board on its own and how long the player took to complete the game

    Args:
        completed_board (Board):  2-D version (matrix) of the completed sudoku board 
        starting_time (datetime): the datetime representation of when the game started
    """ # noqa
    # clear the screen
    clear_screen()
    # calculate the time taken to complete the game
    time_taken_to_complete_game_str = format_time_elapsed_timedelta_to_string(
        calculate_time_elapsed(starting_time)
    )

    # display a congratulations message and the completed sudoku board
    print(
        "Congratulations, you completed the sudoku game! "
        f"\nIt took you {time_taken_to_complete_game_str} to complete the game"
        "\nHere is the completed board"
    )
    print_sudoku_board(
        completed_board,
        should_clear_screen=False
    )


def undo_turn(
    turn_no: int,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    hints: Hints,
    turns: list
) -> Tuple[Tuple[Board, Flat_Board], Tuple[Hints, list]]:
    """Handle the player undoing a turn. Undo the latest change to the sudoku board,
    then calculate the updated turns and hints.

    Args:
        turn_no (int): the current number of turns that have been made by the player
        playing_full_board (Board): 2-D version (matrix) of the current sudoku board
        playing_flat_board (Flat_Board): 1-D version of the current sudoku board
        board_size (int): size of the sudoku board
        hints (Hints): the datastore to represent the hints for the player
        turns (list): the turns that have been made by the player

    Returns:
        Tuple[Tuple[Board, Flat_Board], Tuple[Hints, list]]: the updated game values to play from
    """ # noqa
    # get the turn to undo
    turn = turns[turn_no]
    row_index = turn["row_index"]
    col_index = turn["col_index"]

    # display a message to the player showing what turn is going to be undone
    display_undo_turn_message(turn_no, turn)

    # recalculate the hints for the game without the previous turn
    hints = handle_hints_for_an_undo_or_redo(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        turn["previous_value"]
    )

    # update the sudoku board with the original value from the previous turn
    playing_full_board, playing_flat_board = update_board(
        playing_full_board,
        playing_flat_board,
        row_index,
        col_index,
        board_size,
        turn["previous_value"]
    )

    # return the result of the undo
    return (
        (
            playing_full_board,
            playing_flat_board
        ),
        (
            hints,
            turns
        )
    )


def redo_turn(
    turn_no: int,
    playing_full_board: Board,
    playing_flat_board: Flat_Board,
    board_size: int,
    hints: Hints,
    turns: list
) -> Tuple[Tuple[Board, Flat_Board], Tuple[Hints, list]]:
    """Handle the player redoing a turn. Redo the next change to the sudoku board,
    then recalculate the updated turns and hints.

    Args:
        turn_no (int): the current number of turns that have been made by the player
        playing_full_board (Board): 2-D version (matrix) of the current sudoku board
        playing_flat_board (Flat_Board): 1-D version of the current sudoku board
        board_size (int): size of the sudoku board
        hints (Hints): the datastore to represent the hints for the player
        turns (list): the turns that have been made by the player

    Returns:
        Tuple[Tuple[Board, Flat_Board], Tuple[Hints, list]]: the updated game values to play from
    """ # noqa
    # get the turn to redo
    turn = turns[turn_no + 1]
    row_index = turn["row_index"]
    col_index = turn["col_index"]

    # display a message to the player showing what turn is going to be redone
    display_redo_turn_message(turn_no, turn)

    # recalculate the hints for the game without the previous turn
    hints = handle_hints_for_an_undo_or_redo(
        playing_full_board,
        board_size,
        row_index,
        col_index,
        hints,
        turn["new_value"]
    )

    # update the sudoku board with the original value from the next turn
    playing_full_board, playing_flat_board = update_board(
        playing_full_board,
        playing_flat_board,
        row_index,
        col_index,
        board_size,
        turn["new_value"]
    )

    # return the result of the undo
    return (
        (
            playing_full_board,
            playing_flat_board
        ),
        (
            hints,
            turns
        )
    )
