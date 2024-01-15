import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from .game_page import GamePage, GamePageDirector, GogamePageBuilder,GobanggamePageBuilder,OthellogamePageBuilder
from common import PlayerID

class SetPage(tk.Frame):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.is_join = False

        self.create_picture()
        self.picture.pack()

        self.create_input()
        self.input.pack()

        self.create_start()
        self.start.pack()

        self.create_join()
        self.join.pack()
        
        self.create_player()
        self.frame1.pack()
        self.frame2.pack()
        self.show_network()

        self.pack()

    def create_picture(self):
        self.picture =  tk.Label(self)

    def create_input(self):
        self.entry_var = tk.StringVar()
        self.input = tk.Entry(self,textvariable=self.entry_var,width=100)
        self.entry_var.set('please input the board size(8-19)')

    def create_start(self):
        self.start = tk.Button(self, text='开始游戏', command=self.start_game)

    def create_join(self):
        self.join = tk.Button(self, text="加入游戏", command=self.join_game)

    def create_player(self):
        self.frame1 = tk.Frame(self)        
        self.player1 = tk.IntVar()
        self.label1 = tk.Label(self.frame1, text="玩家1")
        self.rb1 = tk.Radiobutton(self.frame1, text='AI1', value=PlayerID.AI1.value, variable=self.player1, relief=tk.FLAT, command=self.show_network)
        self.rb2 = tk.Radiobutton(self.frame1, text='AI2', value=PlayerID.AI2.value, variable=self.player1, relief=tk.FLAT, command=self.show_network)
        self.rb3 = tk.Radiobutton(self.frame1, text='AI3', value=PlayerID.AI3.value, variable=self.player1, relief=tk.FLAT, command=self.show_network)
        self.rb4 = tk.Radiobutton(self.frame1, text='HUMAN', value=PlayerID.HUMAN.value, variable=self.player1, relief=tk.FLAT, command=self.show_network)
        self.player1.set(PlayerID.HUMAN.value)
        self.label1.grid(row=0, column=0)
        self.rb1.grid(row=0, column=1)
        self.rb2.grid(row=0, column=2)
        self.rb3.grid(row=0, column=3)
        self.rb4.grid(row=0, column=4)
        
        self.frame2 = tk.Frame(self)        
        self.player2 = tk.IntVar()
        self.label2 = tk.Label(self.frame2, text="玩家2")
        self.rb5 = tk.Radiobutton(self.frame2, text='AI1', value=PlayerID.AI1.value, variable=self.player2, relief=tk.FLAT, command=self.show_network)
        self.rb6 = tk.Radiobutton(self.frame2, text='AI2', value=PlayerID.AI2.value, variable=self.player2, relief=tk.FLAT, command=self.show_network)
        self.rb7 = tk.Radiobutton(self.frame2, text='AI3', value=PlayerID.AI3.value, variable=self.player2, relief=tk.FLAT, command=self.show_network)
        self.rb8 = tk.Radiobutton(self.frame2, text='HUMAN', value=PlayerID.HUMAN.value, variable=self.player2, relief=tk.FLAT, command=self.show_network)
        self.player2.set(PlayerID.HUMAN.value)
        self.label2.grid(row=0, column=0)
        self.rb5.grid(row=0, column=1)
        self.rb6.grid(row=0, column=2)
        self.rb7.grid(row=0, column=3)
        self.rb8.grid(row=0, column=4)

        self.frame3 = tk.Frame(self)
        self.first = tk.IntVar()
        self.rb9 = tk.Radiobutton(self.frame3, text="先手", value=0, variable=self.first)
        self.rb10 = tk.Radiobutton(self.frame3, text="后手", value=1, variable=self.first)
        self.first.set(0)
        self.ip_label = tk.Label(self.frame3, text="IP地址:")
        self.ip = tk.StringVar()
        self.ip.set("0.0.0.0")
        self.ip_inupt = tk.Entry(self.frame3, textvariable=self.ip)
        self.port_label = tk.Label(self.frame3, text="端口号:")
        self.port = tk.StringVar()
        self.port.set("4315")
        self.port_input = tk.Entry(self.frame3, textvariable=self.port)
        self.rb9.grid(row=0,column=0)
        self.rb10.grid(row=0,column=1)
        self.ip_label.grid(row=1,column=0)
        self.ip_inupt.grid(row=1,column=1)
        self.port_label.grid(row=2,column=0)
        self.port_input.grid(row=2,column=1)
    
    def show_network(self):
        if self.player1.get() == PlayerID.HUMAN.value and self.player2.get() == PlayerID.HUMAN.value:
            #self.frame3.pack()
            pass
        else:
            self.frame3.pack_forget()

    
    def join_game(self):
        self.is_join = True
        self.start_game()

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
                player1 = self.player1.get()
                player2 = self.player2.get()
                user_info = self.parent.user_info
                first = self.first.get()
                ip = self.ip.get()
                port = int(self.port.get())
                is_join = self.is_join

                self.create_game(board_size, user_info, first, player1, player2, (ip,port), is_join)
                self.pack_forget()



class GobangSetPage(SetPage):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent,width,height)

    def create_picture(self):
        image = Image.open("./asset/gobang.png")    
        self.image = ImageTk.PhotoImage(image.resize((round(0.7*self.width),round(0.7*self.height))))    
        self.picture = tk.Label(self,image=self.image)
    
    def create_game(self,board_size, user_info, first, player1, player2, host, is_join):
        gobanggame_page_builder = GobanggamePageBuilder(self.parent, board_size, user_info, first, player1, player2, host, is_join)
        game_page_director =  GamePageDirector(gobanggame_page_builder)
        game_page_director.make()
        game_page = gobanggame_page_builder.get_game_page()
        game_page.packs()

class GoSetPage(SetPage):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent,width,height)

    def create_picture(self):
        image = Image.open("./asset/go.png")    
        self.image = ImageTk.PhotoImage(image.resize((round(0.7*self.width),round(0.7*self.height))))    
        self.picture = tk.Label(self,image=self.image)

    def create_game(self,board_size, user_info, first, player1, player2, host, is_join):
        gogame_page_builder = GogamePageBuilder(self.parent, board_size, user_info, first, player1, player2, host, is_join)
        game_page_director =  GamePageDirector(gogame_page_builder)
        game_page_director.make()
        game_page = gogame_page_builder.get_game_page()
        game_page.packs()

class OthelloSetPage(SetPage):
    def __init__(self, parent=None,width=100, height=100):
        super().__init__(parent,width,height)

    def create_input(self):
        self.entry_var = tk.StringVar()
        self.input = tk.Entry(self,textvariable=self.entry_var,width=100)
        self.entry_var.set("8(othello's board_size is always 8)")

    def start_game(self):
        self.entry_var.set("8")
        super().start_game()

    def create_picture(self):
        image = Image.open("./asset/othello.png")    
        self.image = ImageTk.PhotoImage(image.resize((round(0.7*self.width),round(0.7*self.height))))    
        self.picture = tk.Label(self,image=self.image)
    
    def create_game(self,board_size, user_info, first, player1, player2, host, is_join):
        gobanggame_page_builder = OthellogamePageBuilder(self.parent, board_size, user_info, first, player1, player2, host, is_join)
        game_page_director =  GamePageDirector(gobanggame_page_builder)
        game_page_director.make()
        game_page = gobanggame_page_builder.get_game_page()
        game_page.packs()