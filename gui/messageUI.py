import tkinter as tk
import time

class MessageUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.text = tk.Text(self, width=30, height=30)
        self.scrollbar = tk.Scrollbar(self, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH)

    def update_message(self, message):
        self.text.insert(tk.END, "[{}]:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),message))
        self.text.see(tk.END)

    def update_messages(self, message_list):
        self.text.delete(1.0,tk.END)
        for m in message_list:
            self.text.insert(tk.END,m+"\n")
        self.text.see(tk.END)