import numpy as np
import show


size = 1000

x = np.linspace(0, size, size)
y = np.random.normal(0, 1, size)

show.my_plot(x, y)

