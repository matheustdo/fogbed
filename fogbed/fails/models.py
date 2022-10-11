from fogbed.fails import DivisionMethod, FailMode, FailModel

class InstanceFailModel(FailModel):
    def __init__(self, mode: FailMode.ALPHA, fail_rate=0.5, division_method=DivisionMethod.UP, life_time=60):
        self.mode = mode
        self.fail_rate = fail_rate
        self.division_method = division_method
        self.life_time = life_time

class NodeFailModel(FailModel):
    def __init__(self, mode: FailMode.ALPHA, life_time=60):
        self.mode = mode
        self.life_time = life_time