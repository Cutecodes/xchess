from chessbase import Player, Faction, ChessGame, GameState
from chessbase import AddPieceCommand, PieceRole, Result
from chessbase import PieceFactory
from chessbase import Board
import random
import copy
from .rule import OthelloRule
import numpy as np

class OthelloLevel_1(Player):
    def __init__(self, user = None, faction:Faction = Faction.BLACK,game:ChessGame=None):
        super().__init__(user, faction,game)
    

    def get_valid_position(self, board:Board, faction:Faction):
        valid_position = []
        size = board.get_size()
        board_state = board.get_state()
        direction = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

        for x in range(size):
            for y in range(size):
                if board_state[x][y] and board_state[x][y].get_faction() == faction:                    
                    for d in direction:
                        cur_x,cur_y = x,y
                        tmp_num = 0
                        n_x, n_y = cur_x + d[0], cur_y + d[1]
                        while 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and board_state[n_x][n_y] and \
                                board_state[n_x][n_y].get_faction() != faction:
                            tmp_num += 1
                            cur_x, cur_y = n_x, n_y
                            n_x, n_y = cur_x+d[0], cur_y+d[1]
                        if tmp_num >= 1 and 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and \
                                board_state[n_x][n_y] is None:
                            valid_position.append((n_x,n_y))

        return valid_position

    def add_piece(self, game:ChessGame):
        board = game.get_board()
        cur_faction = game.get_cur_faction()
        valid_position = []

        if cur_faction == self._faction:
            valid_position = self.get_valid_position(board, cur_faction)
        else:
            return

        position = random.choice(valid_position)

        add_piece_command = AddPieceCommand(game, cur_faction, PieceRole.DEFAULT, position)

        try:
            game.execute_command(add_piece_command)        
        except Exception as e:
            print(e)

    def run(self):
        while self._game.get_state() != GameState.END:
            self.add_piece(self._game)


class OthelloLevel_2(OthelloLevel_1):
    def __init__(self, user = None, faction:Faction = Faction.BLACK,game:ChessGame=None):
        super().__init__(user, faction, game)
    
        self.Vmap = [[500,-25,10,5,5,10,-25,500],
                    [-25,-45,1,1,1,1,-45,-25],
                    [10,1,3,2,2,3,1,10],
                    [5,1,2,1,1,2,1,5],
                    [5,1,2,1,1,2,1,5],
                    [10,1,3,2,2,3,1,10],
                    [-25,-45,1,1,1,1,-45,-25],
                    [500,-25,10,5,5,10,-25,500]]
        self.piecefactory = PieceFactory()
        self.rule = OthelloRule()
    
    def evaluation(self, board:Board, faction:Faction, valid_position):
        score = 0
        for position in valid_position:
            x = position[0]
            y = position[1]
            if self.Vmap[x][y]> score:
                score = self.Vmap[x][y]
        return score 
    
    def get_best_position(self, board:Board, faction:Faction, valid_position):
        piece = self.piecefactory.get_piece(faction,PieceRole.DEFAULT)

        if faction == Faction.BLACK:
            next_faction = Faction.WHITE
        else:
            next_faction = Faction.BLACK

        max_score = -1000
        best_position = valid_position[0]
        for position in valid_position:
            x = position[0]
            y = position[1]
            tmp_board = copy.deepcopy(board)
            self.rule.add_piece(tmp_board,piece,position)
            n_valid_position = self.get_valid_position(tmp_board,next_faction)
            score = self.Vmap[x][y] - self.evaluation(tmp_board, next_faction, n_valid_position)
            if score > max_score:
                max_score = score
                best_position = position

        return best_position
        

    def add_piece(self, game:ChessGame):
        board = game.get_board()
        cur_faction = game.get_cur_faction()
        valid_position = []

        if cur_faction == self._faction:
            valid_position = self.get_valid_position(board, cur_faction)
        else:
            return

        position = self.get_best_position(board, cur_faction, valid_position)

        add_piece_command = AddPieceCommand(game, cur_faction, PieceRole.DEFAULT, position)

        try:
            game.execute_command(add_piece_command)        
        except Exception as e:
            print(e)



class Node:
    def __init__(self, parent=None):
        self.visits = 0
        self.reward = 0.0
        self.children = {}
        self.parent = parent

    def get_value(self, c_puct):
        return self.reward/self.visits + c_puct* np.sqrt(2*np.log(self.parent.visits)/self.visits)




class OthelloLevel_3(Player):
    def __init__(self, user = None, faction:Faction = Faction.BLACK,game:ChessGame=None):
        super().__init__(user, faction, game)    
        self.piecefactory = PieceFactory()
        self.rule = OthelloRule()
        self.max_times = 200
        self.c_puct = 2
        self.Vmap = [[500,-25,10,5,5,10,-25,500],
                    [-25,-45,1,1,1,1,-45,-25],
                    [10,1,3,2,2,3,1,10],
                    [5,1,2,1,1,2,1,5],
                    [5,1,2,1,1,2,1,5],
                    [10,1,3,2,2,3,1,10],
                    [-25,-45,1,1,1,1,-45,-25],
                    [500,-25,10,5,5,10,-25,500]]
    
    def expand(self, node, valid_position):
        for p in valid_position:
            if p not in node.children.keys():
                node.children[p] = Node(node)
    
    def select(self, node):
        max_v = 0
        cur_n = None
        cur_a = None
        for a,n in node.children.items():
            if n.visits == 0:
                return a,n
            else:
                v = n.get_value(self.c_puct)
                if v > max_v:
                    max_v = v
                    cur_n = n
                    cur_a = a

        return cur_a,cur_n

    def simulation(self, action, node, board, cur_faction):
        tmp_board = copy.deepcopy(board)
        faction = cur_faction
        piece = self.piecefactory.get_piece(cur_faction,PieceRole.DEFAULT)
        self.rule.add_piece(tmp_board,piece,action)

        while self.rule.can_continue(tmp_board):
            cur_faction = self.rule.get_next_faction(tmp_board, cur_faction, [Faction.BLACK,Faction.WHITE])
            valid_position = self.get_valid_position(tmp_board,cur_faction)
            piece = self.piecefactory.get_piece(cur_faction,PieceRole.DEFAULT)
            if random.random() > 0.5:
                position = self.get_best_position_by_score(tmp_board, cur_faction,valid_position)
            else:
                position = random.choice(valid_position)
            if position is None:
                break
            self.rule.add_piece(tmp_board,piece,position)
        
        result = self.rule.get_result(tmp_board, faction)
        if  result == Result.BLACK_WIN:
            win_faction = Faction.BLACK
        elif result == Result.WHITE_WIN:
            win_faction = Faction.WHITE
        else:
            win_faction = None

        if win_faction == faction:
            reward = 1 
        else:
            reward = 0
        if result == Result.STALEMATE:
            reward = 0.5
        self.backpropogate(node, reward)

    def backpropogate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    
    def get_valid_position(self, board:Board, faction:Faction):
        '''
        获取可以下的位置
        '''
        valid_position = []
        size = board.get_size()
        board_state = board.get_state()
        direction = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

        for x in range(size):
            for y in range(size):
                if board_state[x][y] and board_state[x][y].get_faction() == faction:                    
                    for d in direction:
                        cur_x,cur_y = x,y
                        tmp_num = 0
                        n_x, n_y = cur_x + d[0], cur_y + d[1]
                        while 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and board_state[n_x][n_y] and \
                                board_state[n_x][n_y].get_faction() != faction:
                            tmp_num += 1
                            cur_x, cur_y = n_x, n_y
                            n_x, n_y = cur_x+d[0], cur_y+d[1]
                        if tmp_num >= 1 and 0 <= n_x and 0 <= n_y and n_x < size and n_y < size and \
                                board_state[n_x][n_y] is None:
                            valid_position.append((n_x,n_y))

        return valid_position
    
    def evaluation(self, board:Board, faction:Faction, valid_position):
        score = 0
        for position in valid_position:
            x = position[0]
            y = position[1]
            if self.Vmap[x][y]> score:
                score = self.Vmap[x][y]
        return score 
    def get_best_position_by_score(self, board:Board, faction:Faction, valid_position):
        piece = self.piecefactory.get_piece(faction,PieceRole.DEFAULT)

        if faction == Faction.BLACK:
            next_faction = Faction.WHITE
        else:
            next_faction = Faction.BLACK

        max_score = -1000
        best_position = valid_position[0]
        for position in valid_position:
            x = position[0]
            y = position[1]
            tmp_board = copy.deepcopy(board)
            self.rule.add_piece(tmp_board,piece,position)
            n_valid_position = self.get_valid_position(tmp_board,next_faction)
            score = self.Vmap[x][y] - self.evaluation(tmp_board, next_faction, n_valid_position)
            if score > max_score:
                max_score = score
                best_position = position

        return best_position
    
    def get_best_position(self, board:Board, faction:Faction, valid_position):
       
        root = Node(None)
        self.expand(root, valid_position)
        times = 0

        while times < self.max_times:
            times += 1
            action, node = self.select(root)
            if action is None:
                action = valid_position[0]
            self.simulation(action, node, board, faction)

        max_v = 0
        cur_a = valid_position[0]
        for a,n in root.children.items():
            v = n.reward/n.visits
            if v > max_v:
                max_v = v
                cur_a = a

        best_position = cur_a
        return best_position
        

    def add_piece(self, game:ChessGame):
        board = game.get_board()
        cur_faction = game.get_cur_faction()
        valid_position = []

        if cur_faction == self._faction:
            valid_position = self.get_valid_position(board, cur_faction)
        else:
            return

        position = self.get_best_position(board, cur_faction, valid_position)

        add_piece_command = AddPieceCommand(game, cur_faction, PieceRole.DEFAULT, position)

        try:
            game.execute_command(add_piece_command)        
        except Exception as e:
            print(e)

    def run(self):
        while self._game.get_state() != GameState.END:
            self.add_piece(self._game)