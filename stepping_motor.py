
import RPi.GPIO as GPIO

class SteppingMotor:
    def __init__(self, pin0=31, pin1=33, pin2=35, pin3=37):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self._pin0 = pin0
        self._pin1 = pin1
        self._pin2 = pin2
        self._pin3 = pin3
        GPIO.setup(self._pin0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin3, GPIO.OUT, initial=GPIO.LOW)

    def right(self):


    def left(self):

import RPi.GPIO as GPIO
import time

pin0=29
pin1=31
pin2=33
pin3=35

# a = [[1,0,0,1], [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1]]
a = [[1,0,0,1],[0,1,0,1],[0,1,1,0],[1,0,1,0]]


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin0, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin3, GPIO.OUT, initial=GPIO.LOW)

for i in range(0, 100):
    for x in a:
        time.sleep(0.1)
        print(i)
        GPIO.output(pin0, x[0])
        GPIO.output(pin1, x[1])
        GPIO.output(pin2, x[2])
        GPIO.output(pin3, x[3])

GPIO.output(pin0, 0)
GPIO.output(pin1, 0)
GPIO.output(pin2, 0)
GPIO.output(pin3, 0)

def ss(i):
    GPIO.output(pin0, a[i][0])
    GPIO.output(pin1, a[i][1])
    GPIO.output(pin2, a[i][2])
    GPIO.output(pin3, a[i][3])

def off():
    GPIO.output(pin0, 0)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 0)

def drive(x):
    GPIO.output(pin0, x[0])
    GPIO.output(pin1, x[1])
    GPIO.output(pin2, x[2])
    GPIO.output(pin3, x[3])


try:
    for i in range(0, 100):
        for x in a:
            time.sleep(1)
            print(i)
            drive(x)
finally:
    off()












