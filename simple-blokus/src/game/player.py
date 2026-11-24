from typing import List, Dict
from game.piece import Piece
import numpy as np


PlayerState = Dict[str, np.ndarray]


class Player:

    def __init__(self, id: int, pieces: List[Piece]):
        assert id in [1, 2]
        self.__id = id
        self.__score = 0
        self.__pieces: List[Piece] = []
        self.__is_started = False
        for piece in pieces:
            self.__pieces.append(piece.copy())

    def get_id(self) -> int:
        return self.__id

    def get_score(self) -> int:
        return self.__score

    def add_score(self, score: int):
        self.__score += score

    def get_pieces(self) -> List[Piece]:
        return self.__pieces

    def get_piece(self, piece_index: int) -> Piece:
        return self.__pieces[piece_index]

    def has_pieces(self) -> bool:
        return any(not piece.is_placed() for piece in self.__pieces)

    def is_started(self) -> bool:
        return self.__is_started

    def set_started(self, started: bool):
        self.__is_started = started

    def get_state(self) -> PlayerState:
        return {
            'remaining_pieces': np.array([not piece.is_placed() for piece in self.__pieces], dtype=np.int64),
            'pieces': np.array([piece.get_state() for piece in self.__pieces], dtype=np.int64)
        }
