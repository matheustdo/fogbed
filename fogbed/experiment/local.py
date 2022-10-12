from typing import List, Type
from fogbed.emulation import EmulationCore
from fogbed.exceptions import ContainerNotFound

from fogbed.net import Fogbed
from fogbed.topo import FogTopo

from mininet.cli import CLI
from mininet.node import Controller, Docker, Switch, UserSwitch


class FogbedExperiment:
    def __init__(self, topology: FogTopo, controller=Controller, switch: Type[Switch]=UserSwitch) -> None:
        self.topology = topology
        self.topology.create()
        self.net = Fogbed(topo=topology, controller=controller, switch=switch)
    
    def _get_all_docker_names(self) -> List[str]:
        return [container.name for container in self.net.hosts]
    
    def get_node(self, name: str) -> Docker:
        if(not name in self._get_all_docker_names()):
            raise ContainerNotFound(f'Container {name} not found.')
        return self.net[name]

    def remove_node(self, name: str):            
        datacenter = EmulationCore.get_virtual_instance_by_container(name)
        datacenter.containers.pop(name)
        self.net.removeDocker(name)

    def start_cli(self):
        CLI(self.net)

    def start(self):
        self.net.start()

    def stop(self):
        self.net.stop()
