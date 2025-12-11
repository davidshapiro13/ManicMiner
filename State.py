#State Definition Dec 10 2025
#David Shapiro
from constants import BLANK_STATE

class State():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
    def set_stateType(self, state_type):
        self.type = state_type

    def __str__(self):
        return "X: " + str(self.x) + ", Y: " + str(self.y) + ", type: " + str(self.type)
    def __repr__(self):
        return self.__str__()