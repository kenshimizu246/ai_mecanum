# -*- coding: utf-8 -*-
import time
import VL53L0X
import RPi.GPIO as GPIO

import event

class MyDistanceEvent(event.EventObject):
    def __init__(self, id, distance):
        self._id = id
        self._distance = distance

    def get_name(self):
        return self._name

class MyVL53L0X:
    def __init__(self, id, xshut, address):
        self._xshut = xshut
        self._address = address
        GPIO.setup(self._xshut, GPIO.OUT, initial=GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(self._xshut, GPIO.HIGH)
        time.sleep(0.1)
        self._sensor = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
        self._sensor.change_address(self._address)

        self._sensor.open()
        self._sensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        timing = self._sensor.get_timing()
        if timing < 20000:
            timing = 20000

        self._timing = timing

    def set_handler(self, hander):
        self._handler = handler

    def get_distance(self):
        if(self._disposed):
            return -1
        distance = self._sensor.get_distance()
        return distance

    def do_sleep(self):
        time.sleep(self._timing/1000000.00)

    def get_timing(self):
        return self._timing

    def mesure(self):
        distance = self.get_distance()
        self._handler(MyDistanceEvent(self._id, distance))

    def dispose(self):
        self._disposed = True
        self._sensor.stop_ranging()
        self._sensor.close()
        GPIO.output(self._xshut, GPIO.LOW)

