from enum import Enum

class Faction(Enum):
    BLACK = 1
    WHITE = 2

class Result(Enum):
    STALEMATE = 0
    BLACK_WIN = 1
    WHITE_WIN = 2

class GameState(Enum):
    RUNNING = 0
    END = 1

DUMP_PATH = "./dump"