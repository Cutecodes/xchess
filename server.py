import sys
import os
from common import SERVER_HOST, SERVER_PORT
from account import UserList

from flask import Flask, request

user_list = UserList()
server = Flask("chess server")

@server.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    
    user_info = user_list.user_login(username, passwd)
    
    if user_info:
        return user_info
    else:
        return '{}'

@server.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    
    user_info = user_list.user_register(username, passwd)
    if user_info:
        return user_info
    else:
        return '{}'

@server.route('/update',methods=['POST'])
def update():
    username = request.form.get('username')
    passwd = request.form.get('passwd')

    d_total = request.form.get('d_total')
    d_wins = request.form.get('d_wins')

    user_info = user_list.user_update(username, passwd, d_total, d_wins)
    if user_info:
        return user_info
    else:
        return '{}'

if __name__ == '__main__':
    server.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)

