import json
import time
import csv
from urllib.request import urlopen

url = "http://localhost:8181/cxf/iot-service/devices/"
min_sample_interval = 200 # publish_time = 2000
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

experiment_current_time = current_time() - experiment_start_time
results = []
samples = 0
sleep_duration = min_sample_interval / 1000

# Experiment
while experiment_current_time < experiment_duration:
  # Gets all devices data and append to results list
  time.sleep(sleep_duration)
  print(samples)
  sample = []
  
  for device_name in device_name_list:
    device_url = url + device_name + "/temperatureSensor"
    response = urlopen(device_url)
    device_json = json.loads(response.read())
    device = { "id": device_name, 
                "value": device_json["value"], 
                "startTime": device_json["startTime"],
                "expStart": experiment_current_time }

    sample.append(device)

  results.append(sample)
  experiment_current_time = current_time() - experiment_start_time
  samples += 1
print("lem: ")
print(len(results))
'''

with open('./examples/experiments/result.csv', 'w') as csvfile:
  csv.writer(csvfile, delimiter=',').writerow(["id", "expStart", "startTime" , "lastUpdate"])
  
  for name in device_name_list:
    for result in results:
      for device in result:
        if name == device["id"]:
          csv.writer(csvfile, delimiter=',').writerow([device["id"], 
            device["expStart"] / 1000,
            (device["startTime"] - experiment_start_time) / 1000, 
            (device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000)])
          break


with open('./examples/experiments/result-module.csv', 'w') as csvfile:
  csv.writer(csvfile, delimiter=',').writerow(["id", "expStart", "startTime" , "lastUpdate"])
  
  for name in device_name_list:
    for result in results:
      for device in result:
        if name == device["id"]:
          csv.writer(csvfile, delimiter=',').writerow([device["id"], 
            device["expStart"] / 1000,
            (device["startTime"] - experiment_start_time) / 1000, 
            abs(device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000)])
          break

min = 1000

for result in results:
  for device in result:
    calc = device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000
    if calc < min:
      min = calc
      
min = abs(min)

with open('./examples/experiments/result-module-min.csv', 'w') as csvfile:
  csv.writer(csvfile, delimiter=',').writerow(["id", "expStart", "startTime" , "lastUpdate"])
  
  for name in device_name_list:
    for result in results:
      for device in result:
        if name == device["id"]:
          csv.writer(csvfile, delimiter=',').writerow([device["id"], 
            device["expStart"] / 1000,
            (device["startTime"] - experiment_start_time) / 1000, 
            (device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000) + min])
          break

'''