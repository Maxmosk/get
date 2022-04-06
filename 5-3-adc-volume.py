#!/bin/python3
import RPi.GPIO as GPIO
import time


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



dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24][::-1]
comp = 4
troyka = 17

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dac + leds, GPIO.OUT)
    GPIO.setup(comp, GPIO.IN)
    GPIO.setup(troyka, GPIO.OUT)

    GPIO.output(troyka, GPIO.LOW)
    while True:
        n = adc()
        print(f"Number: {n}\nVoltage: {3.3*n/256}")
        n_bin = decimal2binary(n)
        GPIO.output(leds, [GPIO.LOW]*8)
        for i in range(7, -1, -1):
            GPIO.output(leds[i], GPIO.HIGH if n > 2**i else GPIO.LOW)

finally:
    GPIO.output(dac + leds, [GPIO.LOW] * 16)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()
