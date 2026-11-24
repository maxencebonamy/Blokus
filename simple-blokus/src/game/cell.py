from typing import Tuple


class CellState:
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2


class Cell:

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__state = CellState.EMPTY

    def get_position(self) -> Tuple[int, int]:
        return self.__x, self.__y

    def get_state(self) -> int:
        return self.__state

    def is_empty(self) -> bool:
        return self.__state == CellState.EMPTY

    def set_state(self, state: int):
        self.__state = state
