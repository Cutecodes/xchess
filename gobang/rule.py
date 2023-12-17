import sys
sys.path.append("..")
import copy
from abc import ABC, abstractmethod
from typing import List
from chessbase import Faction, Result
from chessbase import Board
from chessbase import Piece
from chessbase import Rule
from chessbase import PieceForbiddenError
from chessbase import PieceFactory, PieceRole

class GobangRule(Rule):
    def __init__(self):
        self.forbidden = None

    def get_next_faction(self, board:Board, cur_faction:Faction, factions:List[Faction]) -> Faction:
        if len(factions) != 2:
            raise NotImplementedError

        if cur_faction == factions[0]:
            return factions[1]
        else:
            return factions[0]

    def add_piece(self, board:Board, piece:Piece, position) -> List[Piece]:
    	# 0. we add piece directly        
        board.add_piece(piece, position)
    
    
    def move_piece(self, board:Board, origin_pos, target_pos) -> List[Piece]:
        # gobang not support move piece
        raise NotImplementedError
    
    def check_five(self, board:Board):
        size = board.get_size()
        board_state = board.get_state()
        direction = [(-1,1),(0,1),(1,0),(1,1)]

        for x in range(size):
            for y in range(size):
                if board_state[x][y]:                    
                    cur_x,cur_y = x,y
                    for d in direction:
                        tmp_num = 1
                        n_x, n_y = cur_x+d[0], cur_y+d[1]
                        while 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and board_state[n_x][n_y] and \
                                board_state[cur_x][cur_y].get_faction() == board_state[n_x][n_y].get_faction():
                            tmp_num += 1
                            if tmp_num >= 5:
                                return board_state[cur_x][cur_y].get_faction()
                            cur_x, cur_y = n_x, n_y
                            n_x, n_y = cur_x+d[0], cur_y+d[1]
                        

    def can_continue(self, board:Board) -> bool:
        if self.check_five(board):
            return False
        size = board.get_size()
        board_state = board.get_state()
        for x in range(size):
            for y in range(size):
                if not board_state[x][y]:
                    return True
        
        return False

    def get_result(self, board:Board, cur_faction:Faction) -> Result:
        winner = self.check_five(board)
        
        if winner and winner == Faction.BLACK: 
            return Result.BLACK_WIN
        elif winner:
            return Result.WHITE_WIN
        else:
            return Result.STALEMATE
        
        
        



        
