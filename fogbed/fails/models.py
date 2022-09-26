from enum import Enum, auto

from fogbed.fails import FailModel
from fogbed.emulation import EmulationCore

class DivisionMethod(Enum):
    UP = auto()
    DOWN = auto()
    RANDOM = auto()

class AlphaFailModel(FailModel):
    def __init__(self, fail_rate=1.0, division_method=DivisionMethod.UP):
        self.fail_rate = fail_rate
        self.division_method = division_method

    def assignVirtualInstance(self, vi_name):
        self.vi_name = vi_name
        self.virtual_instance = EmulationCore.virtual_instances()[vi_name]

    def run(self):
        print('rodou')
    
    def stop(self):
        print('parou')