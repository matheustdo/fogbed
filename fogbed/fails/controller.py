from threading import Timer
from typing import List, Union
from fogbed.experiment import Experiment
from fogbed.fails import Cycler
from fogbed.fails.models import FailMode
from fogbed.fails.models.availability import AvailabilityCycler
from fogbed.fails.utils import kill_node_on_time, kill_nodes_on_time, down_node_net_on_time
from fogbed.node.container import Container
from fogbed.node.instance import VirtualInstance


class FailController:
    """ The FailController allows, encapsulate and manages Fogbed failures """
    def __init__(self, experiment: Experiment):
        """ experiment: experiment to control failures """
        self.experiment = experiment
        self.thread_list: List[Union[Timer, Cycler]] = []


    def switch_virtual_instance_fail(self, virtual_instance: VirtualInstance):
        """ Handles virtual instance failure according to its mode
            virtual_instance: virtual_instance with the fail """
        fail_model = virtual_instance.fail_model
        mode = fail_model.mode

        if mode == FailMode.CRASH:
            thread = kill_nodes_on_time(self.experiment, virtual_instance, fail_model.fail_rate, fail_model.life_time, fail_model.split_method, fail_model.selection_method)
            thread.start()
            self.thread_list.append(thread)
        elif mode == FailMode.AVAILABILITY:
            thread = AvailabilityCycler(self.experiment, virtual_instance, fail_model.availability, fail_model.slot_time)
            thread.start()
            self.thread_list.append(thread)


    def switch_node_fail(self, node: Container):
        """ Handles node failure according to its mode
            node: node with the fail """
        fail_model = node.fail_model
        mode = fail_model.mode
        
        if mode == FailMode.CRASH:
            thread = kill_node_on_time(self.experiment, node, fail_model.life_time)
            thread.start()
            self.thread_list.append(thread)
        elif mode == FailMode.DISCONNECT:
            thread = down_node_net_on_time(node, fail_model.life_time)
            thread.start()
            self.thread_list.append(thread)


    def start(self):
        """ Inits the fail controller """
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
        """ Stops the fail controller """
        for thread in self.thread_list:
            if(thread.is_alive()):
                thread.cancel()
