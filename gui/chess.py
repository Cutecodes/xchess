import sys
sys.path.append("..")
import tkinter as tk
from .start_page import StartPage
from .login import Login
from client import Client

class XChess(tk.Tk):
    def __init__(self,logo='./asset/logo.png'):
        super().__init__()
        self.title("XCHESS")
        self.width = 800
        self.height = 600

        self.geometry("{}x{}".format(self.width,self.height))
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=logo))
        self.client = Client()
        self.start_page = None
        self.create_start_page()
        self.login_page = Login(self)
        self.login_page.pack()
        self.user_info = None
    
    def create_start_page(self):
        self.start_page = StartPage(self, self.width, self.height)
    
    def show_start_page(self):
        self.change_size(self.start_page.width, self.start_page.height)
        self.start_page.pack()

    def change_size(self, width, height):
        self.width = width
        self.height = height
        self.geometry("{}x{}".format(self.width, self.height))