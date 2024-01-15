from .utils import *
from .error import *
from .chessgame import ChessGame
from abc import ABC, abstractmethod

class Player:
    def __init__(self, user = None, faction:Faction = Faction.BLACK, game:ChessGame = None):
        self._user = user
        self._faction = faction
        self._game = game

    @abstractmethod
    def add_piece(self, game:ChessGame):
        pass


class HumanPlayer(Player):
    def __init__(self, user = None, faction:Faction = Faction.BLACK, game:ChessGame = None):
        super().__init__(user, faction, game)
    
    def add_piece(self, game:ChessGame):
        pass
