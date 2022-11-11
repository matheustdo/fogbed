import json
import time
import csv
from urllib.request import urlopen
import timeit

# Calculate current time in milliseconds
def current_time():
  return timeit.default_timer() * 1000

def sensor_collect(url, experiment_duration, is_sensor_active, exp_number):
  response = urlopen(url)
  devices_json = json.loads(response.read())
  device_name_list = []
  experiment_start_time = timeit.default_timer() * 1000
  experiment_start_timestamp = time.time() * 1000

  for device in devices_json:
    if device["id"] not in device_name_list:
      device_name_list.append(device["id"])
      
  experiment_current_time = current_time() - experiment_start_time
  results = []
  # sleep_duration = min_sample_interval / 1000
  start_time = timeit.default_timer()
  
  # Experiment
  while experiment_current_time < experiment_duration and timeit.default_timer() - start_time < 150:
    # time.sleep(sleep_duration)
    sample = []
    
    for device_name in device_name_list:
      device_url = url + device_name + "/temperatureSensor"
      response = urlopen(device_url)
      actived = is_sensor_active(device_name)
      device_json = json.loads(response.read())
      device = { "id": device_name, 
                  "value": device_json["value"], 
                  "startTime": device_json["startTime"],
                  "expStart": experiment_current_time,
                  "actived": actived }

      sample.append(device)

    results.append(sample)
    experiment_current_time = current_time() - experiment_start_time
    
  min = 0

  for result in results:
    for device in result:
      calc = device["expStart"] / 1000 - (device["startTime"] - experiment_start_timestamp) / 1000
      if calc < min:
        min = calc
        
  min = abs(min)

  if (exp_number == 1):
    with open('./examples/experiments/result.csv', 'w') as csvfile: 
      csv.writer(csvfile, delimiter=',').writerow(["expNumber", "id", "expStart", "lastUpdate", "actived"])
      
      for name in device_name_list:
        for result in results:
          for device in result:
            if name == device["id"]:
              csv.writer(csvfile, delimiter=',').writerow([exp_number, 
                device["id"], 
                "%.4f" % (device["expStart"] / 1000),
                "%.4f" % ((device["expStart"] / 1000 - (device["startTime"] - experiment_start_timestamp) / 1000) + min),
                device["actived"]])
              break
  else:
    with open('./examples/experiments/result.csv', 'a+') as csvfile: 
      for name in device_name_list:
        for result in results:
          for device in result:
            if name == device["id"]:
              csv.writer(csvfile, delimiter=',').writerow([exp_number, 
                device["id"], 
                "%.4f" % (device["expStart"] / 1000),
                "%.4f" % ((device["expStart"] / 1000 - (device["startTime"] - experiment_start_timestamp) / 1000) + min),
                device["actived"]])
              break
