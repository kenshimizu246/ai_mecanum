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

hpwm = GPIO.PWM(servo0, frequency)
print("set hpwm...")
vpwm = GPIO.PWM(servo1, frequency)
print("set vpwm...")

vpwm.start(angle_45)
hpwm.start(angle_90)
sleep(1)

# Center
vpwm.ChangeDutyCycle(angle_45)
hpwm.ChangeDutyCycle(angle_90)
sleep(1)

# Left Forward
vpwm.ChangeDutyCycle(angle_45)
hpwm.ChangeDutyCycle(angle_135)
sleep(1)

# Right Forward
vpwm.ChangeDutyCycle(angle_45)
hpwm.ChangeDutyCycle(angle_45)
sleep(1)

# Center
vpwm.ChangeDutyCycle(angle_45)
hpwm.ChangeDutyCycle(angle_90)
sleep(1)

# Left
vpwm.ChangeDutyCycle(angle_45)
hpwm.ChangeDutyCycle(angle_180)
sleep(1)

# Right
vpwm.ChangeDutyCycle(angle_45)
hpwm.ChangeDutyCycle(angle_0)
sleep(1)


for x in range(0, 10):
    if(x % 2):
        rr = range(5, 26)
    else:
        rr = range(25, 4, -1)
    for i in rr:
        angle = (i / 10)/ 20 * 100
        hpwm.ChangeDutyCycle(angle)
        print("set hpwm angle {}...".format(angle))
        sleep(0.1)
sleep(1)
hpwm.ChangeDutyCycle(angle_0)
sleep(1)

angles = [angle_0, angle_45, angle_90, angle_135, angle_180, angle_135, angle_90, angle_45, angle_0]

for i in range(0, 100):
    for angle in angles:
        hpwm.ChangeDutyCycle(angle)
        sleep(0.1)

hpwm = GPIO.PWM(servo0, frequency)
hpwm.start(angle_0)
hpwm.ChangeDutyCycle(angle_90)
hpwm.stop()


vpwm.stop()
hpwm.stop()
GPIO.cleanup()
