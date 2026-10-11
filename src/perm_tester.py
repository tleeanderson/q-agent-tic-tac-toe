#!/usr/bin/python
from src.common import generate_board, X, is_game_over, is_win, is_cat, machine_turn, \
    get_actions, get_turn, invoke_action

def reset_globals():
    global Q_AGENT_WINS
    Q_AGENT_WINS = 0

    global PERM_AGENT_WINS
    PERM_AGENT_WINS = 0

    global CAT_GAMES
    CAT_GAMES = 0

PERM_AGENT_WINS = 0
Q_AGENT_WINS = 0
CAT_GAMES = 0

def test_q_agent(stateActValue, machine, permAgent):
    testAgent(stateActValue, generate_board(), machine, permAgent, X)
    print "Q-Agent as %s -> Q-Agent: %d\tPermutation Agent: %d\tCat: %d" % (machine, Q_AGENT_WINS, PERM_AGENT_WINS, CAT_GAMES)
    return PERM_AGENT_WINS > 0

def testAgent(stateActValue, initialBoard, machine, permAgent, turn):
    newBoard = initialBoard
    gameOver = False
    while not gameOver:
        gameOver = is_game_over(newBoard)
        if gameOver:
            if is_win(newBoard, permAgent):
                global PERM_AGENT_WINS
                PERM_AGENT_WINS += 1
            elif is_win(newBoard, machine):
                global Q_AGENT_WINS
                Q_AGENT_WINS += 1
            elif is_cat(newBoard):
                global CAT_GAMES
                CAT_GAMES += 1
        else:
            if turn == machine:
                newBoard = machine_turn(newBoard, stateActValue, machine, False)
            else:
                actions = get_actions(newBoard)
                saveBoard = newBoard
                changeTurn = get_turn(turn)
                for act in actions:
                    newBoard = invoke_action(act, permAgent, saveBoard)
                    testAgent(stateActValue, newBoard, machine, permAgent, changeTurn)
            turn = get_turn(turn)