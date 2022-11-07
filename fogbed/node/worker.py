from typing import Dict, List

from clusternet.client.worker import RemoteWorker
from fogbed.exceptions import VirtualInstanceAlreadyExists, VirtualInstanceNotFound
from fogbed.experiment.link import Link
from fogbed.node.instance import VirtualInstance
from fogbed.node.services.remote_docker import RemoteDocker


def get_tunnel_command(port: str, interface: str, ip: str) -> str:
    return f'ovs-vsctl add-port {port} {port}-{interface} -- set interface {port}-{interface} type=gre options:remote_ip={ip}'

class FogWorker:
    def __init__(self, ip: str) -> None:
        # Validate IP
        self.ip = ip
        self.datacenters: Dict[str, VirtualInstance] = {}
        self.tunnels: List[str] = []
        self.links: List[Link] = []
        self.net = RemoteWorker(ip)
        

    def add(self, datacenter: VirtualInstance, reachable: bool = False):
        if(datacenter.switch in self.datacenters):
            raise VirtualInstanceAlreadyExists(f'Datacenter {datacenter.label} already exists.')
        
        datacenter.set_ip(self.ip)
        datacenter.set_reachable(reachable)
        self.datacenters[datacenter.switch] = datacenter


    def add_link(self, node1: VirtualInstance, node2: VirtualInstance, **params):
        if(not node1.switch in self.datacenters):
            raise VirtualInstanceNotFound(node1.label)
        if(not node2.switch in self.datacenters):
            raise VirtualInstanceNotFound(node2.label)
        self.links.append(Link(node1.switch, node2.switch, **params))


    def add_tunnel(self, destination_ip: str):
        if(destination_ip == self.ip):
            raise Exception('Tunnel loops are not allowed')
        if(destination_ip in self.tunnels):
            raise Exception(f'Already exist a tunnel to worker with ip={destination_ip}')
        self.tunnels.append(destination_ip)
    

    def _create_topology(self):
        for datacenter in self.datacenters.values():
            self.net.add_switch(datacenter.switch)

            for container in datacenter:
                self.net.add_docker(container.name, **container.params)
                self.net.add_link(container.name, datacenter.switch)
                service = RemoteDocker(container.name, self.net.url)
                container.set_docker(service)

        for link in self.links:
            self.net.add_link(**link.to_dict)


    def _get_valid_switchname(self) -> str:
        switches = list(self.datacenters.keys())
        switches.sort()
        last_switch_index = int(switches[-1][1:])
        return f's{last_switch_index + 1}'
    

    def _create_links_to_gateway(self, gateway: str):
        self.net.add_switch(gateway)

        for datacenter in self.datacenters.values():
            if(datacenter.is_reachable):
                self.net.add_link(datacenter.switch, gateway)
    

    def _create_tunnels(self, gateway: str):
        for index, ip in enumerate(self.tunnels):
            command = get_tunnel_command(port=gateway, interface=f'gre{index+1}', ip=ip)
            self.net.run_command(gateway, command)

    @property
    def is_running(self) -> bool:
        return self.net.is_running

    def start(self, controller_ip: str, controller_port: int):
        if(not self.datacenters):
            raise Exception('Expect at least 1 VirtualInstance')

        self.net.add_controller('c0', controller_ip, controller_port)
        self._create_topology()
        
        gateway = self._get_valid_switchname()
        self._create_links_to_gateway(gateway)
        self.net.start()
        self._create_tunnels(gateway)
    
    def stop(self):
        self.net.stop()
