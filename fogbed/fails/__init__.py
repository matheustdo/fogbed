
from abc import ABC, abstractmethod


class FailModel(ABC):
    @abstractmethod
    def assignVirtualInstance(self, vi_name):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass