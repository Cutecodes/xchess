import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from .game_page import GamePage, GamePageDirector, GogamePageBuilder,GobanggamePageBuilder

class SetPage(tk.Frame):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height

        self.create_picture()
        self.picture.pack()

        self.create_input()
        self.input.pack()

        self.create_start()
        self.start.pack()

        self.pack()

    def create_picture(self):
        self.picture =  tk.Label(self)

    def create_input(self):
        self.entry_var = tk.StringVar()
        self.input = tk.Entry(self,textvariable=self.entry_var,width=100)
        self.entry_var.set('please input the board size(8-19)')

    def create_start(self):
        self.start = tk.Button(self, text='开始游戏', command=self.start_game)

    def create_game(self,board_size):
        print(board_size)
    
    def start_game(self):
        try:
            board_size = int(self.entry_var.get())
        except ValueError:
            messagebox.showinfo("提示", "请输入整数棋盘大小！")
        else:
            if board_size < 8 or board_size > 19:
                messagebox.showinfo("提示", "棋盘大小必须在8-19之间！")
            else:
                self.create_game(board_size)
                self.pack_forget()



class GobangSetPage(SetPage):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent,width,height)

    def create_picture(self):
        image = Image.open("./asset/gobang.png")    
        self.image = ImageTk.PhotoImage(image.resize((round(0.8*self.width),round(0.8*self.height))))    
        self.picture = tk.Label(self,image=self.image)
    
    def create_game(self,board_size):
        gobanggame_page_builder = GobanggamePageBuilder(self.parent, board_size)
        game_page_director =  GamePageDirector(gobanggame_page_builder)
        game_page_director.make()
        game_page = gobanggame_page_builder.get_game_page()
        game_page.packs()

class GoSetPage(SetPage):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent,width,height)

    def create_picture(self):
        image = Image.open("./asset/go.png")    
        self.image = ImageTk.PhotoImage(image.resize((round(0.8*self.width),round(0.8*self.height))))    
        self.picture = tk.Label(self,image=self.image)

    def create_game(self,board_size):
        gogame_page_builder = GogamePageBuilder(self.parent, board_size)
        game_page_director =  GamePageDirector(gogame_page_builder)
        game_page_director.make()
        game_page = gogame_page_builder.get_game_page()
        game_page.packs()