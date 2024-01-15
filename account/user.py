import sys
sys.path.append("..")
import os
import json

from common import ACCOUNT_FILE
class User:
    def __init__(self, username, passwd, total = 0, wins = 0):
        self.__username = username
        self.__passwd = passwd
        self.__total = total
        self.__wins = wins

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_passwd(self):
        return self.__passwd

    def set_passwd(self, passwd):
        self.__passwd = passwd
    
    def get_total(self):
        return self.__total

    def add_total(self, d_total):
        self.__total += d_total
    
    def get_wins(self):
        return self.__wins

    def add_wins(self, d_wins):
        self.__wins += d_wins

class UserList:
    def __init__(self, file=ACCOUNT_FILE):
        self.__filepath = os.path.join(os.path.dirname(__file__) + os.path.sep + "..", file)
        self.__users = {}


        with open(self.__filepath,'r') as f:
            line = f.readline()
            while line:
                value = line.strip().split()
                username = value[0]
                passwd = value[1]
                total = int(value[2])
                wins = int(value[3])
                user = User(username, passwd, total, wins)
                self.__users[username] = user
                line = f.readline()
    
    def write_file(self):
        with open(self.__filepath,'w+') as f:
            for user in self.__users.values():
                username = user.get_username()
                passwd = user.get_passwd()
                total = user.get_total()
                wins = user.get_wins()
                f.write(f"{username} {passwd} {total} {wins}\n")

    def user_login(self, username, passwd):
        if username not in self.__users.keys():
            return None

        user = self.__users[username]
        if user.get_passwd() == passwd:
            user_info = {'username':user.get_username(),'passwd':user.get_passwd(),\
                    'total':user.get_total(),'wins':user.get_wins()}
            return json.dumps(user_info)
        else:
            return None
    
    def user_register(self, username, passwd):
        if username in self.__users.keys():
            return None
        user = User(username, passwd)
        self.__users[username] = user
        user_info = {'username':user.get_username(),'passwd':user.get_passwd(),\
                'total':user.get_total(),'wins':user.get_wins()}

        self.write_file()
        return json.dumps(user_info)


    def user_update(self, username, passwd, d_total, d_wins):
        if username not in self.__users.keys():
            return None

        user = self.__users[username]
        if user is None or user.get_passwd() != passwd:
            return None

        user.add_total(int(d_total))
        user.add_wins(int(d_wins))

        user_info = {'username':user.get_username(),'passwd':user.get_passwd(),\
                'total':user.get_total(),'wins':user.get_wins()}

        self.write_file()
        return json.dumps(user_info)

        



