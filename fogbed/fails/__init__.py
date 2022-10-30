from abc import ABC, abstractmethod
from enum import Enum, auto

class SplitMethod(Enum):
    UP = auto()
    DOWN = auto()
    RANDOM = auto()

class SelectionMethod(Enum):
    SEQUENTIAL = auto()
    RANDOM = auto()

class Cycler(ABC):
    @abstractmethod
    def is_alive(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def cancel(self):
        pass