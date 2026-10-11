#!/usr/bin/python
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.common import get_action, is_game_over, add_to_value, add_to_frequency, \
    reward_function, get_min_max_by_board, O, get_actions, invoke_action, get_turn, \
    generate_board, X, machine_turn, write_state_act_value_file
from src.perm_tester import test_q_agent, reset_globals

NUM_GAMES = 2000000
DISCOUNT = 1

def update_state_act_value(current_board, next_board, next_reward, state_act_value, discount, turn):
    current_action = get_action(current_board, next_board)
    if next_board != () and is_game_over(next_board):
        state_act_value[(current_board, current_action)] += add_to_value(state_act_value[(current_board, current_action)], next_reward)

    if current_board != None and current_action != None:
        state_act_value[(current_board, current_action)] += add_to_frequency(state_act_value[(current_board, current_action)], 1)

        minMax = reward_function(next_board) if is_game_over(next_board) else get_min_max_by_board(next_board, state_act_value, max if turn == O else min)
        newValue = (stepSizeFunc(state_act_value[(current_board, current_action)][1])
                    * ((next_reward + discount * minMax) - state_act_value[(current_board, current_action)][0]))

        state_act_value[(current_board, current_action)] = add_to_value(state_act_value[(current_board, current_action)], newValue)

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

#(value, frequency)
def get_state_action(all_boards):
    result = {}
    for board in all_boards:
        actions = get_actions(board)
        for act in actions:
            result[(board, act)] = (0, 0)
    return result

def get_all_boards(board, turn, all_boards):
    board_actions = get_actions(board)
    while board_actions != []:
        root = invoke_action(board_actions.pop(), turn, board)
        all_boards.add(root)
        if is_game_over(root):
            continue
        get_all_boards(root, get_turn(turn), all_boards)

def play_game(state_act_value, machine1, machine2):
    board = generate_board()
    turn = machine1 if machine1 == X else machine2
    game_over = False
    while not game_over:
        if turn == machine1:
            new_board = machine_turn(board, state_act_value, machine1, True)
        else:
            new_board = machine_turn(board, state_act_value, machine2, True)

        #learn from move
        update_state_act_value(board, new_board, reward_function(new_board), state_act_value, DISCOUNT, turn)

        board = new_board
        game_over = is_game_over(board)
        if not game_over:
            turn = get_turn(turn)

def get_state_act_value(all_boards):
    state_act_value = get_state_action(all_boards)
    machine1 = X
    machine2 = O

    for i in range(0, NUM_GAMES):
        if i % 10000 == 0:
            print("I'm %f percent done playing myself" % ((float(i) / NUM_GAMES) * 100))
        play_game(state_act_value, machine1, machine2)

    return state_act_value

def learn():
    is_beatable = True
    num_trials = 0
    empty_board = generate_board()
    all_boards = set([])
    all_boards.add(empty_board)
    get_all_boards(empty_board, X, all_boards)
    reset_globals() #defensive to make sure we have a clean slate
    while is_beatable:
        num_trials += 1
        print("Testing agent...on trial %d" % (num_trials))
        state_act_value = get_state_act_value(all_boards)
        is_beatable = test_q_agent(state_act_value, X, O)
        reset_globals()
        if is_beatable:
            #skip next test because agent lost as X
            continue
        is_beatable = test_q_agent(state_act_value, O, X)
        if is_beatable:
            reset_globals()

    write_state_act_value_file(state_act_value)

learn()