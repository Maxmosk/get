#!/bin/python3
import matplotlib.pyplot as plt
import numpy as np


v_data = np.loadtxt("data-22.04.20-17.13.54.txt")

with open("settings-22.04.20-17.13.54.txt") as sets:
    set_inp = sets.readlines()

t_step = float(set_inp[0].split(" ")[2])
v_step = float(set_inp[1].split(" ")[2])

v_data *= v_step

t_data = np.arange(0, (len(v_data) - 0.99) * t_step, t_step)

fig, ax = plt.subplots(figsize=(16,10), dpi=200)


ax.set_xlabel("time, sec")
ax.set_ylabel("voltage, vlt")
ax.set_title("Capacitor charging and discharging process in an RC circuit", wrap=True)

plt.text(0.8 * max(t_data), 0.8 * max(v_data), \
        f"Charge time: {v_data.argmax() * t_step :.2f} с \n\nDischarge time: {(max(t_data) - v_data.argmax() * t_step) :.2f} с", \
        size='large', wrap=True)


ax.minorticks_on()
ax.grid(True)
ax.grid(True, 'minor', ls=':')

ax.set_xlim(0, 1.1 * max(t_data))
ax.set_ylim(0, 1.1 * max(v_data))

stp=25
plt.plot(t_data, v_data, color = 'm', alpha = 0.5, label="V(t)")
ax.plot(t_data[::stp], v_data[::stp], 'bo')
ax.legend(fontsize = 'large')
fig.savefig("plot.svg", format="svg", dpi=200)
plt.show()
