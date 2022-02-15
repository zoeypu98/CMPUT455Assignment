# Simple transposition table for TicTacToe solver used as reference by Martin Mueller

# https://iq.opengenus.org/zobrist-hashing-game-theory/
# https://www.youtube.com/watch?v=9HFbhPscPU0
# used these codes as inspiration

"""
==========================================================================
Assignment 2 - transposition table (This is an array-based table)
==========================================================================
"""

from sys import stdin, stdout, stderr
import numpy as np
import random
from board_util import (
    GoBoardUtil,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    PASS,
    is_black_white,
    is_black_white_empty,
    coord_to_point,
    where1d,
    MAXSIZE,
    GO_POINT,
)

def random_bitstring():
    """
    generate and return a random integer between 1 and 64 bits
    """
    rand_int = random.randint(1, 2 ** 64 - 1)
    return rand_int


def zobrist_table(state):
    """
    fill a table with random bitstring for each board position
    table[number_of_board_cells][number_of_pieces]

    [   [ '_', '_', '_'], ['_', '_', '_']
        ['_', '_', '_'], ['_', '_', '_']    ]

    """
    num_board_pos = state.size
    numb_pieces = 3

    zobtable = [[[random_bitstring() for piece in range(numb_pieces)]
                 for row in range(num_board_pos)] for col in range(num_board_pos)]

    return zobtable


def hash_function(state):
    """
    returns hash according to current board config
    mapping each piece: BLACK = 1, WHITE = 2, EMPTY = 0
    returns hash
    """
    hash_value = 0
    zobtable = zobrist_table(state.board)

    for row in range(1, state.size + 1):
        for col in range(1, state.size + 1):  # for each cell on board:

            point = coord_to_point(row, col, state.size)

            if state.board[point] != EMPTY:  # if cell is not empty:
                piece = state.board[point]
                hash_value = hash_value ^ zobtable[row][col][piece]

    return hash_value


class TranspositionTable(object):
    """
    Table is stored in a fixed array,

    i.e.
    {'[[1 2],[0 0]]': True }

    key:  maybe board
    value/ result: minimax value.
    """

    def __init__(self):
        self.size = 2 ** 23
        self.bucket = [None] * self.size  # 1d array of size 2^ 23

    # Used to print the whole table with print(tt)
    def print_bucket(self):
        for i in self.bucket:
            if i is not None:
                """ Send Transposition Table to stdout """
                stdout.write("This is bucket= {}\n\n".format(i))
                stdout.flush()

    def store(self, hash_index, state, result):
        """
        hash_index: sliced hashcode index
        key: current state of the board (current config)
            [ key: state1 , value: [True, a1] ]      OR ...
            [ key: state2, value: [False]    ]
        """

        key_value_pair = [state, result]

        if self.bucket[hash_index] is None:
            self.bucket[hash_index] = list([key_value_pair])
            return True

        else:   # collision; states will always be unique, hash_index overlaps
            self.bucket[hash_index].append(key_value_pair)
            return True

    # returns 'None' or result
    def lookup(self, hash_index, state):

        if self.bucket[hash_index] is not None:     # has a list stored

            for pair in self.bucket[hash_index]:
                # self.bucket[hash_index] = [ [state, False]   ]
                if (pair[0] == state).all():
                    result = pair[1]
                    return result

        return None


def main():
    return


main()
