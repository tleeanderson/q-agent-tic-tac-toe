#!/usr/bin/python
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.common import get_action, is_game_over, add_to_value, add_to_frequency, \
    rewardFunction, getMinMaxByBoard, O, get_actions, invoke_action, get_turn, \
    generate_board, X, machine_turn, write_state_act_value_file
from src.perm_tester import testQAgent, resetGlobals

NUM_GAMES = 2000000
DISCOUNT = 1

def updateStateActValue(currentBoard, nextBoard, nextReward, stateActValue, discount, turn):
    currentAction = get_action(currentBoard, nextBoard)
    if nextBoard != () and is_game_over(nextBoard):
        stateActValue[(currentBoard, currentAction)] += add_to_value(stateActValue[(currentBoard, currentAction)], nextReward);

    if currentBoard != None and currentAction != None:
        stateActValue[(currentBoard, currentAction)] += add_to_frequency(stateActValue[(currentBoard, currentAction)], 1)

        minMax = rewardFunction(nextBoard) if is_game_over(nextBoard) else getMinMaxByBoard(nextBoard, stateActValue, max if turn == O else min)
        newValue = (stepSizeFunc(stateActValue[(currentBoard, currentAction)][1])
            * ((nextReward + discount * minMax) - stateActValue[(currentBoard, currentAction)][0]))

        stateActValue[(currentBoard, currentAction)] = add_to_value(stateActValue[(currentBoard, currentAction)], newValue)

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

#(value, frequency)
def getStateAction(allBoards):
    result = {}
    for board in allBoards:
        actions = get_actions(board)
        for act in actions:
            result[(board, act)] = (0, 0)
    return result

def getAllBoards(board, turn, allBoards):
    boardActions = get_actions(board)
    while boardActions != []:
        root = invoke_action(boardActions.pop(), turn, board)
        allBoards.add(root)
        if is_game_over(root):
            continue
        getAllBoards(root, get_turn(turn), allBoards)

def playGame(stateActValue, machine1, machine2):
    board = generate_board()
    turn = machine1 if machine1 == X else machine2
    gameOver = False;
    while not gameOver:
        if turn == machine1:
            newBoard = machine_turn(board, stateActValue, machine1, True)
        else:
            newBoard = machine_turn(board, stateActValue, machine2, True)

        #learn from move
        updateStateActValue(board, newBoard, rewardFunction(newBoard), stateActValue, DISCOUNT, turn)

        board = newBoard
        gameOver = is_game_over(board)
        if not gameOver:
            turn = get_turn(turn)

def getStateActValue(allBoards):
    stateActValue = getStateAction(allBoards)
    machine1 = X
    machine2 = O

    for i in range(0, NUM_GAMES):
        if i % 10000 == 0:
            print "I'm %f percent done playing with myself" % ((float(i) / NUM_GAMES) * 100)
        playGame(stateActValue, machine1, machine2)

    return stateActValue

def learn():
    isBeatable = True
    numTrials = 0
    emptyBoard = generate_board()
    allBoards = set([])
    allBoards.add(emptyBoard)
    getAllBoards(emptyBoard, X, allBoards)
    resetGlobals() #defensive to make sure we have a clean slate
    while isBeatable:
        numTrials += 1
        print "Testing agent...on trial %d" % (numTrials)
        stateActValue = getStateActValue(allBoards)
        isBeatable = testQAgent(stateActValue, X, O)
        resetGlobals()
        if isBeatable:
            #skip next test because agent lost as X
            continue
        isBeatable = testQAgent(stateActValue, O, X)
        if isBeatable:
            resetGlobals()

    write_state_act_value_file(stateActValue)

learn()