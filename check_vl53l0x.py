import time
import threading
from threading import Event, Thread, Lock, current_thread
import multiprocessing
from queue import Queue
from time import sleep
import RPi.GPIO as GPIO

from vl53l0x import MyVL53L0X, DistanceEvent

import VL53L0X

import event

VL53_1_XSHUT = 20
VL53_2_XSHUT = 21

stop = False

def worker(vl, q):
    global stop

    while(not stop):
        vv = vl.get_data()
        q.put(vv)
        vl.interval()
    print("end of publish data")

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    vl = MyVL53L0X()
    vv = vl.get_data()
    print("{:5d} mm".format(vv))

    q = Queue()
    lock = Lock()
    t1 = Thread(target=worker, args=(vl, q))
    t1.daemon = True # this thread will be terminated after main thread complete.
    t1.start()

    try:
        while(True):
            data = q.get()
            print("distance..:{}".format(data))
            q.task_done()
    except KeyboardInterrupt:
        stop = True

    GPIO.cleanup()






