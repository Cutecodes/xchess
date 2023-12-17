class Memento:
    def __init__(self, state):
        self.__state = state

    def get_state(self):
        return self.__state