from .command import Command

class SkipCommand(Command):
    def __init__(self, chess_game, faction):
        super().__init__(chess_game)
        self.__faction = faction
        
    def execute(self):
        self.save()
        self._chess_game.skip(self.__faction)
        return True
        