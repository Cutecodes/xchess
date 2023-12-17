from .command import Command
from chessbase import DUMP_PATH
import pickle
import os
class RestoreCommand(Command):
    def __init__(self, chess_game, filename):
        super().__init__(chess_game)
        self.filename = filename
        
    def execute(self):
        self.save()
        filepath = os.path.join(DUMP_PATH,self.filename)
        with open(filepath,'rb') as f:
           self.memento = pickle.load(f) 
        self.undo()
        return False
        