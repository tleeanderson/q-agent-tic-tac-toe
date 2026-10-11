#!/usr/bin/python
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.common import get_actions, invoke_action, generate_board, X, O, Y, N, machine_turn, \
    get_action, is_game_over, is_win, is_cat, get_turn, load_state_act_value_file

def output(ele, ind):
    return ' ' + (str(ind) if ele == None else str(ele)) + ' '

def print_board(board):
    print('\n%s|%s|%s' % (output(board[0], 0), output(board[1], 1), output(board[2], 2)))
    print('-' * 11)
    print('%s|%s|%s' % (output(board[3], 3), output(board[4], 4), output(board[5], 5)))
    print('-' * 11)
    print('%s|%s|%s\n' % (output(board[6], 6), output(board[7], 7), output(board[8], 8)))

def get_input(actions):
    input_valid = False
    usr_act = None
    invalid_message = "Invalid action. Valid actions are: " + str(actions)
    while not input_valid:
        usr_act = input("Enter move: ")
        try:
            usr_act = int(usr_act)
        except ValueError:
            print(invalid_message)
        else:
            if usr_act in set(actions):
                input_valid = True
            else:
                print(invalid_message)
    return usr_act

def human_turn(board, human):
    usr_act = get_input(get_actions(board))
    return invoke_action(usr_act, human, board)

def play_game(state_act_value, human, machine):
    board = generate_board()
    turn = human if human == X else machine
    print("Initial board: ")
    game_over = False
    while not game_over:
        print_board(board)
        if turn == human:
            new_board = human_turn(board, human)
        else:
            new_board = machine_turn(board, state_act_value, machine, False)
            print("Machine move: " + str(get_action(board, new_board)))

        board = new_board
        game_over = is_game_over(board)
        if game_over:
            if is_win(board, human):
                print("Human wins!")
            elif is_win(board, machine):
                print("Machine wins!")
            elif is_cat(board):
                print("Draw!")
            print_board(board)
        else:
            turn = get_turn(turn)

def get_player_input(valid, out_message):
    player_input = None
    while not player_input in valid:
        player_input = input(out_message).lower()
    return player_input

def main():
        play_again = True
        state_act_value = load_state_act_value_file()
        while play_again:
            human = get_player_input({X, O}, "Do you want to be x or o? ")
            machine = get_turn(human)
            print("\nPlay!\n")
            play_game(state_act_value, human, machine)
            play_again_input = get_player_input({Y, N}, "Do you want to play again (y, n)? ")
            play_again = True if play_again_input == 'y' else False
main()