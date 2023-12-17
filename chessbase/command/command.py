from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, chess_game):
        self._chess_game = chess_game

    def save(self):
        self.memento = self._chess_game.save()

    def undo(self):
        self._chess_game.restore(self.memento)

    @abstractmethod
    def execute():
        pass

class CommandHistory:
    def __init__(self):
        self.__history:list[Command] = []

    def push(self, command:Command):
        self.__history.append(command)

    def pop(self):
        if len(self.__history):
            return self.__history.pop()
        else:
            return None

    