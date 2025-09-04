# -*- coding: utf-8 -*-
import time
import VL53L0X
import RPi.GPIO as GPIO

import event

"""
36 : GPIO 27 : 16
38 : GPIO 28 : 20
40 : GPIO 29 : 21
"""

VL53_1_XSHUT = 20
VL53_2_XSHUT = 21
# VL53_1_XSHUT = 38
# VL53_2_XSHUT = 40

class DistanceEvent(event.EventObject):
    def __init__(self, name, id, distance):
        self._name = name
        self._id = id
        self._distance = distance

    def get_name(self):
        return self._name


class MyVL53L0X():
    def __init__(self, xshut=20, i2c_addr = 0x29, new_addr  = 0x2B):
        GPIO.setup(VL53_1_XSHUT, GPIO.OUT, initial=GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(VL53_1_XSHUT, GPIO.HIGH)
        time.sleep(0.1)
        self._sensor = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
        self._sensor.change_address(0x2B)

        self._sensor.open()
        self._sensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        self._timing = self._sensor.get_timing()
        if self._timing < 20000:
            self._timing = 20000
        print("Read Timing = ", self._timing/1000, " (msec)")

    def get_data(self):
        distance = self._sensor.get_distance()
        # time.sleep(self._timing/1000000.00)
        return distance

    def interval(self):
        time.sleep(self._timing/1000000.00)

    def stop(self):
        self._sensor.stop_ranging()
        self._sensor.close()
        GPIO.output(VL53_1_XSHUT, GPIO.LOW)


if __name__ == '__main__':
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # GPIO.setmode(GPIO.BOARD)

        vl = MyVL53L0X()
        vv = vl.get_data()
        print("{:5d} mm".format(vv))
        vl.stop()

        GPIO.cleanup()
    except KeyboardInterrupt:
        pass


