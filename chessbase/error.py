class TurnError(Exception):
    def __init__(self):
        self.err_msg = "It's not your turn!"

    def __str__(self):
        return self.err_msg

class PieceExistError(Exception):
    def __init__(self):
        self.err_msg = "There is a piece at this position"
    
    def __str__(self):
        return self.err_msg

class PieceOutError(Exception):
    def __init__(self):
        self.err_msg = "Out of board"
    
    def __str__(self):
        return self.err_msg

class PieceNotExistError(Exception):
    def __init__(self):
        self.err_msg = "There is not a piece at this position"
    
    def __str__(self):
        return self.err_msg

class PieceForbiddenError(Exception):
    def __init__(self):
        self.err_msg = "The position is forbidden"
    
    def __str__(self):
        return self.err_msg

class RetractOutError(Exception):
    def __init__(self):
        self.err_msg = "Reached maximum retract times"

    def __str__(self):
        return self.err_msg

class GameOver(Exception):
    def __init__(self, err_msg):
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg