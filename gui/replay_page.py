import tkinter as tk
from PIL import Image, ImageTk
from .boardUI import BoardUI,BoardUIMode

class ReplayPage(tk.Frame):
    def __init__(self, parent=None, game = None, mode=BoardUIMode.GRID, game_page=None):
        super().__init__(parent)
        self.parent = parent
        self.game = game
        self.index = 0
        self.game_page = game_page
        self.boardUI = BoardUI(self, mode=mode)
        self.boardUI.set_board_texture("./asset/back.png")
        self.boardUI.set_black_texture("./asset/black.png")
        self.boardUI.set_white_texture("./asset/white.png")
        
        self.boardUI.grid(row=0, column=0, columnspan=3)
        self.back = tk.Button(self, text="上一步", command=self.back)
        self.next = tk.Button(self, text="下一步", command=self.next)
        self.exit = tk.Button(self, text="退出回放", command=self.exit)

        self.back.grid(row=1, column=0)
        self.next.grid(row=1, column=1)
        self.exit.grid(row=1, column=2)
         
        self.update()

    def update(self):
        board = self.game.get_state_at(self.index)
        if board:
            self.boardUI.set_board(board)
        self.boardUI.get_canvas().update()
        self.boardUI.get_canvas().pack()

    def back(self):
        if self.index > 0:
            self.index -= 1
            self.update()

    def next(self):
        self.index += 1
        self.update()

    def exit(self):
        self.pack_forget()
        self.game_page.packs()
        self.game_page.replay_page = None
        