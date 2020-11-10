from __future__ import division
from __future__ import print_function
from ctypes import *
import time
import math
import random

# load NNUE shared library
nnue = cdll.LoadLibrary("./libnnueprobe.so")

# load NNUE weights file
nnue.nnue_init(b"nn-c3ca321c51c9.nnue")

def randomPolicy(state):
    while not state.is_terminal():
        try:
            action = random.choice(state.generate_states())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(action)
    return state.getReward()

# NNUE evalauation
def nnue_policy(state):
    #print('nnue', state)
    #import chess
    
    #board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1') #'r3K3/q7/k7/8/8/8/8/8 w - - 0 0'
    #print(board)
    
    # case black is checkmated
    #if board.is_checkmate() and board.turn == False:
    #    print(board, board.turn)
    #    return -10000
    
    # case white is checkmated
    #if board.is_checkmate() and board.turn == True:
    #    print(board, board.turn)
    
     
    #can_claim_draw()
    #is_insufficient_material()
    #is_stalemate() 
    
    # get NNUE evaluation score
    return nnue.nnue_evaluate_fen(bytes(state.board.fen(), encoding='utf-8'))

class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.is_terminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=nnue_policy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState):
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.generate_states()
        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.take_action(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = node.state.get_side() * child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
                
            if explorationValue == 0:
                print(child.state.board)
                print('\ntotal score: %s\n\n' % child.totalReward)
            
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action
