from fogbed.experiment import Experiment
from fogbed.fails.models import FailModel, FailMode, Intervaler
from fogbed.node.container import Container
from fogbed.node.instance import VirtualInstance
import random
import time, threading
from fractions import Fraction

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
        self.first_slot = True
        self.slot_number = 0
        self.cycle_size = 1
        self.cycle_part = 0
        self.cycle_step = 0
        self.average = 0

    def print_average(self, amount: int):
        self.average += amount
        print('')
        print('*** SLOT NUMBER: ' + str(self.slot_number))
        print('*** AVERAGE: ' + str((self.average / self.slot_number) / len(self.all_containers)) )
        print('')


    def action(self):
        self.slot_number += 1
        all_containers_names = list(self.all_containers.keys())
        all_containers_amount = len(self.all_containers)
        stop_amount = self.calcule_stop_amount()
        self.print_average(stop_amount)
        down_sorted_idxs = random.sample(range(0, all_containers_amount), stop_amount)
        down_sorted_names = [all_containers_names[down_sorted_idxs[0]], all_containers_names[down_sorted_idxs[1]]]
        cur_containers_names = list(self.vi.containers.keys())
        to_stop = []

        for container_name in cur_containers_names:
            ''' Discover which containers will stop '''
            if (container_name in down_sorted_names):
                to_stop.append(container_name)
        
        for container_name in to_stop:
            ''' Stop containers '''
            self.experiment.remove_docker(container_name)

        if (not self.first_slot):
            to_start = []

            for container_name in all_containers_names:
                ''' Discover which containers will start '''
                if (container_name not in down_sorted_names and container_name not in cur_containers_names):
                    to_start.append(container_name)
                    
            for container_name in to_start:
                ''' Start containers '''
                resources = self.all_containers[container_name].resources
                fail_model = self.all_containers[container_name].fail_model
                container = Container(container_name, resources=resources, fail_model=fail_model)
                self.experiment.add_docker(container, self.vi)
                
        self.first_slot = False

    def __set_interval(self):
        next_time = time.time() + self.slot_time

        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.slot_time
            self.action()

    def is_alive(self):
        return self.running

    def calcule_stop_amount(self):
        if (self.cycle_step >= self.cycle_size):
            self.cycle_step = 0

        if (self.cycle_size > 1):
            if (self.cycle_step < self.cycle_size - self.cycle_part):
                self.cycle_step += 1
                return self.cycle_amount
            elif (self.cycle_step < self.cycle_size):
                self.cycle_step += 1
                return self.cycle_amount + 1
        else:
            return self.cycle_amount

    def calculate_period_size(self):
        all_containers_amount = len(self.all_containers)
        division_factor = round(all_containers_amount * self.availability, 1)
        integer_part = int(division_factor) 
        decimal_part = int((division_factor % 1)* 10) 

        if (decimal_part > 0):
            simplified_parts = Fraction(10, decimal_part)
            numerator = simplified_parts.numerator
            denominator = simplified_parts.denominator
            self.cycle_size = numerator
            self.cycle_part = denominator
            self.cycle_amount = integer_part

    def start(self):
        print('*** Starting Availability Fail on ' + self.vi.label)
        self.calculate_period_size()
        self.action()
        self.thread.start()
        self.running = True

    def cancel(self):
        print('*** Stopping Availability Fail on ' + self.vi.label)
        self.stop_event.set()
        self.running = False
