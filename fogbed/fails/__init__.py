from enum import Enum, auto
from abc import ABC, abstractmethod

class DivisionMethod(Enum):
    UP = auto()
    DOWN = auto()
    RANDOM = auto()

class FailMode(Enum):
    ALPHA = auto()

class FailModel(ABC):
    def __init__(self):
        pass
