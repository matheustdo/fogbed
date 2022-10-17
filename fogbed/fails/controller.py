import random
from threading import Timer
from fogbed.experiment.local import FogbedExperiment
from fogbed.emulation import EmulationCore
from fogbed.fails import FailMode, SelectionMethod
from fogbed.fails.utils import calculateDivision
from fogbed.node.container import Container
from fogbed.node.instance import VirtualInstance
from fogbed.resources import ResourceModel


class FailController:
    def __init__(self, experiment: FogbedExperiment):
        self.experiment = experiment


    def stopNodeOnTime(self, node: Container):
        life_time = node.fail_model.life_time

        def action():
            self.experiment.remove_node(node.name)

            def action2():
                vis = EmulationCore.virtual_instances()
                print(vis['cloud'])
                vis['cloud'].addDocker('d8', resources=ResourceModel.SMALL)
        
            timer2 = Timer(5, action2, [])
            timer2.start()
        
        timer = Timer(life_time, action, [])
        timer.start()
    

    def stopNodesOnTime(self, vi: VirtualInstance):
        vi_fail_model = vi.fail_model
        life_time = vi_fail_model.life_time

        def action():
            fail_rate = vi_fail_model.fail_rate
            division_method = vi_fail_model.division_method
            selection_method = vi_fail_model.selection_method
            all_nodes = list(vi.containers.keys())
            vi_len = len(vi.containers)
            stop_amount = calculateDivision(vi_len, fail_rate, division_method)

            if(selection_method == SelectionMethod.SEQUENTIAL):
                for idx, node_name in enumerate(all_nodes):
                    if (idx < stop_amount):
                        self.experiment.remove_node(node_name)
                    else:
                        break
            else:
                idx_to_remove = random.sample(range(0, vi_len), stop_amount)
                next_idx = idx_to_remove.pop(0)

                for idx, node_name in enumerate(all_nodes):
                    if (idx == next_idx):
                        self.experiment.remove_node(node_name)

                        if (len(idx_to_remove) == 0):
                            break

                        next_idx = idx_to_remove.pop(0)
                        
        
        timer = Timer(life_time, action, [])
        timer.start()


    def viFailSwitch(self, vi: VirtualInstance):
        mode = vi.fail_model.mode

        if mode == FailMode.CRASH:
            self.stopNodesOnTime(vi)

    def nodeFailSwitch(self, node: Container):
        mode = node.fail_model.mode
        
        if mode == FailMode.CRASH:
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
