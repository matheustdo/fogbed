import subprocess
import timeit

experiment_size = 30
exp_number = 1
min_sample_interval = 100 
experiment_duration = 60000

result = 1

start_time = timeit.default_timer()

while (exp_number <= experiment_size):
  print(f"- Experiment number {exp_number}")
  result = subprocess.run(["python3", "test.py", str(exp_number), str(min_sample_interval), str(experiment_duration)]).returncode
  
  while (result == 1):
    result = subprocess.run(["python3", "test.py", str(exp_number), str(min_sample_interval), str(experiment_duration)]).returncode

  exp_number += 1

end_time = timeit.default_timer()
print(f"- Experiment ended in {end_time - start_time}s")