from abc import ABC
from enum import Enum, auto

class DivisionMethod(Enum):
    UP = auto()
    DOWN = auto()
    RANDOM = auto()

class FailMode(Enum):
    CRASH = auto()

class SelectionMethod(Enum):
    SEQUENTIAL = auto()
    RANDOM = auto()

class FailModel(ABC):
    def __init__(self, mode: FailMode):
        self.mode = mode