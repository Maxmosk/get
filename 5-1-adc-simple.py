#!/bin/python3
import RPi.GPIO as GPIO
import time


def decimal2binary(value):
    assert value <= 255 and value >= 0
    return [int(bit) for bit in bin(value)[2:].zfill(8)]



def adc():
    for i in range(256):
        GPIO.output(dac, decimal2binary(i))
        time.sleep(0.006)
        if GPIO.input(comp) == 0:
            return i



dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dac, GPIO.OUT)
    GPIO.setup(comp, GPIO.IN)
    GPIO.setup(troyka, GPIO.OUT)

    GPIO.output(troyka, GPIO.LOW)
    while True:
        n = adc()
        print(f"Number: {n}\nVoltage: {3.3*n/256}")

finally:
    GPIO.output(dac, [GPIO.LOW] * 8)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()
