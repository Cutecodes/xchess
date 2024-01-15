import tkinter as tk

class OpsUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.restart = tk.Button(self, text="重新开始")
        self.retract = tk.Button(self, text="悔棋一步")
        self.giveup = tk.Button(self, text="认输")
        self.save = tk.Button(self, text="保存游戏")
        self.restore = tk.Button(self, text="加载存档")
        self.skip = tk.Button(self, text="虚着")
        self.replay = tk.Button(self, text="回放")
        self.entry_var = tk.StringVar()
        self.input = tk.Entry(self,textvariable=self.entry_var,width=30)
        self.entry_var.set('please input filename to load or save')
        
        self.restart.grid(row=0,column=0)
        self.retract.grid(row=0,column=1)
        self.giveup.grid(row=0,column=2)
        self.save.grid(row=1,column=0)
        self.restore.grid(row=1,column=1)
        self.skip.grid(row=1,column=2)
        self.replay.grid(row=2,column=0)
        self.input.grid(row=3,column=0, columnspan=3)
