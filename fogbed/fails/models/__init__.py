

from abc import ABC, abstractmethod
from enum import Enum, auto

class FailMode(Enum):
    CRASH = auto()
    AVAILABILITY = auto()

class FailModel(ABC):
    def __init__(self, mode: FailMode):
        self.mode = mode

class Intervaler(ABC):
    @abstractmethod
    def is_alive(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def cancel(self):
        pass