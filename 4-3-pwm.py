import RPi.GPIO as GPIO


pwm_pin = 2

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)

    p = GPIO.PWM(pwm_pin, 10000)
    p.start(0)

    while True:
        n = float(input("Enter duty cycle: "))
        print(3.3 * n / 100)
        p.ChangeDutyCycle(n)
finally:
    p.stop()
    GPIO.output(pwm_pin, GPIO.LOW)
    GPIO.cleanup()
    