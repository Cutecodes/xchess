from .command import Command
import sys
import pickle
import os
class SaveCommand(Command):
    def __init__(self, chess_game, filename):
        super().__init__(chess_game)
        self.filename = filename
    
    def save(self):
        self.memento = self._chess_game.save(save_history_command=True)

    def execute(self):
        self.save()
        filepath = os.path.join(os.path.dirname(__file__) + os.path.sep + "../../", r"data/dumps/"+self.filename)
        with open(filepath,'wb') as f:
           pickle.dump(self.memento, f) 
        return False