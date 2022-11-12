import csv
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches
import numpy as np

ficheiro = open('examples/results/result.csv', 'r')

x = []
x_active = []
y_device_1 = []
y_device_2 = []
y_device_3 = []
y_device_1_active = []
y_device_2_active = []
y_device_3_active = []

reader = csv.reader(ficheiro)

last_exp_number = 1
last_device = "device_1"
x_aux = []
x_active_aux = []
y_aux_1 = []
y_aux_2 = []
y_aux_3 = []
y_aux_1_active = []
y_aux_2_active = []
y_aux_3_active = []

for linha in reader:
  exp_number = linha[0]
  
  if (exp_number != "expNumber"):
    exp_number = int(exp_number)
    device = linha[1]

    if (exp_number != last_exp_number):
      x.append(x_aux)
      x_active.append(x_active_aux)
      y_device_1.append(y_aux_1)
      y_device_2.append(y_aux_2)
      y_device_3.append(y_aux_3)
      y_device_1_active.append(y_aux_1_active)
      y_device_2_active.append(y_aux_2_active)
      y_device_3_active.append(y_aux_3_active)
      x_aux = []
      x_active_aux = []
      y_aux_1 = []
      y_aux_2 = []
      y_aux_3 = []
      y_aux_1_active = []
      y_aux_2_active = []
      y_aux_3_active = []
      last_exp_number = exp_number
      
    # Generate X
    if (device == "device_1"):
      x_aux.append(round(float(linha[2]), 5))
      x_active_aux.append(round(float(linha[4]), 5))
    
    # Generate Y
    if (device == "device_1"):
      y_aux_1.append(round(float(linha[3]), 4))
      y_aux_1_active.append(1 if linha[5] == "True" else 0)

    # Generate Y
    if (device == "device_2"):
      y_aux_2.append(round(float(linha[3]), 4))
      y_aux_2_active.append(1 if linha[5] == "True" else 0)

    # Generate Y
    if (device == "device_3"):
      y_aux_3.append(round(float(linha[3]), 4))
      y_aux_3_active.append(1 if linha[5] == "True" else 0)

x.append(x_aux)
x_active.append(x_active_aux)
y_device_1.append(y_aux_1)
y_device_2.append(y_aux_2)
y_device_3.append(y_aux_3)
y_device_1_active.append(y_aux_1_active)
y_device_2_active.append(y_aux_2_active)
y_device_3_active.append(y_aux_3_active)

# Create a subsample from original lists to normalize the x axis
min_len = min(map(len, x))
to_remove_list = []

for x_list in x:
  to_remove_list.append(random.sample(range(0, len(x_list)), len(x_list) - min_len))
  
for idx, to_remove in enumerate(to_remove_list):
  for to_remove_idx in to_remove:
    x[idx][to_remove_idx] = -1
    x_active[idx][to_remove_idx] = -1
    y_device_1[idx][to_remove_idx] = -1
    y_device_2[idx][to_remove_idx] = -1
    y_device_3[idx][to_remove_idx] = -1
    y_device_1_active[idx][to_remove_idx] = -1
    y_device_2_active[idx][to_remove_idx] = -1
    y_device_3_active[idx][to_remove_idx] = -1

for idx, to_remove in enumerate(to_remove_list):
  x[idx] = list(filter((-1).__ne__, x[idx]))
  x_active[idx] = list(filter((-1).__ne__, x_active[idx]))
  y_device_1[idx] = list(filter((-1).__ne__, y_device_1[idx]))
  y_device_2[idx] = list(filter((-1).__ne__, y_device_2[idx]))
  y_device_3[idx] = list(filter((-1).__ne__, y_device_3[idx]))
  y_device_1_active[idx] = list(filter((-1).__ne__, y_device_1_active[idx]))
  y_device_2_active[idx] = list(filter((-1).__ne__, y_device_2_active[idx]))
  y_device_3_active[idx] = list(filter((-1).__ne__, y_device_3_active[idx]))


# Calculate active avg
active_avg_1_aux = np.average(y_device_1_active, axis=0)
active_avg_2_aux = np.average(y_device_2_active, axis=0)
active_avg_3_aux = np.average(y_device_3_active, axis=0)
y_device_1_active_avg = active_avg_1_aux
y_device_2_active_avg = active_avg_2_aux
y_device_3_active_avg = active_avg_3_aux

'''
def avg_active(array, aux):
  for idx, value in enumerate(aux):
    if (len(aux) > idx + 1):
      if (value < aux[idx + 1]):
        if (value > 0.5):
          array.append(1)
        else:
          array.append(0)
      else: 
        if (aux[idx + 1] > 0.5):
          array.append(1)
        else:
          array.append(0)
    elif (value > 0.5):
      array.append(1)
    else:
      array.append(0)
'''
      

# Get avgs
x_avg = np.average(x, axis=0)
x_active_avg = np.average(x_active, axis=0)
y_device_1_avg = np.average(y_device_1, axis=0)
y_device_2_avg = np.average(y_device_2, axis=0)
y_device_3_avg = np.average(y_device_3, axis=0)

x_avg = x_avg
x_active_avg = x_active_avg
y_device_1_avg = y_device_1_avg
y_device_2_avg = y_device_2_avg
y_device_3_avg = y_device_3_avg

fig, axs = plt.subplots(8, gridspec_kw={'height_ratios': [3, 0.3, 1, 3, 0.3, 1, 3, 0.3]})
fig.subplots_adjust(left= 0.1,
                    right= 0.9,
                    top= 0.9,
                    bottom= 0.1,
                    hspace=0.4)
green_color = (0, 0.58, 0.31, 1)
red_color = (1.0, 0.47, 0.42)
x_slim_size = (0, 60)
y_slim_size = (0, 15)

axs[0].set_title("Dispositivo 1 (Disponibilidade 100%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[0].plot(x_avg, y_device_1_avg)
axs[0].set_xlim(x_slim_size)
axs[0].set_ylim(y_slim_size[0], 1.25)
axs[0].set_ylabel("Tempo sem enviar dados (s)")
axs[1].plot(x_active_avg, y_device_1_active_avg, color=(green_color))
axs[1].set_facecolor(green_color)
axs[1].get_yaxis().set_visible(False)
axs[1].set_xlim(x_slim_size)
axs[1].set_xlabel("Tempo corrido de experimento (s)")

axs[2].set_visible(False)
plt.figure()
axs[3].set_title("Dispositivo 2 (Disponibilidade 50%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[3].plot(x_avg, y_device_2_avg)
axs[3].set_xlim(x_slim_size)
axs[3].set_ylim(y_slim_size[0], 5)
axs[3].set_ylabel("Tempo sem enviar dados (s)")
axs[4].stackplot(x_active_avg, y_device_2_active_avg, color=(green_color))
axs[4].set_facecolor(red_color)
axs[4].get_yaxis().set_visible(False)
axs[4].set_xlim(x_slim_size)
axs[4].set_xlabel("Tempo corrido de experimento (s)")

axs[5].set_visible(False)

axs[6].set_title("Dispositivo 3 (Disponibilidade 20%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[6].plot(x_avg, y_device_3_avg)
axs[6].set_xlim(x_slim_size)
axs[6].set_ylim(y_slim_size[0], 16)
axs[6].set_ylabel("Tempo sem enviar dados (s)")
axs[7].stackplot(x_active_avg, y_device_3_active_avg, color=(green_color))
axs[7].set_facecolor(red_color)
axs[7].get_yaxis().set_visible(False)
axs[7].set_xlim(x_slim_size)
axs[7].set_xlabel("Tempo corrido de experimento (s)")
red_patch = mpatches.Patch(color=red_color, label='Dispositivo desconectado')
green_patch = mpatches.Patch(color=green_color, label='Dispositivo conectado')
axs[7].legend(handles=[red_patch, green_patch], bbox_to_anchor=(1, -2), loc='upper right', borderaxespad=0.)

plt.show()