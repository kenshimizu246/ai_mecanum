import time
import threading
from threading import Event, Thread, Lock, current_thread
import multiprocessing
from queue import Queue
from time import sleep

from bme280_mh_z19o import BME280Sensor
import mh_z19

stop = False

def get_air_data():
    sensor = BME280Sensor(0x76)
    sensor.get_calib_param()
    data1 = sensor.readData()
    data2 = mh_z19.read_all()
    data = {**data1, **data2}
    return data

def worker(q, lock):
    global stop
    while(not stop):
        with lock:
            data = get_air_data()
            q.put(data)
        sleep(1)
    print("end of publish data")

if __name__ == '__main__':
    q = Queue()
    lock = Lock()
    t1 = Thread(target=worker, args=(q, lock))
    t1.daemon = True # this thread will be terminated after main thread complete.
    t1.start()

    try:
        while(True):
            data = q.get()
            with lock:
                print(data)
                q.task_done()
    except KeyboardInterrupt:
        stop = True

        



