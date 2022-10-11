from random import random
from threading import Timer
from fogbed.experiment.local import FogbedExperiment
from fogbed.emulation import EmulationCore
from fogbed.fails import FailMode
from fogbed.fails.utils import calculateDivision
from fogbed.node.container import Container
from fogbed.node.instance import VirtualInstance


class FailController:
    def __init__(self, experiment: FogbedExperiment):
        self.experiment = experiment


    def stopNodeOnTime(self, node: Container):
        life_time = node.fail_model.life_time

        def action():
            self.experiment.get_node(node.name).stop()
        
        timer = Timer(life_time, action, [])
        timer.start()
    

    def stopNodesOnTime(self, vi: VirtualInstance):
        vi_fail_model = vi.fail_model
        life_time = vi_fail_model.life_time

        def action():
            fail_rate = vi_fail_model.fail_rate
            division_method = vi_fail_model.division_method
            all_nodes = list(vi.containers.keys())
            vi_len = len(vi.containers)
            stop_amount = calculateDivision(vi_len, fail_rate, division_method)

            for idx, node in enumerate(all_nodes):
                if (idx < stop_amount):
                    try:
                        self.experiment.get_node(node).stop()
                    except: 
                        pass
        
        timer = Timer(life_time, action, [])
        timer.start()


    def viFailSwitch(self, vi: VirtualInstance):
        mode = vi.fail_model.mode

        if mode == FailMode.ALPHA:
            self.stopNodesOnTime(vi)

    def nodeFailSwitch(self, node: Container):
        mode = node.fail_model.mode
        
        if mode == FailMode.ALPHA:
            self.stopNodeOnTime(node)

    def start(self):
        vis = EmulationCore.virtual_instances()
        
        for key in vis:
            vi = EmulationCore.virtual_instances()[key]
            nodes = vi.containers

            for node_key in nodes:
                node = nodes[node_key]
                
                if node.fail_model is not None:
                    self.nodeFailSwitch(node)
            
            if vi.fail_model is not None:
                self.viFailSwitch(vi)
