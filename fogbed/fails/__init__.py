from enum import Enum, auto
from abc import ABC, abstractmethod

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
    def __init__(self):
        pass
