from enum import Enum
from .utils import *
from threading import Lock, Thread

class PieceRole(Enum):
    '''
    棋子角色，象棋可能有象马等，围棋此属性值用不到
    '''
    DEFAULT = 0

class Piece():
    def __init__(self, faction:Faction, piece_role:PieceRole = PieceRole.DEFAULT):
        self._faction = faction
        self._piece_role = piece_role

    def get_faction(self) -> Faction:
        return self._faction

    def set_faction(self, faction:Faction):
        self._faction = faction
    
    def get_piece_role(self):
        return self._piece_role

    def set_piece_role(self, piece_role:PieceRole):
        self._piece_role = piece_role

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class PieceFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.__pieces = {}

    def get_piece(self, faction:Faction, piece_role:PieceRole) -> Piece:
        piece = None
        if (faction, piece_role) in self.__pieces.keys():
            piece = self.__pieces[(faction, piece_role)]
        else:
            piece = Piece(faction, piece_role)
            self.__pieces[(faction, piece_role)] = piece

        return piece
