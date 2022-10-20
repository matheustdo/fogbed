from enum import Enum, auto

class DivisionMethod(Enum):
    UP = auto()
    DOWN = auto()
    RANDOM = auto()

class SelectionMethod(Enum):
    SEQUENTIAL = auto()
    RANDOM = auto()