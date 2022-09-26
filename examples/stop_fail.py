from fogbed.emulation import EmulationCore
from fogbed.experiment.local import FogbedExperiment
from fogbed.resources import ResourceModel
from fogbed.resources.models import CloudResourceModel, EdgeResourceModel
from fogbed.topo import FogTopo
from fogbed.fails.models import AlphaFailModel, DivisionMethod

from mininet.log import setLogLevel

'''
async def remove_node_by_name(name: str, secs: float, vi: VirtualInstance): 
    print('* Remove scheduled for ' + name + ' in ' + str(secs) + 's...')
    time.sleep(secs)

    try:
        vi.removeDocker(name)
        print('* Node removed successfully: ' + name)
    except Exception as ex: 
        print(ex)

async def add_node(name: str, secs: float, vi: VirtualInstance): 
    print('* Addition scheduled for ' + name + ' in ' + str(secs) + 's...')
    time.sleep(secs)

    try:
        vi.addDocker(name)
        print('* Node removed successfully: ' + name)
    except Exception as ex: 
        print(ex)

async def remove_node(node: Docker, secs: float): 
    print('* Remove scheduled for ' + node.name + ' in ' + str(secs) + 's...')
    time.sleep(secs)
    
    try:
        node.stop()
        print('* Node removed successfully: ' + node.name)
    except Exception as ex: 
        print(ex)

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

setLogLevel('info')

EmulationCore(max_cpu=0.5, max_mem=512)
topo = FogTopo()

edge  = topo.addVirtualInstance('edge')
cloud = topo.addVirtualInstance('cloud')
topo.addLink(edge, cloud, delay='100ms', bw=1)

edge.assignResourceModel(EdgeResourceModel(max_cu=2, max_mu=256))
cloud.assignResourceModel(CloudResourceModel(max_cu=2, max_mu=512))

edge.addDocker('d1', resources=ResourceModel.SMALL)
edge.addDocker('d2', resources=ResourceModel.SMALL)
edge.addDocker('d3', resources=ResourceModel.SMALL)

cloud.addDocker('d4', resources=ResourceModel.SMALL)
cloud.addDocker('d5', resources=ResourceModel.SMALL)
cloud.addDocker('d6', resources=ResourceModel.SMALL)

edge.assignFailModel(AlphaFailModel(fail_rate=1.0, division_method=DivisionMethod.UP))

print(f'{edge}\n')
print(f'{cloud}\n')

exp = FogbedExperiment(topo)

try:
    exp.start()
    
    d1 = exp.get_node('d1')
    d6 = exp.get_node('d6')
    print(d1.resources)
    exp.start_cli()
except Exception as ex: 
    print(ex)
finally:
    exp.stop()
