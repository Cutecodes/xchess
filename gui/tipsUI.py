import tkinter as tk

class TipsUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text="Tips:鼠标单击指定位置可以下棋哦~")
        self.bn1 = tk.Button(self, text="隐藏提示", command=self.no_show)
        self.bn2 = tk.Button(self, text="显示提示", command=self.show)
        self.label.pack()
        self.bn1.pack()

    def update_tips(self, tips):
        self.label.configure(text="Tips:{}".format(tips))

    def no_show(self):
        self.label.pack_forget()
        self.bn1.pack_forget()
        self.bn2.pack()

    def show(self):
        self.label.pack()
        self.bn1.pack()
        self.bn2.pack_forget()
    