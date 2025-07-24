import RPi.GPIO as GPIO
from time import sleep

servo = 18
frequency = 50

angle_0 = 2.5 / 20 * 100
angle_45 = 2.0 / 20 * 100
angle_90 = 1.5 / 20 * 100
angle_135 = 1.0 / 20 * 100
angle_180 = 0.5 / 20 * 100

GPIO.setmode(GPIO.BCM)
print("set mode...")
GPIO.setwarnings(False)
GPIO.setup(servo, GPIO.OUT)

pwm = GPIO.PWM(servo, frequency)
print("set pwm...")

pwm.start(angle_0)
print("set pwm angle 0...")
sleep(1)
pwm.ChangeDutyCycle(angle_45)
print("set pwm angle 45...")
sleep(1)
sleep(1)
pwm.ChangeDutyCycle(angle_90)
print("set pwm angle 90...")
sleep(1)
pwm.ChangeDutyCycle(angle_135)
print("set pwm angle 135...")
sleep(1)
pwm.ChangeDutyCycle(angle_180)
print("set pwm angle 180...")
sleep(1)
pwm.ChangeDutyCycle(angle_0)
print("set pwm angle 0...")
sleep(1)

for x in range(0, 10):
    if(x % 2):
        rr = range(5, 26)
    else:
        rr = range(25, 4, -1)
    for i in rr:
        angle = (i / 10)/ 20 * 100
        pwm.ChangeDutyCycle(angle)
        print("set pwm angle {}...".format(angle))
        sleep(0.1)
sleep(1)
pwm.ChangeDutyCycle(angle_0)
sleep(1)

angles = [angle_0, angle_45, angle_90, angle_135, angle_180, angle_135, angle_90, angle_45, angle_0]

for i in range(0, 100):
    for angle in angles:
        pwm.ChangeDutyCycle(angle)
        sleep(0.1)



pwm.stop()
GPIO.cleanup()
