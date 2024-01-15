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

class OthelloRule(Rule):
    def __init__(self):
        self.forbidden = None

    def get_next_faction(self, board:Board, cur_faction:Faction, factions:List[Faction]) -> Faction:
        if len(factions) != 2:
            raise NotImplementedError
        

        if cur_faction == factions[0]:
            if len(self.get_valid_position(board,factions[1])):
                return factions[1]
            else:
                return factions[0]
        else:
            if len(self.get_valid_position(board,factions[0])):
                return factions[0]
            else:
                return factions[1]

    def add_piece(self, board:Board, piece:Piece, position) -> List[Piece]:
        # 0. we add piece directly
        faction = piece.get_faction()
        size = board.get_size()
        board_state = board.get_state()

        if position in self.get_valid_position(board, faction) or board_state[position[0]][position[1]]:
            board.add_piece(piece, position)
        else:
            raise PieceForbiddenError

        # 1. we remove some pieces
        
        direction = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        remove_pieces = []

        for d in direction:
            cur_x,cur_y = position[0], position[1]
            tmp_piece = []
            n_x, n_y = cur_x + d[0], cur_y + d[1]
            while 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and board_state[n_x][n_y] and \
                    board_state[n_x][n_y].get_faction() != faction:
                tmp_piece.append((n_x,n_y))
                cur_x, cur_y = n_x, n_y
                n_x, n_y = cur_x + d[0], cur_y + d[1]
                if 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and \
                        board_state[n_x][n_y] and board_state[n_x][n_y].get_faction() == faction:
                    remove_pieces.extend(tmp_piece)
                    break
                elif 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and \
                        board_state[n_x][n_y] is None:
                    break


        for p in remove_pieces:
            board_state[p[0]][p[1]] = piece

        return remove_pieces       
    
    def move_piece(self, board:Board, origin_pos, target_pos) -> List[Piece]:
        # othello not support move piece
        raise NotImplementedError

    def get_valid_position(self, board:Board, faction:Faction):
        valid_position = []
        size = board.get_size()
        board_state = board.get_state()
        direction = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

        for x in range(size):
            for y in range(size):
                if board_state[x][y] and board_state[x][y].get_faction() == faction:                    
                    for d in direction:
                        cur_x,cur_y = x,y
                        tmp_num = 0
                        n_x, n_y = cur_x + d[0], cur_y + d[1]
                        while 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and board_state[n_x][n_y] and \
                                board_state[n_x][n_y].get_faction() != faction:
                            tmp_num += 1
                            cur_x, cur_y = n_x, n_y
                            n_x, n_y = cur_x+d[0], cur_y+d[1]
                        if tmp_num >= 1 and 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and \
                                board_state[n_x][n_y] is None:
                            valid_position.append((n_x,n_y))

        return valid_position
                        
    def can_continue(self, board:Board) -> bool:
        size = board.get_size()
        board_state = board.get_state()
        # No position to place piece
        if len(self.get_valid_position(board,Faction.BLACK)) == 0 and \
                len(self.get_valid_position(board,Faction.WHITE)) == 0:
            return False
        
        # the board is full
        for x in range(size):
            for y in range(size):
                if not board_state[x][y]:
                    return True
        
        return False
    
    def count_piece(self, board):
        white = 0
        black = 0

        board_state = board.get_state()
        size = board.get_size()

        for x in range(size):
            for y in range(size):
                if board_state[x][y]:
                    if board_state[x][y].get_faction() == Faction.BLACK:
                        black += 1
                    else:
                        white += 1
        return black,white


    def get_result(self, board:Board, cur_faction:Faction) -> Result:
        black, white = self.count_piece(board)
        
        if black > white: 
            return Result.BLACK_WIN
        elif black < white:
            return Result.WHITE_WIN
        else:
            return Result.STALEMATE
        
        
        



        
