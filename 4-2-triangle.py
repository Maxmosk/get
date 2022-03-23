import RPi.GPIO as GPIO
import time


def decimal2binary(value):
    assert value <= 255 and value >= 0
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


dac = [26, 19, 13, 6, 5, 11, 9, 10]


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dac, GPIO.OUT)

    t = int(input("Enter period: ")) / 510

    while True:
        for i in range(256):
            GPIO.output(dac, decimal2binary(i))
            time.sleep(t)
        for i in range(255, 0, -1):
            GPIO.output(dac, decimal2binary(i))
            time.sleep(t)
finally:
    GPIO.output(dac, [0] * 8)
    GPIO.cleanup()
