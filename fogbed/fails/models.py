from fogbed.fails import DivisionMethod, FailMode, FailModel, SelectionMethod


class InstanceFailModel(FailModel):
    def __init__(self, mode: FailMode.CRASH, fail_rate=0.5, division_method=DivisionMethod.UP, life_time=60, selection_method=SelectionMethod.SEQUENTIAL):
        self.mode = mode
        self.fail_rate = fail_rate
        self.selection_method = selection_method
        self.life_time = life_time
        self.division_method = division_method

class NodeFailModel(FailModel):
    def __init__(self, mode: FailMode.CRASH, life_time=60):
        self.mode = mode
        self.life_time = life_time