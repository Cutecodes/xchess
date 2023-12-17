from .command import Command

class RestartCommand(Command):
    def __init__(self, chess_game):
        super().__init__(chess_game)

    def execute(self):
        self._chess_game.restart()