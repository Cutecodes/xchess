import sys
sys.path.append("..")
import copy
from abc import ABC, abstractmethod
from typing import List
from chessbase import Faction, Result
from chessbase import Board
from chessbase import Piece
from chessbase import Rule
from chessbase import PieceForbiddenError
from chessbase import PieceFactory, PieceRole

class GoRule(Rule):
    def __init__(self):
        self.forbidden = None

    def get_next_faction(self, board:Board, cur_faction:Faction, factions:List[Faction]) -> Faction:
        if len(factions) != 2:
            raise NotImplementedError

        if cur_faction == factions[0]:
            return factions[1]
        else:
            return factions[0]
    
    def check_qi(self, chain, board_state, x, y, qi_state, is_visied, faction:Faction):
        size = len(board_state)
        direction = [(-1,0),(0,1),(1,0),(0,-1)]
        if is_visied[x][y] == False and 0 <= x and 0 <= y and x < size and y < size:
            is_visied[x][y] = True
            chain.append((x,y))
        else:
            return

        for d in direction:
            n_x = x + d[0]
            n_y = y + d[1]
            if 0 <= n_x and 0 <= n_y and n_x < size and n_y < size:
                if board_state[n_x][n_y] is None:
                    qi_state[x][y] += 1
                elif board_state[n_x][n_y].get_faction() == faction:
                    if is_visied[n_x][n_y] == False:
                        self.check_qi(chain, board_state, n_x, n_y, qi_state, is_visied, faction)
                        qi_state[x][y] += qi_state[n_x][n_y]
        
    def remove_piece(self, board:Board, faction:Faction):
        board_state = board.get_state()
        size = board.get_size()
        is_visied = [[False for j in range(size)] for i in range(size)]
        qi_state = [[0 for j in range(size)] for i in range(size)]

        for x in range(size):
            for y in range(size):
                if board_state[x][y] and board_state[x][y].get_faction() == faction:
                    chain = []
                    self.check_qi(chain, board_state, x, y, qi_state, is_visied, faction)
                    for p in chain:
                        i,j = p[0],p[1]
                        qi_state[i][j] = qi_state[x][y]
        
        rm_pieces = []
        for x in range(size):
            for y in range(size):
                if board_state[x][y] and board_state[x][y].get_faction() == faction and \
                        qi_state[x][y] == 0:
                    
                    piece = board.remove_piece((x,y))
                    rm_pieces.append((piece,(x,y)))
        
        return rm_pieces

    def add_piece(self, board:Board, piece:Piece, position) -> List[Piece]:
        cur_faction = piece.get_faction()
        # 0. check forbidden position
        if self.forbidden is not None:
            f = self.forbidden[0].get_faction()
            p = self.forbidden[1]
            if f == cur_faction and p == position:
                raise PieceForbiddenError
    
    	# 1. we add piece directly        
        board.add_piece(piece, position)
        
        # 2. we check and remove enemy faction's piece
        enemy_faction = self.get_next_faction(Board, cur_faction, [Faction.BLACK, Faction.WHITE])
        rm_pieces = self.remove_piece(board, enemy_faction)

        # 3. we check and remove current faction's piece
        rm_pieces.extend(self.remove_piece(board, cur_faction))

        # 4. add forbidden position
        if len(rm_pieces) == 1:
            if rm_pieces[0][1] == position:
                raise PieceForbiddenError
            else:
                self.forbidden = rm_pieces[0]
        else:
            self.forbidden = None

        rm_pieces = [p[0] for p in rm_pieces]
        return rm_pieces
    
    def move_piece(self, board:Board, origin_pos, target_pos) -> List[Piece]:
    	# go not support move piece
        raise NotImplementedError

    def can_continue(self, board:Board) -> bool:
        board_state = board.get_state()
        size = board.get_size()
        is_visied = [[False for j in range(size)] for i in range(size)]
        qi_state = [[0 for j in range(size)] for i in range(size)]

        piecefactory = PieceFactory()
        black_piece = piecefactory.get_piece(Faction.BLACK,PieceRole.DEFAULT)
        white_piece = piecefactory.get_piece(Faction.WHITE,PieceRole.DEFAULT)
        tmp_board = copy.deepcopy(board)
        for x in range(size):
            for y in range(size):
                if board_state[x][y] is None:
                    try:
                        tmp_board.add_piece(black_piece, (x,y))
                    except PieceForbiddenError:
                        pass
                    else:
                        return True

                if board_state[x][y] is None:
                    try:
                        tmp_board.add_piece(white_piece, (x,y))
                    except PieceForbiddenError:
                        pass
                    else:
                        return True
        # all faction can not add piece, game is over
        return False
    
    def coumpte_score(self, board:Board, cur_faction:Faction):
        # assume there is no dead piece and all is closed, we may implement it after
        # bfs to coumpte faction
        board_state = board.get_state()
        size = board.get_size()

        is_visied = [[False for j in range(size)] for i in range(size)]
        # score > 0 black+1,score = 0 , black += 0.5, if all is closed, should no 0.5 
        score = [[0.0 for j in range(size)] for i in range(size)]
        direction = [(-1,0),(0,1),(1,0),(0,-1)]
        
        q = []
        for x in range(size):
            for y in range(size):
                if board_state[x][y] and board_state[x][y].get_faction() == Faction.BLACK and \
                        is_visied[x][y] == False :
                    q.append((x,y))
                    while len(q):
                        cur_x, cur_y = q[0][0],q[0][1]
                        q.pop(0)
                        if is_visied[cur_x][cur_y] == True:
                            continue
                        score[cur_x][cur_y] += 1
                        is_visied[cur_x][cur_y] = True
                        for d in direction:
                            n_x = cur_x + d[0]
                            n_y = cur_y + d[1]
                            if 0 <= n_x and 0 <= n_y and n_x < size and n_y < size:
                                if board_state[n_x][n_y] is None:
                                    score[n_x][n_y] += 1
                                    q.append((n_x,n_y))
                                elif board_state[n_x][n_y].get_faction() == Faction.BLACK:
                                    q.append((n_x,n_y))

                elif board_state[x][y] and board_state[x][y].get_faction() == Faction.WHITE and \
                        is_visied[x][y] == False :
                    q.append((x,y))
                    while len(q):
                        cur_x, cur_y = q[0][0],q[0][1]
                        q.pop(0)
                        if is_visied[cur_x][cur_y] == True:
                            continue
                        score[cur_x][cur_y] -= 1
                        is_visied[cur_x][cur_y] = True
                        for d in direction:
                            n_x = cur_x + d[0]
                            n_y = cur_y + d[1]
                            if 0 <= n_x and 0 <= n_y and n_x < size and n_y < size:
                                if board_state[n_x][n_y] is None:
                                    score[n_x][n_y] -= 1
                                    q.append((n_x,n_y))
                                elif board_state[n_x][n_y].get_faction() == Faction.WHITE:
                                    q.append((n_x,n_y))
            
            black_score = 0
            for x in range(size):
                for y in range(size):
                    if score[x][y] > 0:
                        black_score += 1
                    elif score[x][y] > -0.5:
                        black_score += 0.5
            return black_score  

    def get_result(self, board:Board, cur_faction:Faction) -> Result:
        size = board.get_size()
        if self.coumpte_score(board, cur_faction) > (size * size) / 2:
            return Result.BLACK_WIN
        else:
            return Result.WHITE_WIN
        
        
        



        
