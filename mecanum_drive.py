
import RPi.GPIO as GPIO

"""
import mecanum_drive as md

dv = md.MecanumDrive("Test")
"""


class MecanumDrive:
    def __init__(self, name, pin0=7, pin1=11, pin2=13, pin3=15, pin4=16, pin5=18, pin6=22, pin7=36):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self._pin0 = pin0
        self._pin1 = pin1
        self._pin2 = pin2
        self._pin3 = pin3
        self._pin4 = pin4
        self._pin5 = pin5
        self._pin6 = pin6
        self._pin7 = pin7
        GPIO.setup(self._pin0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin4, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin5, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin6, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin7, GPIO.OUT, initial=GPIO.LOW)

    def stop(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"

    def forward(self):
        GPIO.output(self._pin0, GPIO.HIGH)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.HIGH)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.HIGH)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.HIGH)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"

    def backward(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.HIGH)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.HIGH)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.HIGH)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.HIGH)
        return "OK"

    def right(self):
        GPIO.output(self._pin0, GPIO.HIGH)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.HIGH)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.HIGH)
        GPIO.output(self._pin6, GPIO.HIGH)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"

    def left(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.HIGH)
        GPIO.output(self._pin2, GPIO.HIGH)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.HIGH)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.HIGH)
        return "OK"

    def right_forward(self):
        GPIO.output(self._pin0, GPIO.HIGH)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.HIGH)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"

    def left_forward(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.HIGH)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.HIGH)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"

    def left_backward(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.HIGH)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.HIGH)
        return "OK"

    def right_backward(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.HIGH)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.HIGH)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"


    def left_spin(self):
        GPIO.output(self._pin0, GPIO.HIGH)
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.HIGH)
        GPIO.output(self._pin4, GPIO.HIGH)
        GPIO.output(self._pin5, GPIO.LOW)
        GPIO.output(self._pin6, GPIO.LOW)
        GPIO.output(self._pin7, GPIO.HIGH)
        return "OK"

    def right_spin(self):
        GPIO.output(self._pin0, GPIO.LOW)
        GPIO.output(self._pin1, GPIO.HIGH)
        GPIO.output(self._pin2, GPIO.HIGH)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.LOW)
        GPIO.output(self._pin5, GPIO.HIGH)
        GPIO.output(self._pin6, GPIO.HIGH)
        GPIO.output(self._pin7, GPIO.LOW)
        return "OK"



