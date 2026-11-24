from typing import List, Tuple
import numpy as np


class Piece:

    MIN_X = -2
    MAX_X = 2
    MIN_Y = -2
    MAX_Y = 2

    def __init__(self, blocks: List[Tuple[int, int]]):
        for x, y in blocks:
            assert self.MIN_X <= x <= self.MAX_X
            assert self.MIN_Y <= y <= self.MAX_Y
        self.__blocks = blocks
        self.__placed = False

    def get_blocks(self) -> List[Tuple[int, int]]:
        return self.__blocks

    def is_placed(self) -> bool:
        return self.__placed

    def place(self):
        self.__placed = True

    # def rotate(self):
    #     self.__blocks = [(y, -x) for x, y in self.__blocks]

    def copy(self):
        return Piece(self.__blocks[:][:])

    def get_state(self) -> np.ndarray:
        return np.array([[1 if (x, y) in self.__blocks else 0 for y in range(self.MIN_Y, self.MAX_Y + 1)] for x in range(self.MIN_X, self.MAX_X + 1)])
