import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

gp_out = 2
GPIO.setup(gp_out, GPIO.OUT)
servo = GPIO.PWM(gp_out, 50)
servo.start(0.0)

try:
    while True:
        print("input Duty Cycle (2.5 - 12)")
        dc = float(input())

        servo.ChangeDutyCycle(dc)
        time.sleep(1)
        servo.ChangeDutyCycle(0.0)

except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()
