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

from mininet.log import setLogLevel

# setLogLevel('info')

url = "http://localhost:8181/cxf/iot-service/devices/"
min_sample_interval = 200 # publish_time = 2000
experiment_duration = 30000

def wait_url(url, verify):
  result = None 
  start_time = timeit.default_timer()
  
  while (result == None and timeit.default_timer() - start_time < 150):
    time.sleep(3)
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


def fot_sensors():
  Services(max_cpu=1, max_mem=4096)
  exp = FogbedExperiment()

  #cloud = exp.add_virtual_instance('cloud', CloudResourceModel(max_cu=2, max_mu=1024))
  fog = exp.add_virtual_instance('fog', FogResourceModel(max_cu=2, max_mu=1024))
  edge = exp.add_virtual_instance('edge', EdgeResourceModel(max_cu=2, max_mu=1024)) #, AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT))

  #gateway_cloud = Container('gate_cloud', resources=ResourceModel.XLARGE)
  gateway_fog = Container('gate_fog', resources=ResourceModel.XLARGE, dimage="gateway:publishing", environment={"COLLECT_TIME": "200","PUBLISH_TIME": "1000"}, port_bindings={1883:1883, 8181:8181, 1099:1099, 8101:8101, 61616:61616, 44444:44444})
  device_1 = Container('device_1', resources=ResourceModel.SMALL, dimage='device:latest', fail_model=AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT)) 
  device_2 = Container('device_2', resources=ResourceModel.SMALL, dimage='device:latest') 

  #exp.add_docker(gateway_cloud, cloud)
  exp.add_docker(gateway_fog, fog)
  exp.add_docker(device_1, edge)
  exp.add_docker(device_2, edge)

  #exp.add_link(cloud, fog)
  exp.add_link(fog, edge)

  fail_controller = FailController(exp)

  collect_return = -1

  try:
      exp.start()

      gateway_fog.cmd("./usr/local/bin/servicemix-init.sh &")
      gateway_fog.cmd("./opt/servicemix/bin/servicemix &")
      print("# Starting Servicemix")
      print(f"## Servicemix started in {round(wait_url(url, False), 1)}s")

      device_1.cmd(f"java -jar device.jar -di {device_1.name} &")
      print(f"# Starting {device_1.name}")
      print(f"## Device {device_1.name} started in " + str(round(wait_url(f"{url}{device_1.name}/temperatureSensor", True), 1)) + "s")

      device_2.cmd(f"java -jar device.jar -di {device_2.name} &")
      print(f"# Starting {device_2.name}")
      print(f"## Device {device_2.name} started in " + str(round(wait_url(f"{url}{device_2.name}/temperatureSensor", True), 1)) + "s")
      
      time.sleep(2)
      fail_controller.start()

      def is_sensor_active(device_name):
        # resp = gateway_fog.cmd(f"timeout 0.1 ping -c {exp.get_docker(device_name).ip}")
        # index = resp.find("[")
        # return index  > -1
        #resp = exp.get_docker(device_name).cmd(f"ifconfig eth0")
        #index = resp.find("UP")
        #return index > -1
        #return True
        return True

      print(f"# Starting collect")
      collect_return = sensor_collect(url, min_sample_interval, experiment_duration, is_sensor_active)
      # exp.start_cli()
  except Exception as e:
      print(e)
  finally:
      fail_controller.stop()
      exp.stop()

  return collect_return

print(fot_sensors())
# sudo service mosquitto stop ; sudo systemctl stop mosquitto.service