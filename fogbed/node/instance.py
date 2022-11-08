from itertools import chain
from typing import Dict, Optional

from fogbed.exceptions import ContainerNotFound
from fogbed.fails.models import FailModel
from fogbed.exceptions import ContainerNotFound
from fogbed.node.container import Container
from fogbed.resources import ResourceModel



class VirtualInstance(object):
    COUNTER = 0

    def __init__(self, 
        name: str, 
        resource_model: Optional[ResourceModel] = None,
        fail_model: Optional[FailModel] = None
    ):
        self.label      = name
        self.switch     = self._create_switch()
        self._ip        = ''
        self._reachable = False
        self.containers: Dict[str, Container] = {}
        self.resource_model: Optional[ResourceModel] = resource_model
        self.fail_model: Optional[FailModel] = fail_model
    
    def create_container(self, container: Container):
        self._set_default_params(container)

        if(self.resource_model is not None):
            self.resource_model.allocate(container)
        self.containers[container.name] = container

    
    def _create_switch(self) -> str:
        VirtualInstance.COUNTER += 1
        return f's{VirtualInstance.COUNTER}'
    

    def remove_container(self, name: str):
        if(not name in self.containers):
            ContainerNotFound(f'Container {name} not found.')
        
        container = self.containers[name]
        if(self.resource_model is not None):
            self.resource_model.free(container)
        self.containers.pop(name)
    
    def get_ip(self) -> str:
        return self._ip

    def set_ip(self, ip: str):
        self._ip = ip
    
    def set_reachable(self, reachable: bool):
        self._reachable = reachable
        
    def _set_default_params(self, container: Container):
        if(container.resources is None):
            container._params['resources'] = ResourceModel.TINY

    @property
    def is_reachable(self) -> bool:
        return self._reachable

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
