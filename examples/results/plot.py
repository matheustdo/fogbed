import csv
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

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
random.seed(1)
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

# Charts lastPublish and actived X time

fig, axs = plt.subplots(8, gridspec_kw={'height_ratios': [3, 0.3, 1, 3, 0.3, 1, 3, 0.3]})
fig.subplots_adjust(left= 0.1,
                    right= 0.9,
                    top= 0.9,
                    bottom= 0.1,
                    hspace=0.2)
green_color = (0, 0.58, 0.31, 1)
red_color = (1.0, 0.47, 0.42)
x_slim_size = (0, 60)
y_slim_size = (0, 15)
fig.suptitle('Amostra única', fontsize=14)

axs[0].set_title("Dispositivo 1 (Disponibilidade 100%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[0].plot(x[1], y_device_1[1])
axs[0].set_xlim(x_slim_size)
axs[0].set_ylim(y_slim_size[0], 1.25)
axs[0].set_ylabel("Tempo sem enviar dados (s)")
axs[0].get_xaxis().set_visible(False)
axs[1].plot(x_active[1], y_device_1_active[1], color=(green_color))
axs[1].set_facecolor(green_color)
axs[1].get_yaxis().set_visible(False)
axs[1].set_xlim(x_slim_size)
axs[1].set_xlabel("Tempo corrido de experimento (s)")

axs[2].set_visible(False)
axs[3].set_title("Dispositivo 2 (Disponibilidade 50%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[3].plot(x[1], y_device_2[1])
axs[3].set_xlim(x_slim_size)
axs[3].set_ylim(y_slim_size[0], 5)
axs[3].set_ylabel("Tempo sem enviar dados (s)")
axs[3].get_xaxis().set_visible(False)
axs[4].step(x_active[1], y_device_2_active[1], color=(green_color))
axs[4].fill_between(x_active[1], y_device_2_active[1], step="pre", alpha=1, color=green_color)
axs[4].set_facecolor(red_color)
axs[4].get_yaxis().set_visible(False)
axs[4].set_xlim(x_slim_size)
axs[4].set_xlabel("Tempo corrido de experimento (s)")

axs[5].set_visible(False)

axs[6].set_title("Dispositivo 3 (Disponibilidade 20%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[6].plot(x[1], y_device_3[1])
axs[6].set_xlim(x_slim_size)
axs[6].set_ylim(y_slim_size[0], 16)
axs[6].set_ylabel("Tempo sem enviar dados (s)")
axs[6].get_xaxis().set_visible(False)
axs[7].step(x_active[1], y_device_3_active[1], color=(green_color))
axs[7].fill_between(x_active[1], y_device_3_active[1], step="pre", alpha=1, color=green_color)
axs[7].set_facecolor(red_color)
axs[7].get_yaxis().set_visible(False)
axs[7].set_xlim(x_slim_size)
axs[7].set_xlabel("Tempo corrido de experimento (s)")
red_patch = mpatches.Patch(color=red_color, label='Dispositivo desconectado')
green_patch = mpatches.Patch(color=green_color, label='Dispositivo conectado')
axs[7].legend(handles=[red_patch, green_patch], bbox_to_anchor=(1, -2), loc='upper right', borderaxespad=0.)


## Average lastPublish and actived X time

# Calculate active avg
active_avg_1_aux = np.average(y_device_1_active, axis=0)
active_avg_2_aux = np.average(y_device_2_active, axis=0)
active_avg_3_aux = np.average(y_device_3_active, axis=0)

y_device_1_active_avg = active_avg_1_aux
y_device_2_active_avg = active_avg_2_aux
y_device_3_active_avg = active_avg_3_aux

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
                    hspace=0.2)
green_color = (0, 0.58, 0.31, 1)
red_color = (1.0, 0.47, 0.42)
x_slim_size = (0, 60)
y_slim_size = (0, 15)
fig.suptitle('Média de 30 amostras', fontsize=14)

axs[0].set_title("Dispositivo 1 (Disponibilidade 100%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[0].plot(x_avg, y_device_1_avg)
axs[0].set_xlim(x_slim_size)
axs[0].set_ylim(y_slim_size[0], 1.25)
axs[0].set_ylabel("Tempo sem enviar dados (s)")
axs[0].get_xaxis().set_visible(False)
axs[1].plot(x_active_avg, y_device_1_active_avg, color=(green_color))
axs[1].set_facecolor(green_color)
axs[1].get_yaxis().set_visible(False)
axs[1].set_xlim(x_slim_size)
axs[1].set_xlabel("Tempo corrido de experimento (s)")

axs[2].set_visible(False)
axs[3].set_title("Dispositivo 2 (Disponibilidade 50%): Tempo desde que o dispositivo enviou os últimos dados para o gateway em comparação com sua conectividade")
axs[3].plot(x_avg, y_device_2_avg)
axs[3].set_xlim(x_slim_size)
axs[3].set_ylim(y_slim_size[0], 5)
axs[3].set_ylabel("Tempo sem enviar dados (s)")
axs[3].get_xaxis().set_visible(False)
axs[4].stackplot(x_active_avg, y_device_2_active_avg, color=(green_color))
#axs[4].fill_between(x_active_avg, y_device_2_active_avg, step="pre", alpha=1, color=green_color)
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
axs[6].get_xaxis().set_visible(False)
axs[7].stackplot(x_active_avg, y_device_3_active_avg, color=(green_color))
#axs[7].fill_between(x_active_avg, y_device_3_active_avg, step="pre", alpha=1, color=green_color)
axs[7].set_facecolor(red_color)
axs[7].get_yaxis().set_visible(False)
axs[7].set_xlim(x_slim_size)
axs[7].set_xlabel("Tempo corrido de experimento (s)")
red_patch = mpatches.Patch(color=red_color, label='Dispositivo desconectado')
green_patch = mpatches.Patch(color=green_color, label='Dispositivo conectado')
axs[7].legend(handles=[red_patch, green_patch], bbox_to_anchor=(1, -2), loc='upper right', borderaxespad=0.)

# Charts LastPublish and Actived X number of sent data


def calc_send_time(device_array):
  x_device_number = []
  y_device_send_time = []

  for y_idx, experiment in enumerate(device_array):
    last_value = -1
    last_trend = ""
    first_trend = ""
    peak = -1
    peak_time = -1
    experiment_aux = []
    
    for idx, value in enumerate(experiment):
      if (last_value == -1):
        last_value = value
        first_trend = "up" if value < experiment[idx + 1] else "down"
      elif (value > last_value): 
        if (first_trend == "down" and last_trend == "down"):
          peak = last_value
          if (peak > -1 and peak_time > -1):
            experiment_aux.append(round(x[y_idx][idx - 1] - peak_time, 5))

          peak_time = x[y_idx][idx - 1]

        last_trend = "up"
        last_value = value
      elif (value < last_value): 
        if (first_trend == "up" and last_trend == "up"):
          peak = last_value
          if (peak > -1 and peak_time > -1):
            experiment_aux.append(round(x[y_idx][idx - 1] - peak_time, 5))

          peak_time = x[y_idx][idx - 1]

        last_trend = "down"
        last_value = value
        
    x_device_number.append(list(range(1, len(experiment_aux) + 1)))
    y_device_send_time.append(experiment_aux)
  
  return x_device_number, y_device_send_time

x_device_1_number, y_device_1_send_time = calc_send_time(y_device_1)
x_device_2_number, y_device_2_send_time = calc_send_time(y_device_2)
x_device_3_number, y_device_3_send_time = calc_send_time(y_device_3)

# print(x[0])
# print(y_device_1[0])

def get_mean(device_send_time):
  df = pd.DataFrame(device_send_time, columns = ['number',])
  mean = df.expanding().mean()
  mean_y = list(map(lambda x: x[0], mean.values.tolist()))
  return mean_y
  
mean_y_1 = get_mean(y_device_1_send_time[1])
mean_y_2 = get_mean(y_device_2_send_time[1])
mean_y_3 = get_mean(y_device_3_send_time[1])

fig, axs = plt.subplots(3, gridspec_kw={'height_ratios': [3, 3, 3]})
fig.subplots_adjust(left= 0.1,
                    right= 0.9,
                    top= 0.9,
                    bottom= 0.1,
                    hspace=0.4)
fig.suptitle('Amostra única', fontsize=14)

single_average_1 = np.average(y_device_1_send_time[1])
single_average_2 = np.average(y_device_2_send_time[1])
single_average_3 = np.average(y_device_3_send_time[1])

print(f"(Sigle sample) Average of Device 1 (100%): {single_average_1}")
print(f"(Sigle sample) Average of Device 2 (50%): {single_average_2}")
print(f"(Sigle sample) Average of Device 3 (20%): {single_average_3}")

axs[0].set_title("Dispositivo 1 (Disponibilidade 100%): Tempo que o dispositivo leva para enviar dados")
axs[0].bar(x_device_1_number[1], y_device_1_send_time[1])
axs[0].plot(x_device_1_number[1], mean_y_1, color='tab:orange')
axs[0].set_ylim(0, 1.5)
axs[0].set_xlim(0.5, len(x_device_1_number[1]) + 0.5)
axs[0].set_ylabel("Tempo até enviar dado (s)")
axs[0].set_xlabel("Número do dado enviado (n)")
axs[0].text(0.99, 0.95, f'Tempo médio total: {round(single_average_1, 4)}s',
        verticalalignment='top', horizontalalignment='right',
        transform=axs[0].transAxes,
        fontsize=12)

axs[1].set_title("Dispositivo 2 (Disponibilidade 50%): Tempo que o dispositivo leva para enviar dados")
axs[1].bar(x_device_2_number[1], y_device_2_send_time[1])
axs[1].plot(x_device_2_number[1], mean_y_2, color='tab:orange')
axs[1].set_ylim(0, 5)
axs[1].set_xlim(0.5, len(x_device_2_number[1]) + 0.5)
axs[1].set_ylabel("Tempo até enviar dado (s)")
axs[1].set_xlabel("Número do dado enviado (n)")
axs[1].text(0.99, 0.95, f'Tempo médio total: {round(single_average_2, 4)}s',
        verticalalignment='top', horizontalalignment='right',
        transform=axs[1].transAxes,
        fontsize=12)

axs[2].set_title("Dispositivo 3 (Disponibilidade 20%): Tempo que o dispositivo leva para enviar dados")
axs[2].bar(x_device_3_number[1], y_device_3_send_time[1])
axs[2].plot(x_device_3_number[1], mean_y_3, color='tab:orange')
axs[2].set_ylim(0, 15)
axs[2].set_xlim(0.5, len(x_device_3_number[1]) + 0.5)
orange_patch = mpatches.Patch(color='tab:blue', label='Tempo médio de envio dos dados acumulado')
blue_patch = mpatches.Patch(color='tab:orange', label='Tempo de envio do dado')
axs[2].legend(handles=[blue_patch, orange_patch], bbox_to_anchor=(1, -0.15), loc='upper right', borderaxespad=0.)
axs[2].set_ylabel("Tempo até enviar dado (s)")
axs[2].set_xlabel("Número do dado enviado (n)")
axs[2].text(0.99, 0.95, f'Tempo médio total: {round(single_average_3, 4)}s',
        verticalalignment='top', horizontalalignment='right',
        transform=axs[2].transAxes,
        fontsize=12)

# Avg sent data all experiments

def array_simplifier(device_list):
  aux = []
  max_len = max(map(len, device_list))

  for value in device_list:
    aux.append(value.copy())

  for value_aux in aux:
    while (len(value_aux) < max_len):
      value_aux.append(np.average(value_aux))

  return aux


y_device_1_send_time_avg = np.average(array_simplifier(y_device_1_send_time), axis=0)
y_device_2_send_time_avg = np.average(array_simplifier(y_device_2_send_time), axis=0)
y_device_3_send_time_avg = np.average(array_simplifier(y_device_3_send_time), axis=0)

x_device_1_send_time_avg = list(range(1, len(y_device_1_send_time_avg) + 1))
x_device_2_send_time_avg = list(range(1, len(y_device_2_send_time_avg) + 1))
x_device_3_send_time_avg = list(range(1, len(y_device_3_send_time_avg) + 1))
mean_y_1_avg = get_mean(y_device_1_send_time_avg)
mean_y_2_avg = get_mean(y_device_2_send_time_avg)
mean_y_3_avg = get_mean(y_device_3_send_time_avg)

fig, axs = plt.subplots(3, gridspec_kw={'height_ratios': [3, 3, 3]})
fig.subplots_adjust(left= 0.1,
                    right= 0.9,
                    top= 0.9,
                    bottom= 0.1,
                    hspace=0.4)
fig.suptitle('Média de 30 amostras', fontsize=14)

total_average_1 = np.average(y_device_1_send_time_avg)
total_average_2 = np.average(y_device_2_send_time_avg)
total_average_3 = np.average(y_device_3_send_time_avg)

print(f"(30 exp. sample) Average of Device 1 (100%): {total_average_1}")
print(f"(30 exp. sample) Average of Device 2 (50%): {total_average_2}")
print(f"(30 exp. sample) Average of Device 3 (20%): {total_average_3}")

axs[0].set_title("Dispositivo 1 (Disponibilidade 100%): Tempo que o dispositivo leva para enviar dados")
axs[0].bar(x_device_1_send_time_avg, y_device_1_send_time_avg)
axs[0].plot(x_device_1_send_time_avg, mean_y_1_avg, color='tab:orange')
axs[0].set_ylim(0, 1.5)
axs[0].set_xlim(0.5, len(x_device_1_send_time_avg) + 0.5)
axs[0].set_ylabel("Tempo até enviar dado (s)")
axs[0].set_xlabel("Número do dado enviado (n)")
axs[0].text(0.99, 0.95, f'Tempo médio total: {round(total_average_1, 4)}s',
        verticalalignment='top', horizontalalignment='right',
        transform=axs[0].transAxes,
        fontsize=12)

axs[1].set_title("Dispositivo 2 (Disponibilidade 50%): Tempo que o dispositivo leva para enviar dados")
axs[1].bar(x_device_2_send_time_avg, y_device_2_send_time_avg)
axs[1].plot(x_device_2_send_time_avg, mean_y_2_avg, color='tab:orange')
axs[1].set_ylim(0, 5)
axs[1].set_xlim(0.5, len(x_device_2_send_time_avg) + 0.5)
axs[1].set_ylabel("Tempo até enviar dado (s)")
axs[1].set_xlabel("Número do dado enviado (n)")
axs[1].text(0.99, 0.95, f'Tempo médio total: {round(total_average_2, 4)}s',
        verticalalignment='top', horizontalalignment='right',
        transform=axs[1].transAxes,
        fontsize=12)

axs[2].set_title("Dispositivo 3 (Disponibilidade 20%): Tempo que o dispositivo leva para enviar dados")
axs[2].bar(x_device_3_send_time_avg, y_device_3_send_time_avg)
axs[2].plot(x_device_3_send_time_avg, mean_y_3_avg, color='tab:orange')
axs[2].set_ylim(0, 15)
axs[2].set_xlim(0.5, len(x_device_3_send_time_avg) + 0.5)
orange_patch = mpatches.Patch(color='tab:blue', label='Tempo médio de envio dos dados acumulado')
blue_patch = mpatches.Patch(color='tab:orange', label='Tempo de envio do dado')
axs[2].legend(handles=[blue_patch, orange_patch], bbox_to_anchor=(1, -0.15), loc='upper right', borderaxespad=0.)
axs[2].set_ylabel("Tempo até enviar dado (s)")
axs[2].set_xlabel("Número do dado enviado (n)")
axs[2].text(0.99, 0.95, f'Tempo médio total: {round(total_average_3, 4)}s',
        verticalalignment='top', horizontalalignment='right',
        transform=axs[2].transAxes,
        fontsize=12)

plt.show()