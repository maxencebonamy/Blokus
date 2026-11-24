from typing import Dict, List, Union
from game.board import Board, BoardState
from game.player import Player, PlayerState
from game.piece import Piece


GameState = Dict[str, Union[BoardState, PlayerState]]


class Game:

    def __init__(self, board_size: int, pieces: List[Piece]):
        self.__board = Board(board_size, self)
        self.__players = [
            Player(1, pieces),
            Player(2, pieces)
        ]
        self.__current_player_id = 0
        self.__terminated = False

    def get_board(self) -> Board:
        return self.__board

    def get_players(self) -> List[Player]:
        return self.__players

    def get_current_player(self) -> Player:
        return self.__players[self.__current_player_id]

    def is_terminated(self) -> bool:
        return self.__terminated

    def get_winner(self) -> Union[Player, None]:
        if not self.__terminated:
            return None
        player1, player2 = self.__players
        if player1.get_score() > player2.get_score():
            return player1
        if player2.get_score() > player1.get_score():
            return player2
        return None

    def __can_player_play(self) -> bool:
        player = self.get_current_player()
        for piece in player.get_pieces():
            if not piece.is_placed() and self.__board.can_be_placed(piece, player.get_id()):
                return True
        return False

    def play(self, piece_index: int, x: int, y: int) -> int:
        player = self.get_current_player()
        piece = player.get_piece(piece_index)

        placed = self.__board.place_piece(piece, x, y, player.get_id())
        if not placed:
            return 0

        score_to_add = len(piece.get_blocks())
        player.add_score(score_to_add)
        self.__switch_player()

        self.__terminated = self.__terminated or not self.get_current_player().has_pieces() or not self.__can_player_play()
        return score_to_add

    def __switch_player(self):
        self.__current_player_id = 1 - self.__current_player_id

    def get_state(self) -> GameState:
        return {
            'board': self.__board.get_state(),
            'player_1_remaining_pieces': self.__players[0].get_state()['remaining_pieces'],
            'player_2_remaining_pieces': self.__players[1].get_state()['remaining_pieces'],
            'player_1_pieces': self.__players[0].get_state()['pieces'],
            'player_2_pieces': self.__players[1].get_state()['pieces']
        }
