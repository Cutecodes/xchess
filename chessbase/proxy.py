from enum import Enum
from .utils import *
from .error import *
from .rule import Rule
from .board import Board
from .piece import Piece,PieceFactory,PieceRole
from .memento import Memento
from .command import CommandHistory
from .chessgame import ChessGame

class ProxyMode(Enum):
    LOCAL = 0
    SERVER = 1
    CLIENT = 2

class Proxy:
    def __init__(self,mode:ProxyMode=ProxyMode.LOCAL , game:ChessGame=None, host=()):
        self.mode = mode
        if self.mode != ProxyMode.LOCAL and host == ():
            raise NotImplementedError
        
        self.game = game
        self.user_info1 = None
        self.user_info2 = None
        self.message_list = []

    def set_userinfo1(self, user_info):
        self.user_info1 = user_info

    def set_userinfo2(self, user_info):
        self.user_info2 = user_info

    def get_userinfo(self):
        return self.user_info1,self.user_info2

    def get_message_list(self):
        return self.message_list

    def get_board(self):
        result = None
        try:
            result = self.game.get_board()
        except Exception as e:
            self.message_list.append(str(e))

        return result

    def get_cur_faction(self):
        result = None
        try:
            result = self.game.get_cur_faction()
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def get_state(self):
        result = None
        try:
            result = self.game.get_state()
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def return_result(self):
        result = None
        try:
            result = self.game.return_result()
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def add_piece(self, faction:Faction, piece_role:PieceRole, position):
        result = None
        try:
            result = self.game.add_piece(faction,piece_role,position)
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def move_piece(self, faction:Faction, origin_pos, target_pos):
        result = None
        try:
            result = self.game.move_piece(faction,origin_pos,target_pos)
        except Exception as e:
            self.message_list.append(str(e))

        return result  
    def give_up(self, faction:Faction):
        result = None
        try:
            result = self.game.give_up(faction)
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def skip(self, faction:Faction):
        result = None
        try:
            result = self.game.skip(faction)
        except Exception as e:
            self.message_list.append(str(e))

        return result   
    def board_init(self):
        result = None
        try:
            result = self.game.board_init()
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def restart(self):
        result = None
        try:
            result = self.game.restart()
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def retract(self, faction:Faction):
        result = None
        try:
            result = self.game.retract(faction)
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def execute_command(self, command): 
        result = None  
        try:
            result = self.game.execute_command(command)
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def undo_command(self):
        result = None      
        try:
            result = self.game.undo_command()
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def save(self, save_history_command=False) -> Memento:
        result = None
        try:
            result = self.game.save(save_history_command)
        except Exception as e:
            self.message_list.append(str(e))

        return result 
    def restore(self, memento:Memento):
        result = None
        try:
            result = self.game.restore(memento)
        except Exception as e:
            self.message_list.append(str(e))

        return result
    def get_state_at(self, index):
        result = None	
        try:
            result = self.game.get_state_at(index)
        except Exception as e:
            self.message_list.append(str(e))

        return result