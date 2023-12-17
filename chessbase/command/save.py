from .command import Command
from chessbase import DUMP_PATH
import pickle
import os
class SaveCommand(Command):
    def __init__(self, chess_game, filename):
        super().__init__(chess_game)
        self.filename = filename
        
    def execute(self):
        self.save()
        filepath = os.path.join(DUMP_PATH,self.filename)
        with open(filepath,'wb') as f:
           pickle.dump(self.memento, f) 
        return False
        