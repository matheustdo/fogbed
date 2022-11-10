import json
import time
from urllib.request import urlopen

url = "http://localhost:8181/cxf/iot-service/devices/"
sample_rate = 500 # publish_time = 2000
experiment_duration = 10000

# Calculate current time in milliseconds
def current_time():
  return int(time.time() * 1000)

# Avoid a soft-iot first 
try:
  urlopen(url)
except:
  pass

# Gets all devices names
response = urlopen(url)
devices_json = json.loads(response.read())
device_name_list = []
experiment_start_time = current_time()

for device in devices_json:
  device_name_list.append(device["id"])

sample_number = 0
experiment_current_time = current_time() - experiment_start_time
results = []

# Experiment
while experiment_current_time < experiment_duration:
  if (int(experiment_current_time / sample_rate) - sample_number >= 0):
    # Gets all devices data and append to results list
    sample = []
    
    for device_name in device_name_list:
      device_url = url + device_name + "/temperatureSensor"
      response = urlopen(device_url)
      device_json = json.loads(response.read())
      device = { "id": device_name, 
                 "value": device_json["value"], 
                 "startTime": device_json["startTime"],
                 "dataTime": device_json["startTime"] - experiment_start_time }
      print(device)
      sample.append(device)

    results.append(sample)
    sample_number += 1

  experiment_current_time = current_time() - experiment_start_time
