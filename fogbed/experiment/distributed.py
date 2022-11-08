from typing import Dict, List, Optional

from fogbed.emulation import Services
from fogbed.exceptions import ContainerNotFound, NotEnoughResourcesAvailable
from fogbed.experiment import Experiment
from fogbed.experiment.helpers import (
    verify_if_container_ip_exists, 
    verify_if_container_name_exists,
    verify_if_datacenter_exists
)
from fogbed.node.instance import VirtualInstance
from fogbed.node.container import Container
from fogbed.node.services.remote_docker import RemoteDocker
from fogbed.node.worker import FogWorker
from fogbed.resources import ResourceModel

from mininet.log import info

class FogbedDistributedExperiment(Experiment):
    def __init__(self, controller_ip: str, controller_port: int) -> None:
        self.controller_ip   = controller_ip
        self.controller_port = controller_port
        self.workers: Dict[str, FogWorker] = {}
        self.is_running = False


    def add_docker(self, container: Container, datacenter: VirtualInstance):
        verify_if_container_name_exists(container.name)
        verify_if_container_ip_exists(container.ip)

        try:
            datacenter.create_container(container)

            if(self.is_running):
                worker = self._get_worker_by_datacenter(datacenter)
                worker.net.add_docker(container.name, **container.params)
                worker.net.add_link(container.name, datacenter.switch)
                worker.net.config_default(container.name)
                service = RemoteDocker(container.name, worker.net.url)
                container.set_docker(service)

        except NotEnoughResourcesAvailable:
            info(f'{container.name}: Allocation of container was blocked by resource model.\n\n')

              

    def add_tunnel(self, worker1: FogWorker, worker2: FogWorker): 
        worker1.add_tunnel(worker2.ip)
        worker2.add_tunnel(worker1.ip)
        

    def add_worker(self, ip: str) -> FogWorker:
        if(ip in self.workers):
            raise Exception(f'Already exist a worker with ip={ip}')

        worker = FogWorker(ip=ip)
        self.workers[worker.ip] = worker
        return worker
    

    def add_virtual_instance(self, name: str, resource_model: Optional[ResourceModel] = None) -> VirtualInstance:
        verify_if_datacenter_exists(name)
        datacenter = VirtualInstance(name, resource_model)
        Services.add_virtual_instance(datacenter)
        return datacenter


    def get_containers(self) -> List[Container]:
        return Services.get_all_containers()


    def get_docker(self, name: str) -> Container:
        container = Services.get_container_by_name(name)
        
        if(container is None):
            raise ContainerNotFound(f'Container {name} not found.')
        return container


    def get_virtual_instances(self) -> List[VirtualInstance]:
        return list(Services.virtual_instances().values())

    def _get_worker_by_datacenter(self, datacenter: VirtualInstance) -> FogWorker:
        return self.workers[datacenter.get_ip()]

    def remove_docker(self, name: str):
        datacenter = Services.get_virtual_instance_by_container(name)
        datacenter.remove_container(name)

        if(self.is_running):
            worker = self._get_worker_by_datacenter(datacenter)
            worker.net.remove_link(name, datacenter.switch)
            worker.net.remove_docker(name)


    def start(self):
        for worker in self.workers.values():
            worker.start(self.controller_ip, self.controller_port)
        self.is_running = True

    def stop(self):
        for worker in self.workers.values():
            if(worker.is_running):
                worker.stop()
        self.is_running = False
