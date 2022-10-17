from threading import Timer
from typing import List
from fogbed.experiment import Experiment
from fogbed.fails import FailMode
from fogbed.fails.utils import calculate_division, stop_node_on_time, stop_nodes_on_time
from fogbed.node.container import Container
from fogbed.node.instance import VirtualInstance


class FailController:
    def __init__(self, experiment: Experiment):
        self.experiment = experiment
        self.thread_list: List[Timer] = []


    def switch_virtual_instance_fail(self, virtual_instance: VirtualInstance):
        fail_model = virtual_instance.fail_model
        mode = fail_model.mode

        if mode == FailMode.CRASH:
            thread = stop_nodes_on_time(self.experiment, virtual_instance, fail_model.fail_rate, fail_model.life_time, fail_model.division_method, fail_model.selection_method)
            self.thread_list.append(thread)
            thread.start()


    def switch_node_fail(self, node: Container):
        fail_model = node.fail_model
        mode = fail_model.mode
        
        if mode == FailMode.CRASH:
            thread = stop_node_on_time(self.experiment, node, fail_model.life_time)
            self.thread_list.append(thread)
            thread.start()


    def start(self):
        virtual_instances = self.experiment.get_virtual_instances()
        
        for virtual_instance in virtual_instances:
            nodes = virtual_instance.containers

            for node_key in nodes:
                node = nodes[node_key]
                
                if node.fail_model is not None:
                    self.switch_node_fail(node)
            
            if virtual_instance.fail_model is not None:
                self.switch_virtual_instance_fail(virtual_instance)

    def stop(self):
        for thread in self.thread_list:
            if(thread.is_alive()):
                thread.cancel()
