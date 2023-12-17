import tkinter as tk
from PIL import Image, ImageTk
import sys
sys.path.append('..')
from chessbase import Board
from chessbase import PieceFactory
from chessbase import Faction
from chessbase import PieceRole, Faction

from enum import Enum

class BoardUIMode(Enum):
    CROSS = 0
    GRID = 1

class BoardUI(tk.Frame):
    def __init__(self, parent=None, grid_size=40, mode:BoardUIMode=BoardUIMode.CROSS):
        super().__init__(parent)
        self.__grid_size = grid_size
        self.__canvas = None
        self.__mode = mode
        self._board_texture = None
        self._board_img = None
        self._black_texture = None
        self._black_img = None
        self._white_texture = None
        self._white_img = None
    
    def set_board_texture(self, texture):
        self._board_texture = Image.open(texture)
    
    def set_black_texture(self, texture):
        self._black_texture = Image.open(texture)
    
    def set_white_texture(self, texture):
        self._white_texture = Image.open(texture)

    def set_board(self, board:Board):
        self.__board = board
        self.__board_size = board.get_size()
        
        if self.__mode == BoardUIMode.CROSS:
            canvas_size = self.__grid_size * (self.__board_size + 1)
        elif self.__mode == BoardUIMode.GRID:
            canvas_size = self.__grid_size * (self.__board_size + 2)

        if self.__canvas is None:
            self.__canvas = tk.Canvas(self, width = canvas_size, height = canvas_size)
        else:
            self.__canvas.config(width=canvas_size, height=canvas_size)
        
        self.draw_bcakground()        
        self.draw_piece()
        self.__canvas.update()


    def bind(self, event, callback):
        self.__canvas.bind(event, callback)

    def get_mode(self):
        return self.__mode

    def get_canvas(self):
        return self.__canvas
    
    def get_grid_size(self):
        return self.__grid_size
        
    def draw_bcakground(self):
        grid_size = self.__grid_size

        if self.__mode == BoardUIMode.CROSS:
            size = self.__board_size - 1
            canvas_size = (size+3)*grid_size
        elif self.__mode == BoardUIMode.GRID:
            size = self.__board_size
            canvas_size = (size+2)*grid_size
        
        if self._board_texture is not None and self._board_img is None:
            self._board_img = ImageTk.PhotoImage(self._board_texture.resize((2*canvas_size, 2*canvas_size)))
            self.__canvas.create_image(0,0,image=self._board_img)
        elif self._board_texture is not None:
            self.__canvas.create_image(0,0,image=self._board_img)

        if self.__mode == BoardUIMode.CROSS:
            size = self.__board_size - 1
        elif self.__mode == BoardUIMode.GRID:
            size = self.__board_size

        for i in range(size):
            coord = grid_size, grid_size, (size+1)*grid_size, (i+2) * grid_size
            self.__canvas.create_rectangle(coord)
            coord = grid_size, grid_size, (i+2) * grid_size,  (size+1)*grid_size
            self.__canvas.create_rectangle(coord)
 
        coord = grid_size, grid_size,  (size+1)*grid_size,  (size+1)*grid_size
        self.__canvas.create_rectangle(coord, width=2)

    def draw_piece(self):
        size = self.__board_size
        grid_size = self.__grid_size

        for x in range(size):
            for y in range(size):
                if self.__board.get_piece((x,y)) is not None:
                    if self.__mode == BoardUIMode.CROSS:
                        p_x, p_y = (x+1)*grid_size, (y+1)*grid_size
                    elif self.__mode == BoardUIMode.GRID:
                        p_x, p_y = (x+1.5)*grid_size, (y+1.5)*grid_size
                    
                    if self.__board.get_piece((x,y)).get_faction() == Faction.BLACK:
                        if self._black_texture is not None and self._black_img is None:
                            self._black_img = ImageTk.PhotoImage(self._black_texture.resize((grid_size, grid_size)))
                            self.__canvas.create_image(p_x, p_y, image=self._black_img)
                        elif self._black_texture is not None:
                            self.__canvas.create_image(p_x, p_y, image=self._black_img)
                        else:
                            self.__canvas.create_oval(p_x - grid_size//2, p_y - grid_size//2, \
                                    p_x + grid_size//2, p_y + grid_size//2, fill='black')
                    elif self.__board.get_piece((x,y)).get_faction() == Faction.WHITE:
                        if self._white_texture is not None and self._white_img is None:
                            self._white_img = ImageTk.PhotoImage(self._white_texture.resize((11*grid_size//10, 11*grid_size//10)))
                            self.__canvas.create_image(p_x, p_y, image=self._white_img)
                        elif self._white_texture is not None:
                            self.__canvas.create_image(p_x, p_y, image=self._white_img)
                        else:
                            self.__canvas.create_oval(p_x - grid_size//2, p_y - grid_size//2, 
                                    p_x + grid_size//2, p_y + grid_size//2, fill='white')
          