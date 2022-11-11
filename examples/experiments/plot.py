import csv
import matplotlib.pyplot as plt

ficheiro = open('examples/experiments/result.csv', 'r')

x = []
y_1 = []
y_2 = []
y_3 = []
y_4 = []

reader = csv.reader(ficheiro)

for linha in reader:
  # Gets exp time
  if (linha[1] == "device_1"): 
    x.append(round(float(linha[2]), 1))

  # device_1
  if (linha[1] == "device_1"): 
    y_1.append(round(float(linha[3]), 4))
    y_3.append(1 if linha[4] == "True" else 0)
  # device_2
  elif (linha[1] == "device_2"): 
    y_2.append(round(float(linha[3]), 4))
    y_4.append(0.5 if linha[4] == "True" else 0)

print("device_1 average: " + str(sum(y_1) / len(y_1)) + "s")
print("device_2 average: " + str(sum(y_2) / len(y_2)) + "s")

plt.plot(x, y_1)
plt.plot(x, y_2)
plt.plot(x, y_3)
plt.plot(x, y_4)
plt.show()