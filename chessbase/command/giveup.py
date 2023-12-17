from .command import Command

class GiveupCommand(Command):
    def __init__(self, chess_game, faction):
        super().__init__(chess_game)
        self.__faction = faction
        
    def execute(self):
        self._chess_game.give_up(self.__faction)
        