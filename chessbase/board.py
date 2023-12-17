from enum import Enum
from .error import PieceExistError, PieceOutError, PieceNotExistError

class Board:
    def __init__(self, size=8):
        self.__size = size
        self.__board = [[None for _ in range(size)] for _ in range(size)]

    def add_piece(self, piece, position):
        x = position[0]
        y = position[1]
        if x >= 0 and x < self.__size and y >= 0 and y < self.__size:
            if self.__board[x][y] is not None:
                raise PieceExistError
            else:
                self.__board[x][y] = piece
        else:
            raise PieceOutError
    
    def move_piece(self, origin, target):
        o_x = origin[0]
        o_y = origin[1]
        t_x = target[0]
        t_y = target[1]
        if self.__board[o_x][o_y] is None:
            raise PieceNotExistError
        piece = None
        if 0 <= o_x and o_x < self.__size and 0 <= o_y and o_y < self.__size \
           and o <= t_x and t_x < self.__size and 0 <= t_y and t_y < self.__size :
            piece = self.__board[t_x][t_y]
            self.__board[t_x][t_y] = self.__board[o_x][o_y]
            self.__board[o_x][o_y] = None
        else:
            return PieceOutError
        return piece

    def remove_piece(self, position):
        chess = None
        
        x, y = position[0], position[1]
        if 0 <= x and x < self.__size and 0 <= y and y < self.__size:
            chess = self.__board[x][y] 
            self.__board[x][y] = None
        else:
            raise PieceOutError
        if chess is None:
            raise PieceNotExistError

        return chess

    def get_state(self):
        return self.__board

    def set_state(self, board):
        if len(board) != self.__size:
            return False
        else:
            self.__board = board
            return True

    def get_size(self):
        return self.__size
    
    def get_piece(self, position):
        chess = None
        
        x, y = position[0], position[1]
        if 0 <= x and x < self.__size and 0 <= y and y < self.__size:
            chess = self.__board[x][y] 
       
        return chess