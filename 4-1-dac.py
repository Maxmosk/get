import RPi.GPIO as GPIO


def decimal2binary(value):
    assert value <= 255 and value >= 0
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


dac = [26, 19, 13, 6, 5, 11, 9, 10]


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dac, GPIO.OUT)

    while True:
        in_str = input("Please, enter number from 0 to 255: ")

        assert in_str != "q"

        if not in_str.isnumeric():
            print("It isn't incorrect value!")
            continue

        n = int(in_str)
        if n > 255 or n < 0:
            print("Value in out of range!")
            continue

        GPIO.output(dac, decimal2binary(n))
        print(3.3 * n / 256)
except AssertionError:
    pass
finally:
    GPIO.output(dac, [0] * 8)
    GPIO.cleanup()
