from game.game import Game
from game.piece import Piece
from game.cell import CellState


class Terminal:

    def __init__(self, game: Game):
        self.__game = game

    def __display_player_symbol(self, player_id: int):
        print('X' if player_id == 1 else 'O', end=' ')

    def __display_board(self):
        board = self.__game.get_board()
        for y in range(board.get_size()):
            for x in range(board.get_size()):
                cell = board.get_cell(x, y)
                state = cell.get_state()
                if state == CellState.EMPTY:
                    print('.', end=' ')
                else:
                    self.__display_player_symbol(state)
            print()

    def __display_piece(self, piece: Piece, player_id: int):
        blocks = piece.get_blocks()
        for y in range(Piece.MIN_Y, Piece.MAX_Y + 1):
            for x in range(Piece.MIN_X, Piece.MAX_X + 1):
                if (x, y) not in blocks:
                    print('.', end=' ')
                elif (x, y) == (0, 0):
                    print('#', end=' ')
                else:
                    self.__display_player_symbol(player_id)
            print()

    def __display_player(self, player_id: int):
        player = self.__game.get_current_player()
        print(f'Player {player_id} (Score: {player.get_score()}):')
        for index, piece in enumerate(player.get_pieces()):
            if piece.is_placed():
                continue
            print(f'Piece {index + 1}')
            self.__display_piece(piece, player_id)
            print()

    def __handle_input(self):
        self.__display_player(self.__game.get_current_player().get_id())
        print('Enter piece index and position (x, y):')
        piece_index, x, y = map(int, input().split())
        self.__game.play(piece_index - 1, x, y)
        if self.__game.is_terminated():
            winner = self.__game.get_winner()
            if winner is None:
                print('It is a draw')
            else:
                print(f'Player {winner.get_id()} wins')
            exit()

    def run(self):
        while True:
            self.__display_board()
            self.__handle_input()
