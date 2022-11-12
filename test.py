from fogbed.emulation import Services
from fogbed.experiment.local import FogbedExperiment
from fogbed.fails.controller import FailController
from fogbed.node.container import Container
from fogbed.resources import ResourceModel
from fogbed.resources.models import CloudResourceModel, EdgeResourceModel, FogResourceModel
from fogbed.fails.models.availability import AvailabilityFail, AvailabilityMode
import time
import timeit
from collector import sensor_collect
from urllib.request import urlopen
import json
import sys

from mininet.log import setLogLevel

# setLogLevel('info')

url = "http://localhost:8181/cxf/iot-service/devices/"

exp_number = int(sys.argv[1])
min_sample_interval = int(sys.argv[2])
experiment_duration = int(sys.argv[3])

def wait_url(url, verify, timeout):
  result = None 
  start_time = timeit.default_timer()
  
  while (result == None):
    if (timeit.default_timer() - start_time > timeout):
      raise Exception("url timeout")

    time.sleep(2)

    try:
      result = urlopen(url)
      if (verify):
        try:
          resp = json.load(result)
          if ("device" not in resp):
            result = None
        except:
          result = None
    except: 
      pass
    
  return timeit.default_timer() - start_time


def init_gateway(gateway):
  started = False
  attempt = 0
  total_time = 0
  timeout = 80
  print("# Starting Servicemix")

  while (not started and attempt < 2):
    attempt += 1
    
    try:
      gateway.cmd("./usr/local/bin/servicemix-init.sh &")
      gateway.cmd("./opt/servicemix/bin/servicemix &")
      total_time += round(wait_url(url, False, timeout), 1)
      print(f"## Servicemix started in {total_time}s in {attempt} attempt(s)")
      started = True
    except:
      total_time += timeout

  if (not started):
    raise Exception("url timeout")


def init_device(device):
  started = False
  attempt = 0
  total_time = 0
  timeout = 15
  print(f"# Starting {device.name}")

  while (not started and attempt < 3):
    attempt += 1
    
    try:
      device.cmd(f"java -jar device.jar -di {device.name} &")
      total_time += round(wait_url(f"{url}{device.name}/temperatureSensor", True, timeout), 1)
      print(f"## Device {device.name} started in {total_time}s in {attempt} attempt(s)")
      started = True
    except:
      total_time += timeout

  if (not started):
    raise Exception("url timeout")
  
Services(max_cpu=6, max_mem=4096)
exp = FogbedExperiment()

#cloud = exp.add_virtual_instance('cloud', CloudResourceModel(max_cu=2, max_mu=1024))
fog = exp.add_virtual_instance(f'fog', FogResourceModel(max_cu=16, max_mu=1024))
edge = exp.add_virtual_instance(f'edge', EdgeResourceModel(max_cu=3, max_mu=1024)) #, AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT))

#gateway_cloud = Container('gate_cloud', resources=ResourceModel.XLARGE)
gateway_fog = Container(f'gate_fog', resources=ResourceModel.XLARGE, dimage="matheustdo/gateway:publishing", environment={"COLLECT_TIME": "100","PUBLISH_TIME": "1000"}, port_bindings={1883:1883, 8181:8181, 1099:1099, 8101:8101, 61616:61616, 44444:44444})
device_1 = Container(f'device_1', resources=ResourceModel.SMALL, dimage='matheustdo/device:latest') 
device_2 = Container(f'device_2', resources=ResourceModel.SMALL, dimage='matheustdo/device:latest', fail_model=AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT)) 
device_3 = Container(f'device_3', resources=ResourceModel.SMALL, dimage='matheustdo/device:latest', fail_model=AvailabilityFail(availability=0.2, slot_time=3, availability_mode=AvailabilityMode.DISCONNECT)) 


#exp.add_docker(gateway_cloud, cloud)
exp.add_docker(gateway_fog, fog)
exp.add_docker(device_1, edge)
exp.add_docker(device_2, edge)
exp.add_docker(device_3, edge)

#exp.add_link(cloud, fog)
exp.add_link(fog, edge)

fail_controller = FailController(exp)

collect_return = 1

try:
    exp.start()
    init_gateway(gateway_fog)
    init_device(device_1)
    init_device(device_2)
    init_device(device_3)
    
    time.sleep(2)
    fail_controller.start()

    def is_sensor_active(device_name):
      resp = gateway_fog.cmd(f"timeout {min_sample_interval / 1000} ping {exp.get_docker(device_name).ip}")
      index = resp.find("64 bytes")
      return index  > -1

    print(f"# Starting collect")
    sensor_collect(url, experiment_duration, is_sensor_active, exp_number)
    print(f"## Collect completed")
    collect_return = 0
except Exception as e:
    print(e)
    
fail_controller.stop()
exp.stop()

exit(collect_return)

# sudo service mosquitto stop ; sudo systemctl stop mosquitto.service