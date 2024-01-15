import tkinter as tk
from chessbase import Faction

class PlayerUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_player()

    def create_player(self):
        #username = self.user1.get_username()
        #total = self.user1.get_total()
        #wins = self.user1.get_wins()
        username = "null"
        total = 0
        wins = 0
        win_rate = wins/total*100 if total != 0 else 0

        self.frame1 = tk.LabelFrame(self)
        self.flabel1 = tk.Label(self.frame1, text="黑方信息")
        self.ulabel1 = tk.Label(self.frame1, text="用户名:%s"%username)
        self.tlabel1 = tk.Label(self.frame1, text="总场次:%d"%total)
        self.rlabel1 = tk.Label(self.frame1, text="胜率:%.2f%%"%win_rate)

        self.frame1.configure(borderwidth=3, relief='solid')
        self.flabel1.pack(anchor="w")
        self.ulabel1.pack(anchor="w")
        self.tlabel1.pack(anchor="w")
        self.rlabel1.pack(anchor="w")
        self.frame1.grid(row=0, column=0)

        #username = self.user2.get_username()
        #total = self.user2.get_total()
        #wins = self.user2.get_wins()

        self.frame2 = tk.LabelFrame(self)
        self.flabel2 = tk.Label(self.frame2, text="白方信息")
        self.ulabel2 = tk.Label(self.frame2, text="用户名:%s"%username)
        self.tlabel2 = tk.Label(self.frame2, text="总场次:%d"%total)
        self.rlabel2 = tk.Label(self.frame2, text="胜率:%.2f%%"%win_rate)

        self.frame2.configure(borderwidth=1, relief='solid')
        self.flabel2.pack(anchor="w")
        self.ulabel2.pack(anchor="w")
        self.tlabel2.pack(anchor="w")
        self.rlabel2.pack(anchor="w")
        self.frame2.grid(row=0, column=1)

    def update_user1(self, username, total, wins):
        win_rate = wins/total*100 if total != 0 else 0
        self.ulabel1.configure(text="用户名:%s"%username)
        self.tlabel1.configure(text="总场次:%d"%total)
        self.rlabel1.configure(text="胜率:%.2f%%"%win_rate)
    
    def update_user2(self, username, total, wins):
        win_rate = wins/total*100 if total != 0 else 0
        self.ulabel2.configure(text="用户名:%s"%username)
        self.tlabel2.configure(text="总场次:%d"%total)
        self.rlabel2.configure(text="胜率:%.2f%%"%win_rate)

    def update_cur_player(self, faction):
        if faction == 0:
            self.frame1.configure(borderwidth=3, relief='solid')
            self.frame2.configure(borderwidth=1, relief='solid')
        else:
            self.frame1.configure(borderwidth=1, relief='solid')
            self.frame2.configure(borderwidth=3, relief='solid')

