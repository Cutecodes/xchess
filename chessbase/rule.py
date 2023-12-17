from abc import ABC, abstractmethod
from typing import List
from .utils import Faction, Result
from .board import Board
from .piece import Piece

class Rule(ABC):
    @abstractmethod
    def get_next_faction(self, board:Board, cur_faction:Faction, factions:List[Faction]) -> Faction:
        pass
    
    @abstractmethod
    def add_piece(self, board:Board, piece:Piece, position) -> List[Piece]:
        pass
    
    @abstractmethod
    def move_piece(self, board:Board, origin_pos, target_pos) -> List[Piece]:
        pass
    
    @abstractmethod
    def can_continue(self, board:Board) -> bool:
        '''
        检测死棋，不需要或者无法继续的情况
        '''
        pass

    @abstractmethod
    def get_result(self, board:Board, cur_faction:Faction) -> Result:
        '''
        主动要求或无法继续游戏时输赢判决
        '''
        pass
    