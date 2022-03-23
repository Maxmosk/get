import RPi.GPIO as GPIO


def decimal2binary(value):
    assert (value <= 255 and value >= 0)
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


dac = [26, 19, 13, 6, 5, 11, 9, 10]


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dac, GPIO.OUT)

    while True:
        n = int(input("Please, enter number from 0 to 255: "))
        GPIO.output(dac, decimal2binary(n))
        print(5 * n / 256)
finally:
    GPIO.output(dac, [0] * 8)
    GPIO.cleanup()
