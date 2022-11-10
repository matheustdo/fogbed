from fogbed.emulation import Services
from fogbed.experiment.local import FogbedExperiment
from fogbed.fails.controller import FailController
from fogbed.node.container import Container
from fogbed.resources import ResourceModel
from fogbed.resources.models import CloudResourceModel, EdgeResourceModel, FogResourceModel
from fogbed.fails.models.availability import AvailabilityFail, AvailabilityMode
import time

from mininet.log import setLogLevel

# setLogLevel('info')

Services(max_cpu=1, max_mem=4096)
exp = FogbedExperiment()

cloud = exp.add_virtual_instance('cloud', CloudResourceModel(max_cu=2, max_mu=1024))
fog = exp.add_virtual_instance('fog', FogResourceModel(max_cu=2, max_mu=1024))
edge = exp.add_virtual_instance('edge', EdgeResourceModel(max_cu=2, max_mu=1024)) #, AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT))

gateway_cloud = Container('gate_cloud', resources=ResourceModel.XLARGE)
gateway_fog = Container('gate_fog', resources=ResourceModel.XLARGE, dimage="gateway:publishing", environment={"COLLECT_TIME": "200","PUBLISH_TIME": "2000"}, port_bindings={1883:1883, 8181:8181, 1099:1099, 8101:8101, 61616:61616, 44444:44444})
device_1 = Container('device_1', resources=ResourceModel.SMALL, dimage='device:latest', fail_model=AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT)) 
device_2 = Container('device_2', resources=ResourceModel.SMALL, dimage='device:latest') 

exp.add_docker(gateway_cloud, cloud)
exp.add_docker(gateway_fog, fog)
exp.add_docker(device_1, edge)
exp.add_docker(device_2, edge)

exp.add_link(cloud, fog)
exp.add_link(fog, edge)

fail_controller = FailController(exp)

try:
    exp.start()
    #  gateway_fog.cmd("./usr/local/bin/servicemix-init.sh &")
    #  gateway_fog.cmd("./opt/servicemix/bin/servicemix &")
    #time.sleep(100) # Time to start servicemix
    #  device_1.cmd("java -jar device.jar -di device_1 &")
    #time.sleep(10) # Time to start devices
    #  device_2.cmd("java -jar device.jar -di device_2 &")
    # Time to start devices
    # time.sleep(10)
    fail_controller.start()
    resp = gateway_fog.cmd("timeout 0.1 ping -c 1 -D " + device_1.ip)
    index = resp.find("[")
    if(index  > -1):
      te = resp[index + 1:resp.find("]")]
      print(te)
    time.sleep(2)
    resp1 = gateway_fog.cmd("timeout 0.1 ping -c 1 -D " + device_1.ip)
    if(resp1.find("[") > -1):
      te = resp1[index + 1:resp1.find("]")]
      print(te)
    
    # exp.start_cli()
finally:
    fail_controller.stop()
    exp.stop()