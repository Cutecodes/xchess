import tkinter as tk
from .start_page import StartPage

class XChess(tk.Tk):
    def __init__(self,logo='./asset/logo.png'):
        super().__init__()
        self.title("XCHESS")
        self.width = 800
        self.height = 600

        self.geometry("{}x{}".format(self.width,self.height))
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=logo))
        self.start_page = None
        self.set_page = None
        self.game_page = None
        self.create_start_page()
        self.start_page.pack()
    
    def create_start_page(self):
        self.start_page = StartPage(self, self.width, self.height)
