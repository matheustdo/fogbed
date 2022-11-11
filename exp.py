import subprocess

experiment_size = 30
exp_number = 1
min_sample_interval = 100 
experiment_duration = 40000

result = 1

while (exp_number <= experiment_size):
  result = subprocess.run(["python3", "test.py", str(exp_number), str(min_sample_interval), str(experiment_duration)]).returncode
  
  while (result == 1):
    result = subprocess.run(["python3", "test.py", str(exp_number), str(min_sample_interval), str(experiment_duration)]).returncode

  exp_number += 1