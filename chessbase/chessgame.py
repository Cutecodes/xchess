from .utils import *
from .error import *
from .rule import Rule
from .board import Board
from .piece import Piece,PieceFactory,PieceRole
from .memento import Memento
from .command import CommandHistory
import copy

class ChessGame():

    def __init__(self, board:Board, rule:Rule, piece_factory:PieceFactory, factions=[Faction.BLACK, Faction.WHITE], max_retract_times=1):
        self.__factions = factions
        self.__board = board
        self.__init_board = copy.deepcopy(self.__board)
        self.__rule = rule
        self.__piece_factory = piece_factory
        self.__max_retract_times = max_retract_times

        self.restart()

    def get_board(self):
        return self.__board

    def get_cur_faction(self):
        return self.__cur_faction

    def get_state(self):
        return self.__state

    def return_result(self):
        
        result = self.__rule.get_result(self.__board, self.__cur_faction)
        if  result == Result.BLACK_WIN:
            self.__winner = Faction.BLACK
            winner = "black"
        elif result == Result.WHITE_WIN:
            self.__winner = Faction.WHITE
            winner = "white"

        if self.__winner:
            raise GameOver("The winner is {}".format(winner))
        else:
            raise GameOver("draw")

    def add_piece(self, faction:Faction, piece_role:PieceRole, position):
        if faction != self.__cur_faction:
            raise TurnError
         
        piece = self.__piece_factory.get_piece(faction, piece_role)
        pieces = self.__rule.add_piece(self.__board, piece, position)
        self.__cur_faction = self.__rule.get_next_faction(self.__board, self.__cur_faction, self.__factions)
        self.__give_up_state = {f:False for f in self.__factions}
        if not self.__rule.can_continue(self.__board):
            self.__state = GameState.END
            self.return_result()


    def move_piece(self, faction:Faction, origin_pos, target_pos):
        if faction != self.__cur_faction:
            raise TurnError

        pieces = self.__rule.move_piece(self.__board, origin_pos, target_pos)
        self.__cur_faction = self.__rule.get_next_faction(self.__board, self.__cur_faction, self.__factions)
        self.__give_up_state = {f:False for f in self.__factions}
        if not self.__rule.can_continue(self.__board):
            self.return_result()
    
    def give_up(self, faction:Faction):
        if len(self.__factions) == 2:
            if self.__factions[0] == faction:
                self.__winner = self.__factions[1]
            else:
                self.__winner = self.__factions[0]

            if self.__winner == Faction.BLACK:
                winner = "black"
            else:
                winner = "white"
        
            self.__state = GameState.END
            raise GameOver("The winner is {}".format(winner))

    def skip(self, faction:Faction):
        if len(self.__factions) == 2:
            self.__give_up_state[faction] = True
            self.__cur_faction = self.__rule.get_next_faction(self.__board, self.__cur_faction, self.__factions)
            for k in self.__give_up_state.keys():
                if not self.__give_up_state[k]:
                    return

            self.return_result()
    
    def board_init(self):
        # may override for different
        self.__board = copy.deepcopy(self.__init_board)

    def restart(self):
        self.board_init()

        self.__cur_faction = self.__factions[0]
        self.__state = GameState.RUNNING
        self.__winner = None
        self.__history_command = CommandHistory()

        self.__retract_times = {f:0 for f in self.__factions }
        self.__give_up_state = {f:False for f in self.__factions}

    def retract(self, faction:Faction):
        if self.__retract_times[faction] < self.__max_retract_times:
            if self.__cur_faction != faction:
                if self.undo_command():
                    self.__retract_times[faction] += 1
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise RetractOutError

    def execute_command(self, command):
        if self.__state != GameState.RUNNING:
            raise GameOver("game over")
        if (command.execute()):
            self.__history_command.push(command)

    def undo_command(self):
        command = self.__history_command.pop()
        if command:
            command.undo()
            return True 
        else:
            return False

    def save(self, save_history_command=False) -> Memento:
        state = {}
        state['cur_faction'] = self.__cur_faction
        state['state'] = self.__state
        state['winner'] = self.__winner
        state['board'] = copy.deepcopy(self.__board)
        if save_history_command:
            state['history_command'] = copy.deepcopy(self.__history_command)
        state['retract_times'] = copy.deepcopy(self.__retract_times)
        state['give_up_state'] = copy.deepcopy(self.__give_up_state)
        return Memento(state)

    def restore(self, memento:Memento):
        if memento is None:
            return

        state = memento.get_state()
        self.__cur_faction = state['cur_faction']
        self.__state = state['state']
        self.__winner = state['winner']
        self.__board = state['board']
        if 'history_command' in state.keys():
            self.__history_command = state['history_command']
        self.__retract_times = state['retract_times'] 
        self.__give_up_state = state['give_up_state'] 
    
    def get_state_at(self, index):
        length = len(self.__history_command)
        if index < length:
            command = self.__history_command[index]
            memento = command.memento
            if memento is None:
                return None
            else:
                state = memento.get_state()
                return state['board']
        else:
            return None

