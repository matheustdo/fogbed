import json
import time
import csv
from urllib.request import urlopen


def sensor_collect(url, min_sample_interval, experiment_duration, is_sensor_active):
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
  sleep_duration = min_sample_interval / 1000

  try:
    # Experiment
    while experiment_current_time < experiment_duration:
      # Gets all devices data and append to results list
      time.sleep(sleep_duration)
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
  except:
    return -1

  min = 1000

  test = "b"

  for result in results:
    for device in result:
      calc = device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000
      if calc < min:
        min = calc

  for result in results:
    for device in result:
      calc = device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000
      if calc == min:
        test = device
        
  min = abs(min)
  print("min  " + str(min))
  print("startTime  " + str(test["startTime"]))
  print("experiment_start_time  " + str(experiment_start_time))
  print("startTime - experiment_start_time  " + str(test["startTime"] - experiment_start_time))
  print("startTime / 1000  " + str(test["startTime"] / 1000))
  print("calc  " + str(test["expStart"] / 1000 - (test["startTime"] - experiment_start_time) / 1000))
  


  with open('./examples/experiments/result.csv', 'w') as csvfile:
    csv.writer(csvfile, delimiter=',').writerow(["id", "expStart", "lastUpdate", "actived"])
    
    for name in device_name_list:
      for result in results:
        for device in result:
          if name == device["id"]:
            csv.writer(csvfile, delimiter=',').writerow([device["id"], 
              device["expStart"] / 1000,
              (device["expStart"] / 1000 - (device["startTime"] - experiment_start_time) / 1000) + min,
              device["actived"]])
            break
  
  return 0
