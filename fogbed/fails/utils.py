import math
import random
from fogbed.experiment import Experiment
from fogbed.fails import DivisionMethod, SelectionMethod
from fogbed.node.container import Container
from threading import Timer

from fogbed.node.instance import VirtualInstance

def calculate_division(value: float, factor: float, division_method: DivisionMethod):
    if division_method == DivisionMethod.RANDOM:
        return random.Random.randint(0, int)
    elif division_method == DivisionMethod.DOWN:
        return math.floor(value * factor)

    return math.ceil(value * factor)


def stop_node_on_time(experiment: Experiment, node: Container, life_time: int):
    def action():
        experiment.remove_docker(node.name)
    
    timer = Timer(life_time, action, [])
    return timer


def stop_nodes_on_time(experiment: Experiment, vi: VirtualInstance, fail_rate: float, life_time: int, division_method: DivisionMethod, selection_method: SelectionMethod):
    def action():
        all_nodes = list(vi.containers.keys())
        vi_len = len(vi.containers)
        stop_amount = calculate_division(vi_len, fail_rate, division_method)

        if(selection_method == SelectionMethod.SEQUENTIAL):
            for idx, node_name in enumerate(all_nodes):
                if (idx < stop_amount):
                    experiment.remove_docker(node_name)
                else:
                    break
        else:
            idx_to_remove = random.sample(range(0, vi_len), stop_amount)
            next_idx = idx_to_remove.pop(0)

            for idx, node_name in enumerate(all_nodes):
                if (idx == next_idx):
                    experiment.remove_docker(node_name)

                    if (len(idx_to_remove) == 0):
                        break

                    next_idx = idx_to_remove.pop(0)
                    
    timer = Timer(life_time, action, [])
    return timer

'''
async def down_node_net(node: Docker,  secs: float):
    print('* Net down scheduled for ' + node.name + ' in ' + str(secs) + 's...')
    time.sleep(secs)
    
    try:
        node.cmd('ifconfig ' + node.name + '-eth0 down')
        print('* Net down on: ' + node.name)
    except Exception as ex: 
        print(ex)


async def up_node_net(node: Docker,  secs: float):
    print('* Net up scheduled for ' + node.name + ' in ' + str(secs) + 's...')
    time.sleep(secs)

    try:
        node.cmd('ifconfig ' + node.name + '-eth0 up')
        print('* Net up on: ' + node.name)
    except Exception as ex: 
        print(ex)
'''