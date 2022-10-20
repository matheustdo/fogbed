from fogbed.fails import DivisionMethod, FailModel, FailMode, SelectionMethod

class CrashFail(FailModel):
    def __init__(self, fail_rate=0.5, division_method=DivisionMethod.UP, life_time=30, selection_method=SelectionMethod.SEQUENTIAL):
        self.fail_rate = fail_rate
        self.selection_method = selection_method
        self.life_time = life_time
        self.division_method = division_method
        super().__init__(FailMode.CRASH)