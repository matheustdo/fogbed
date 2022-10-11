import math
from random import Random
from fogbed.fails import DivisionMethod

def calculateDivision(value: float, factor: float, division_method: DivisionMethod):
    if division_method == DivisionMethod.RANDOM:
        return Random.randint(0, int)
    elif division_method == DivisionMethod.DOWN:
        return math.floor(value * factor)

    return math.ceil(value * factor)

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