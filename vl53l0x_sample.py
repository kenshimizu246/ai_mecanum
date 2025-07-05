# -*- coding: utf-8 -*-
import time
import VL53L0X
import RPi.GPIO as GPIO

VL53_1_XSHUT = 20    # GPIO for XSHUT PIN of VL53L0X No.1
VL53_2_XSHUT = 21    # GPIO for XSHUT PIN of VL53L0X No.2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# HW Standby mode (XSHUT PIN is Active Low)
GPIO.setup(VL53_1_XSHUT, GPIO.OUT, initial=GPIO.LOW)
time.sleep(0.5)

# No.1のVL53L0XをBOOTして、初期i2cアドレス(0x29)で、i2cアドレスを変更する
GPIO.output(VL53_1_XSHUT, GPIO.HIGH) # VL53L0X No.1 BOOT
time.sleep(0.1)
sensor1 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
sensor1.change_address(0x2B)    #No.1のVL53L0Xのi2cアドレスを0x2Bに変更

# センサーの測距精度を設定して、測定開始する
sensor1.open()
sensor1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = sensor1.get_timing()
if timing < 20000:
    timing = 20000
print("Read Timing = ", timing/1000, " (msec)")

for rpt in range(500):
    distance1 = sensor1.get_distance()
    print("{:5d} mm".format(distance1))
    time.sleep(timing/1000000.00)   # micro sec. -> sec.
    
sensor1.stop_ranging()
sensor1.close()
GPIO.output(VL53_1_XSHUT, GPIO.LOW) # i2cアドレスを初期アドレスに戻す
GPIO.cleanup()
