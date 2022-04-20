#!/bin/python3
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
from datetime import datetime


# SETUP
#####################
GPIO.setmode (GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setup(dac, GPIO.OUT)
comp = 4
GPIO.setup(comp, GPIO.IN)
troyka = 17
GPIO.setup(troyka, GPIO.OUT, initial = 0)
leds = [21, 20, 16, 12, 7, 8, 25, 24][::-1]
GPIO.setup(leds, GPIO.OUT)
#####################


#####################
def decimal2binary(value):
    assert value <= 255 and value >= 0
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def adc():
    n = 0
    for i in range(7, -1, -1):
        n += 2**i
        GPIO.output(dac, decimal2binary(n))
        time.sleep(0.01)
        if GPIO.input(comp) == 0:
            n -= 2**i
    return n


def set_volume(val):
    val += 14
    bright = val*8//256
    GPIO.output(leds[:bright], 1)
    GPIO.output(leds[bright:], 0)
#####################


values = []
highest = 0.97
lowest = 0.02


# MAIN
#####################
try:
    start_time = time.time()
    GPIO.output(troyka, 1)

    # CHARGE
    #####################
    while True:
        n = adc()
        set_volume(n)
        values.append(n)
        print(f"n={n}    V={n*3.3/256}", end='\r')
        if n >= highest * 255:
            break

    highest_time = time.time() - start_time
    print(f"First part ended after {highest_time}")
    #####################

    # DISCHARGE
    #####################
    GPIO.output(troyka, 0)
    while True:
        n = adc()
        set_volume(n)
        values.append(n)
        print(f"n={n}    V={n*3.3/256}", end='\r')
        if n <= lowest * 255:
            break

    lowest_time = time.time() - start_time
    print(f"Second part ended after {lowest_time}")
    #####################

    # DATA OUTPUT
    #####################
    date = datetime.now().strftime('%y.%m.%d-%H.%M.%S')
    with open(f"data-{date}.txt", 'w') as f:
        f.write('\n'.join(str(i) for i in values))

    with open(f"settings-{date}.txt", 'w') as f:
        f.write(f"Average frequency: {lowest_time/len(values)} s \nDiscretization is {3.3/256} V\n")

    print(
        f"Experiment lasted: {lowest_time} s", 
        f"Average time of measurement: {lowest_time/2} s", 
        f"Average frequency: {lowest_time/len(values)} s", 
        f"Discretization is {3.3/256} V", 
        sep='\n'
        )
    #####################

    # PLOT
    #####################
    plt.plot(values)
    plt.show()
    #####################
finally:
    # CLEANUP
    #####################
    GPIO.output(dac, 0)
    GPIO.cleanup()
    #####################
#####################

