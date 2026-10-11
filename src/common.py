#!/usr/bin/python
from random import randint
import pickle
from os import getcwd

BOARD_LEN = 9
X = 'x'
O = 'o'
Y = 'y'
N = 'n'
WIN_REWARD = 99
CAT_REWARD = .5
NON_TERM_REWARD = 0
LOSS_REWARD = -99
STATE_ACT_VALUE_FILE = getcwd() + "/../data/state.dat"

def add_to_frequency(tup, value):
    return (tup[0], tup[1] + value)

def add_to_value(tup, value):
    return (tup[0] + value, tup[1])

def load_state_act_value_file():
    state_act_value = None
    try:
        handle = open(STATE_ACT_VALUE_FILE, "rb")
    except IOError:
        print("ERROR: %s file does not exist." % (STATE_ACT_VALUE_FILE))
    else:
        state_act_value = pickle.load(handle)

    return state_act_value

def write_state_act_value_file(state_act_value):
    try:
        handle = open(STATE_ACT_VALUE_FILE, "wb")
    except IOError:
        print("ERROR: when opening %s for write" % (STATE_ACT_VALUE_FILE))
    else:
        pickle.dump(state_act_value, handle)


def get_best_move(board, state_act_value, min_max):
    actions = get_actions(board)
    action_vals = {}
    result = None
    for act in actions:
        action_vals[state_act_value[(board, act)][0]] = act

    if len(action_vals) == 1:
        #all of the actions are equal so choose at random
        result = actions[randint(0, len(actions) - 1)]
    else:
        #hashed by value of action so return min/max key
        result = action_vals[min_max(action_vals.keys())]

    return result

def machine_turn(board, state_act_value, machine, learning):
    action = None
    if learning:
        if randint(0, 99) in range(0, 12): #12 percent chance to move randomly
            possibles = get_actions(board)
            action = possibles[randint(0, len(possibles) - 1)]
        else:
            action = get_best_move(board, state_act_value, min if machine == O else max)
    else:
        action = get_best_move(board, state_act_value, min if machine == O else max)

    return invoke_action(action, machine, board)

def get_action(prev_board, current_board):
    result = None
    if prev_board is not None:
        for idx, ele in enumerate(prev_board):
            if ele != current_board[idx]:
                result = idx
                break
    return result

def reward_function(board):
    if is_win(board, X):
        return WIN_REWARD
    elif is_win(board, O):
        return LOSS_REWARD
    elif is_cat(board):
        return CAT_REWARD
    else:
        return NON_TERM_REWARD

def get_min_max_by_board(board, dictionary, minMax):
    actions = get_actions(board);
    values = set()
    for action in actions:
        values.add(dictionary[(board, action)][0])

    return minMax(values)

def get_turn(turn):
    return X if turn == O else O

def invoke_action(index, ele, board):
    result = list(board[:])
    result[index] = ele
    return tuple(result)

def get_actions(board):
    #print(f"get_actions, board: {board}")
    return [idx for idx, ele in enumerate(board) if ele is None] if board != () and not is_game_over(board) else []

def is_cat(board):
    return len([ele for ele in board if not ele is None]) == BOARD_LEN

def is_win(board, char):
    #horizontal wins
    return ((board[0] == char and board[1] == char and board[2] == char)
    or (board[3] == char and board[4] == char and board[5] == char)
    or (board[6] == char and board[7] == char and board[8] == char)
    #vertical wins
    or  (board[0] == char and board[3] == char and board[6] == char)
    or  (board[1] == char and board[4] == char and board[7] == char)
    or  (board[2] == char and board[5] == char and board[8] == char)
    #diagonal wins
    or  (board[0] == char and board[4] == char and board[8] == char)
    or  (board[2] == char and board[4] == char and board[6] == char))

def is_game_over(board):
    return is_cat(board) or is_win(board, X) or is_win(board, O)

#None space is unoccupied
#x means x is in space
#o means o is in space
def generate_board():
    return tuple([None for _ in range(BOARD_LEN)])