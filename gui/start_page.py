import tkinter as tk
from PIL import Image, ImageTk
from .set_page import GobangSetPage, GoSetPage, OthelloSetPage

class StartPage(tk.Frame):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.game_list = []
        self.create_game_list()

    def create_game_list(self):
        self.create_gobang()
        self.create_go()
        self.create_othello()
        for b in self.game_list:
            b.pack()

    def create_gobang(self):
        image = Image.open("./asset/gobang.png")    
        self.gobang_image = ImageTk.PhotoImage(image.resize((round(0.3*self.width),round(0.3*self.height))))    
 
        self.game_list.append(tk.Button(self,image=self.gobang_image, command=self.create_gobang_set_page))
    
    def create_go(self):
        image = Image.open("./asset/go.png")    
        self.go_image = ImageTk.PhotoImage(image.resize((round(0.3*self.width),round(0.3*self.height))))    
 
        self.game_list.append(tk.Button(self, image=self.go_image, command=self.create_go_set_page))

    def create_othello(self):
        image = Image.open("./asset/othello.png")    
        self.othello_image = ImageTk.PhotoImage(image.resize((round(0.3*self.width),round(0.3*self.height))))    
 
        self.game_list.append(tk.Button(self, image=self.othello_image, command=self.create_othello_set_page))
    
    def create_gobang_set_page(self):
        GobangSetPage(self.parent, self.width, self.height)
        self.pack_forget()

    def create_go_set_page(self):
        GoSetPage(self.parent, self.width, self.height)
        self.pack_forget()

    def create_othello_set_page(self):
        OthelloSetPage(self.parent, self.width, self.height)
        self.pack_forget()