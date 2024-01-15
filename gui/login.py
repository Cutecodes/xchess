import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from .start_page import StartPage

class Login(tk.Frame):
    def __init__(self, parent=None,width=300, height=200):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.create_login_page()
        self.parent.change_size(self.width, height)

    def login(self):
        username = self.uname.get()
        passwd = self.pwd.get()
        
        user_info = self.parent.client.login(username, passwd)
        if user_info:
            self.parent.user_info = user_info
            self.delete_login_page()
            self.pack_forget()
            self.parent.show_start_page()
        else:
            messagebox.showinfo("提示", "用户不存在或密码错误！")

    def register(self):
        username = self.uname.get()
        passwd = self.pwd.get()
        
        user_info = self.parent.client.register(username, passwd)
        if user_info:
            messagebox.showinfo("提示", "注册成功，请登录！")
        else:
            messagebox.showinfo("提示", "用户名已存在！")

    def login_with_guest(self):
        user_info = {'username':'guest','passwd':None,'total':0,'wins':0}
        if user_info:
            self.parent.user_info = user_info
            self.delete_login_page()
            self.pack_forget()
            self.parent.show_start_page()
        else:
            print("error")

    def create_login_page(self):
        self.ulabel = tk.Label(text='username:')
        self.ulabel.place(x=50, y=30)
        self.uname = tk.Entry()
        self.uname.place(x=120, y=30)

        self.plabel = tk.Label(text='password:')
        self.plabel.place(x=50, y=70)
        self.pwd = tk.Entry(show = '*')
        self.pwd.place(x=120, y=70)

        self.login_button = tk.Button(text='  login ', command=self.login)
        self.login_button.place(x=90, y=110)
        self.register_button = tk.Button(text='register', command=self.register)
        self.register_button.place(x=150, y=110)
        self.login_with_button = tk.Button(text='login with guest', command=self.login_with_guest)
        self.login_with_button.place(x=90, y=150)
    
    def delete_login_page(self):
        self.ulabel.place_forget()
        self.uname.place_forget()

        self.plabel.place_forget()
        self.pwd.place_forget()

        self.login_button.place_forget()
        self.register_button.place_forget()
        self.login_with_button.place_forget()
