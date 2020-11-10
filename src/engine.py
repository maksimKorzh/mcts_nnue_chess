#
#    MCTS + Stockfish NNUE
#  experimental chess engine
#

# packages
from state import *

# create initial state instance
state = State()

# run game loop
state.game_loop()
