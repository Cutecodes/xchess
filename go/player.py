from chessbase import Player, Faction, ChessGame, GameState
from chessbase import AddPieceCommand, PieceRole
import random

class GoLevel_1(Player):
    def __init__(self, user = None, faction:Faction = Faction.BLACK,game:ChessGame=None):
        super().__init__(user, faction,game)

    def add_piece(self, game:ChessGame):
        board = game.get_board()
        cur_faction = game.get_cur_faction()
        valid_position = []

        if cur_faction == self._faction:
            board_size = board.get_size()
            board_state = board.get_state()
            for x in range(board_size):
                for y in range(board_size):
                    if board_state[x][y] is None:
                        valid_position.append((x,y))
        else:
            return

        position = random.choice(valid_position)

        add_piece_command = AddPieceCommand(game, cur_faction, PieceRole.DEFAULT, position)

        try:
            game.execute_command(add_piece_command)        
        except Exception as e:
            print(e)

    def run(self):
        while self._game.get_state() != GameState.END:
            self.add_piece(self._game)






    