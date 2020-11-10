#
#    MCTS + Stockfish NNUE
#  experimental chess engine
#

# packages
from state import *
from uci import *

# create initial state instance
state = State()

# run engine in UCI mode
uci_loop(state)

# 4K3/r7/6k1/8/8/8/8/q7 b - - 0 1 
