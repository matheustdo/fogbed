from fogbed.experiment import Experiment
from fogbed.fails.models import FailModel, FailMode, Intervaler
from fogbed.node.container import Container
from fogbed.node.instance import VirtualInstance
import random
import time, threading

class AvailabilityFail(FailModel):
    def __init__(self, availability=0.5, slot_time=2.0):
        self.availability = availability
        self.slot_time = slot_time
        super().__init__(FailMode.AVAILABILITY)

class AvailabilityCycler(Intervaler):
    def __init__(self, experiment: Experiment, vi: VirtualInstance, availability: float, slot_time: float):
        self.experiment = experiment
        self.vi = vi
        self.availability = availability
        self.slot_time = slot_time
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.__set_interval)
        self.running = False
        self.all_containers = self.vi.containers.copy()
        self.first_cycle = True

    def action(self):
        all_containers_names = list(self.all_containers.keys())
        all_containers_amount = len(self.all_containers)
        stop_amount = int(all_containers_amount * self.availability)
        down_sorted_idxs = random.sample(range(0, all_containers_amount), stop_amount)
        down_sorted_names = [all_containers_names[down_sorted_idxs[0]], all_containers_names[down_sorted_idxs[1]]]
        cur_containers_names = list(self.vi.containers.keys())
        to_stop = []

        for container_name in cur_containers_names:
            ''' Discover which containers will stop '''
            if (container_name == down_sorted_names[0] or container_name == down_sorted_names[1]):
                to_stop.append(container_name)
        
        for container_name in to_stop:
            ''' Stop containers '''
            self.experiment.remove_docker(container_name)

        if (not self.first_cycle):
            to_start = []

            for container_name in all_containers_names:
                ''' Discover which containers will start '''
                if (container_name != down_sorted_names[0] and container_name != down_sorted_names[1] and container_name not in cur_containers_names):
                    to_start.append(container_name)
                    
            for container_name in to_start:
                ''' Start containers '''
                resources = self.all_containers[container_name].resources
                fail_model = self.all_containers[container_name].fail_model
                container = Container(container_name, resources=resources, fail_model=fail_model)
                self.experiment.add_docker(container, self.vi)
                
        self.first_cycle = False

    def __set_interval(self):
        next_time = time.time() + self.slot_time

        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.slot_time
            self.action()

    def is_alive(self):
        return self.running

    def start(self):
        print('*** Starting Availability Fail on ' + self.vi.label)
        self.action()
        self.thread.start()
        self.running = True

    def cancel(self):
        print('*** Stopping Availability Fail on ' + self.vi.label)
        self.stop_event.set()
        self.running = False
