# packages
import chess
from copy import deepcopy
from mcts import mcts as MCTS

# board state class
class State:
    # init board state instance
    def __init__(self, opponent=False):
        # assign chess board instance to current state from scratch
        self.board = chess.Board()
        
        # assign chess board instance to current state from existing position
        if opponent:
            self.board = deepcopy(opponent.board)
    
    # get whether the game is in the terminal state (win/draw/loss) or not
    def is_terminal(self):
        return self.board.is_game_over()
    
    # generate states (generate legal moves)
    def generate_states(self):
        # legal actions (moves) to consider in current position
        actions = []
        
        # generate legal moves
        moves = self.board.legal_moves
        
        # loop over legal moves
        for move in moves:
            # append move to action list
            actions.append(str(move))
        
        # return list of available actions (moves)
        return actions
    
    # take action (make move on board)
    def take_action(self, action):
        # create new state instance from the current state
        new_state = State(self)
        
        # take action (make move on board)
        new_state.board.push(chess.Move.from_uci(action))
        
        # return new state with action naken on board
        return new_state
    
    # get side
    def get_side(self):
        # case white to move
        if self.board.turn == True:
            return 1
        
        # case black to move
        elif self.board.turn == False:
            return -1
    
    # game loop
    def game_loop(self):
        # create MCTS instance
        mcts = MCTS(timeLimit=1000)
        
        # search position for the best move
        best_move = mcts.search(self)
        print('Bestmove', best_move)

    # output current state's board position
    def __str__(self):
        # for windows users
        #return self.board.__str__()
        return self.board.unicode().replace('⭘', '.')






























