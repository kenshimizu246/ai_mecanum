# -*- coding: utf-8 -*-
import time
import VL53L0X
import RPi.GPIO as GPIO

import event

VL53_1_XSHUT = 20
VL53_2_XSHUT = 21

class DistanceEvent(event.EventObject):
    def __init__(self, name, id, distance):
        self._name = name
        self._id = id
        self._distance = distance

    def get_name(self):
        return self._name

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(VL53_1_XSHUT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(VL53_2_XSHUT, GPIO.OUT, initial=GPIO.LOW)
time.sleep(0.5)

GPIO.output(VL53_1_XSHUT, GPIO.HIGH)
time.sleep(0.1)
sensor1 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
sensor1.change_address(0x2B)

GPIO.output(VL53_2_XSHUT, GPIO.HIGH)
time.sleep(0.1)
sensor2 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
sensor2.change_address(0x2D)

sensor1.open()
sensor1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
sensor2.open()
sensor2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = sensor1.get_timing()
if timing < 20000:
    timing = 20000
print("Read Timing = ", timing/1000, " (msec)")

for rpt in range(500):
    distance1 = sensor1.get_distance()
    distance2 = sensor2.get_distance()
    print("{:5d} mm, {:5d} mm".format(distance1, distance2))
    time.sleep(timing/1000000.00)
    
sensor1.stop_ranging()
sensor1.close()
GPIO.output(VL53_1_XSHUT, GPIO.LOW)
sensor2.stop_ranging()
sensor2.close()
GPIO.output(VL53_2_XSHUT, GPIO.LOW)
GPIO.cleanup()
