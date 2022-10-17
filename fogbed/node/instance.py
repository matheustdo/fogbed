from itertools import chain
from typing import Dict, Optional

from fogbed.exceptions import ContainerNotFound, ResourceModelNotFound
from fogbed.fails import FailModel
from fogbed.node.container import Container
from fogbed.resources import ResourceModel

from mininet.node import Docker
from mininet.topo import Topo


class VirtualInstance(object):
    COUNTER = 0

    def __init__(self, name: str) -> None:
        self.label    = name
        self.switch   = self._create_switch()
        self.containers: Dict[str, Container] = {}
        self.resource_model: Optional[ResourceModel] = None
        self.fail_model: Optional[FailModel] = None
        
    
    def assignResourceModel(self, resource_model: ResourceModel):
        self.resource_model = resource_model


    def assignFailModel(self, fail_model: FailModel):
        self.fail_model = fail_model    
    

    def create_container(self, container: Container):
        if(self.resource_model is None):
            raise ResourceModelNotFound('Assign a resource model to this virtual instance.')
        
        self._set_default_params(container)
        self.resource_model.allocate(container)
        self.containers[container.name] = container

    
    def _create_switch(self) -> str:
        VirtualInstance.COUNTER += 1
        return f's{VirtualInstance.COUNTER}'
    

    def create_topology(self) -> Topo:
        topology = Topo()
        topology.addSwitch(self.switch)
        
        for container in self.containers.values():
            topology.addHost(container.name, cls=Docker, **container.params)
            topology.addLink(container.name, self.switch)
        return topology
    

    def remove_container(self, name: str):
        if(not name in self.containers):
            ContainerNotFound(f'Container {name} not found.')
        
        container = self.containers[name]
        if(self.resource_model is not None):
            self.resource_model.free(container)
        self.containers.pop(name)
    

    def _set_default_params(self, container: Container):
        if(container.params.get('dimage') is None):
            container.params['dimage'] = 'ubuntu:trusty'

        if(container.resources is None):
            container.params['resources'] = ResourceModel.TINY

    @property
    def compute_units(self) -> float:
        if(self.resource_model is None): return 0.0
        return self.resource_model.max_cu
    
    @property
    def memory_units(self) -> int:
        if(self.resource_model is None): return 0
        return self.resource_model.max_mu

    def __repr__(self) -> str:
        return f'VirtualInstance(name={self.label})'

    def __str__(self) -> str:
        containers = [repr(container) for container in self.containers.values()]
        header = f'[{self.label}]\n'
        return header + '\n'.join(containers)
    
    def __iter__(self):
        for container in chain(self.containers.values()):
            yield container
