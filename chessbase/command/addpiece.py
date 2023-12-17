from .command import Command

class AddPieceCommand(Command):
    def __init__(self, chess_game, faction, piece_role, position):
        super().__init__(chess_game)
        self.__faction = faction
        self.__piece_role = piece_role
        self.__position = position

    def execute(self):
        self.save()
        self._chess_game.add_piece(self.__faction, self.__piece_role, self.__position)
        return True

