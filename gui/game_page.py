import tkinter as tk
import math
from PIL import Image, ImageTk
from tkinter import messagebox
from abc import ABC, abstractmethod
from .boardUI import BoardUI,BoardUIMode
from .messageUI import MessageUI
from .opsUI import OpsUI
from .tipsUI import TipsUI
from chessbase import ChessGame
from go import GoRule
from gobang import GobangRule
from chessbase import Board
from chessbase import PieceFactory, PieceRole
from chessbase import Faction
from chessbase import PieceExistError, PieceOutError, PieceForbiddenError
from chessbase import RetractOutError, GameOver
from chessbase import AddPieceCommand, RestartCommand, RetractCommand, GiveupCommand
from chessbase import SkipCommand, SaveCommand, RestoreCommand

class GamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__game = None
        self.__boardUI = None
        self.__tips = None
        self.__ops = None
        self.__message = None
        
    def set_game(self, game):
        self.__game = game

    def set_boardUI(self, boardui):
        self.__boardUI = boardui

    def set_tips(self, tips):
        self.__tips = tips
    
    def set_ops(self, ops):
        self.__ops = ops

    def set_message(self, message):
        self.__message = message

    def packs(self):
        if self.__boardUI:
            self.__boardUI.set_board(self.__game.get_board())
            self.__boardUI.get_canvas().pack()
            self.__boardUI.bind("<Button-1>", self.board_on_click)
            self.__boardUI.grid(row=0, column=0, rowspan=3)
        if self.__tips:
            self.__tips.grid(row=0, column=1)
        if self.__ops:
            self.__ops.restart.configure(command=self.restart)
            self.__ops.retract.configure(command=self.retract)
            self.__ops.giveup.configure(command=self.giveup)
            self.__ops.save.configure(command=self.save)
            self.__ops.restore.configure(command=self.restore)
            self.__ops.skip.configure(command=self.skip)
            self.__ops.grid(row=1, column=1)
        if self.__message:
            self.__message.grid(row=2, column=1)
            self.__message.update_message("welcome to XCHESS!")
            self.__message.update_message("black first")
        self.pack()

    def update(self):
        self.__boardUI.set_board(self.__game.get_board())
        self.__boardUI.get_canvas().update()
        self.__boardUI.get_canvas().pack()

    def restart(self):
        restart_command = RestartCommand(self.__game)
        try:
            self.__game.execute_command(restart_command)
        except Exception as e:
            print(e)
        else:
            if self.__message:
                self.__message.update_message("restart successfully")
        finally:
            cur_faction = self.__game.get_cur_faction()
            if cur_faction == Faction.BLACK:
                player = "black"
            else:
                player = "white"
            if self.__message:
                self.__message.update_message("cur player is {} ".format(player))

            self.update()

    def retract(self):
        cur_faction = self.__game.get_cur_faction()
        if cur_faction == Faction.BLACK:
            last_faction = Faction.WHITE
        else:
            last_faction = Faction.BLACK
        retract_command = RetractCommand(self.__game, last_faction)
        try:
            self.__game.execute_command(retract_command)
        except RetractOutError:
            if self.__message:
                self.__message.update_message("reach max retract times")
        except Exception as e:
            print(e)
        else:
            if self.__message:
                self.__message.update_message("retract successfully")
        finally:
            cur_faction = self.__game.get_cur_faction()
            if cur_faction == Faction.BLACK:
                player = "black"
            else:
                player = "white"
            if self.__message:
                self.__message.update_message("cur player is {} ".format(player))

            self.update()
    
    def giveup(self):
        cur_faction = self.__game.get_cur_faction()
        giveup_command = GiveupCommand(self.__game, cur_faction)
        try:
            self.__game.execute_command(giveup_command)
        except GameOver as e:
            self.show_result(e)
        except Exception as e:
            print(e)

    def save(self):
        filename = ""
        if self.__ops:
            filename = self.__ops.entry_var.get()
        save_command = SaveCommand(self.__game, filename)
        try:
            self.__game.execute_command(save_command)
        except GameOver as e:
            self.show_result(e)
        except Exception as e:
            if self.__message:
                self.__message.update_message("{}".format(e))
            print(e)
        else:
            if self.__message:
                self.__message.update_message("save to {} successfully".format(filename))
            self.update()

    def restore(self):
        filename = ""
        if self.__ops:
            filename = self.__ops.entry_var.get()
        restore_command = RestoreCommand(self.__game, filename)
        try:
            self.__game.execute_command(restore_command)
        except GameOver as e:
            self.show_result(e)
        except Exception as e:
            if self.__message:
                self.__message.update_message("{}".format(e))
            print(e)
        else:
            if self.__message:
                self.__message.update_message("restore from {} successfully".format(filename))
        self.update()  

    def skip(self):
        cur_faction = self.__game.get_cur_faction()
        if cur_faction == Faction.BLACK:
            player = "black"
        else:
            player = "white"
        skip_command = SkipCommand(self.__game, cur_faction)
        try:
            self.__game.execute_command(skip_command)
        except GameOver as e:
            self.show_result(e)
        except Exception as e:
            print(e)
        else:
            if self.__message:
                self.__message.update_message("{} skip successfully".format(player))

            cur_faction = self.__game.get_cur_faction()
            if cur_faction == Faction.BLACK:
                player = "black"
            else:
                player = "white"
            if self.__message:
                self.__message.update_message("cur player is {} ".format(player))
            
            self.update()


    def board_on_click(self, event):
        #print("clicked at:", event.x, event.y)
        self.__boardUI.get_canvas().delete(tk.ALL)
        grid_size = self.__boardUI.get_grid_size()
        if self.__boardUI.get_mode() == BoardUIMode.CROSS:
            x = round(event.x / grid_size) - 1
            y = round(event.y / grid_size) - 1
        elif self.__boardUI.get_mode() == BoardUIMode.GRID:
            x = math.floor((event.x - grid_size) / grid_size)
            y = math.floor((event.y - grid_size) / grid_size)
        else:
            if self.__message:
                self.__message.update_message("Not support BoardUI Mode")

       
        cur_faction = self.__game.get_cur_faction()
        if cur_faction == Faction.BLACK:
            player = "black"
        else:
            player = "white"
        if self.__message:
            self.__message.update_message("{} try add piece at {} {}".format(player,x,y))
        add_piece_command = AddPieceCommand(self.__game, cur_faction, PieceRole.DEFAULT, (x,y))

        
        try:
            self.__game.execute_command(add_piece_command)
        except PieceExistError:
            if self.__message:
                self.__message.update_message("position:({} {}) is placed".format(x,y))
        except PieceOutError:
            if self.__message:
                self.__message.update_message("position:({} {}) is out of board".format(x,y))
        except PieceForbiddenError:
            if self.__message:
                self.__message.update_message("position:({} {}) is forbbiden".format(x,y))
        except GameOver as e:
            self.show_result(e)
        except Exception as e:
            print(e)
        else:
            if self.__message:
                self.__message.update_message("{} add piece at {} {} successfully".format(player,x,y))

            cur_faction = self.__game.get_cur_faction()
            if cur_faction == Faction.BLACK:
                player = "black"
            else:
                player = "white"
            if self.__message:
                self.__message.update_message("cur player is {} ".format(player))
        self.update()
            
    
    def show_result(self, e):
        messagebox.showinfo("提示", "{}".format(e))
        self.parent.destroy()
        exit(0)


class GamePageBuilder(ABC):
    def __init__(self, parent, board_size):
        self.parent = parent
        self.board_size = board_size

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_game_page(self) -> GamePage:
        pass

    @abstractmethod
    def build_game(self):
        pass
    
    @abstractmethod
    def build_boardUI(self):
        pass
    
    @abstractmethod
    def build_tips(self):
        pass
    
    @abstractmethod
    def build_ops(self):
        pass
    
    @abstractmethod
    def build_message(self, message):
        pass

class GogamePageBuilder(GamePageBuilder):
    def __init__(self, parent, board_size):
        super().__init__(parent, board_size)

    def reset(self):
        self.__game_page = GamePage(self.parent)

    def get_game_page(self) -> GamePage:
        return self.__game_page

    def build_game(self):
        board = Board(self.board_size)
        rule = GoRule()
        piecefactory = PieceFactory()
        game = ChessGame(board, rule, piecefactory)
        self.__game_page.set_game(game)
    
    def build_boardUI(self):
        boardui = BoardUI(self.__game_page)
        boardui.set_board_texture("./asset/back.png")
        boardui.set_black_texture("./asset/black.png")
        boardui.set_white_texture("./asset/white.png")
        self.__game_page.set_boardUI(boardui)
        
    def build_tips(self):
        tipsui = TipsUI(self.__game_page)
        self.__game_page.set_tips(tipsui)
    
    def build_ops(self):
        ops = OpsUI(self.__game_page)
        self.__game_page.set_ops(ops)
    
    def build_message(self):
        messageui = MessageUI(self.__game_page)
        self.__game_page.set_message(messageui)

class GobanggamePageBuilder(GamePageBuilder):
    def __init__(self, parent, board_size):
        super().__init__(parent, board_size)

    def reset(self):
        self.__game_page = GamePage(self.parent)

    def get_game_page(self) -> GamePage:
        return self.__game_page

    def build_game(self):
        board = Board(self.board_size)
        rule = GobangRule()
        piecefactory = PieceFactory()
        game = ChessGame(board, rule, piecefactory)
        self.__game_page.set_game(game)
    
    def build_boardUI(self):
        boardui = BoardUI(self.__game_page)
        boardui.set_board_texture("./asset/back.png")
        boardui.set_black_texture("./asset/black.png")
        boardui.set_white_texture("./asset/white.png")
        self.__game_page.set_boardUI(boardui)
        
    def build_tips(self):
        tipsui = TipsUI(self.__game_page)
        self.__game_page.set_tips(tipsui)
    
    def build_ops(self):
        ops = OpsUI(self.__game_page)
        self.__game_page.set_ops(ops)
    
    def build_message(self):
        messageui = MessageUI(self.__game_page)
        self.__game_page.set_message(messageui)
    

class GamePageDirector:
    def __init__(self, builder:GamePageBuilder):
        self.__builder = builder

    def make(self) -> GamePage:
        self.__builder.reset()
        self.__builder.build_game()
        self.__builder.build_boardUI()
        self.__builder.build_tips()
        self.__builder.build_ops()
        self.__builder.build_message()
        return self.__builder.get_game_page()