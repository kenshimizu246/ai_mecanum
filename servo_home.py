import RPi.GPIO as GPIO
from time import sleep

"""
12 PWM0 GPIO 1   BCM 18 
32 PWM0 GPIO 26  BCM 12
33 PWM1 GPIO 23  BCM 13
35 PWM1 GPIO 24  BCM 19
"""

servo0 = 13
servo1 = 18
frequency = 50

angle_0 = 2.5 / 20 * 100
angle_45 = 2.0 / 20 * 100
angle_90 = 1.5 / 20 * 100
angle_135 = 1.0 / 20 * 100
angle_180 = 0.5 / 20 * 100

GPIO.setmode(GPIO.BCM)
print("set mode...")
GPIO.setwarnings(False)
GPIO.setup(servo0, GPIO.OUT)
GPIO.setup(servo1, GPIO.OUT)

pwm0 = GPIO.PWM(servo0, frequency)
sleep(1)
pwm0.start(0)
print("set pwm0 angle 0...")
sleep(1)

pwm1 = GPIO.PWM(servo1, frequency)
sleep(1)
pwm1.start(0)
print("set pwm1 angle 0...")
sleep(1)

pwm0.ChangeDutyCycle(angle_90)
sleep(0.5)
pwm0.stop()
sleep(0.5)
pwm1.ChangeDutyCycle(angle_45)
sleep(0.5)
pwm1.stop()
sleep(0.5)
GPIO.cleanup()
