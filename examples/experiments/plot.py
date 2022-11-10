import csv
import matplotlib.pyplot as plt

ficheiro = open('result-module-min.csv', 'r')

x = []
y_1 = []
y_2 = []

reader = csv.reader(ficheiro)

for linha in reader:
  # Gets exp time
  if (linha[0] == "device_1"): 
    x.append(round(float(linha[1]), 1))

  # device_1
  if (linha[0] == "device_1"): 
    y_1.append(round(float(linha[3]), 4))
  # device_2
  elif (linha[0] == "device_2"): 
    y_2.append(round(float(linha[3]), 4))

print("device_1 average: " + str(sum(y_1) / len(y_1)) + "s")
print("device_2 average: " + str(sum(y_2) / len(y_2)) + "s")

plt.plot(x, y_1)
plt.plot(x, y_2)
plt.show()