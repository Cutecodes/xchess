from .command import Command

class RetractCommand(Command):
    def __init__(self, chess_game, faction):
        super().__init__(chess_game)
        self.__faction = faction
        
    def execute(self):
        self.save()
        return self._chess_game.retract(self.__faction)
        