from flask_socketio import SocketIO, emit

import mecanum_drive as md


from picame2_lib import MyCamera, MyConf, MyThread, evtMgr
import cv2
import time
import threading
from threading import Event
import multiprocessing
import queue

from time import sleep

import RPi.GPIO as GPIO


dv = md.MecanumDrive('a')

dv.stop()
sleep(1)

"""
dv.forward()
sleep(2)

dv.backward()
sleep(2)

dv.right()
sleep(2)

dv.left()
sleep(2)

dv.right_forward()
sleep(2)

dv.left_forward()
sleep(5)

dv.left_backward()
sleep(5)

dv.right_backward()
sleep(5)

dv.left_spin()
sleep(5)
"""

dv.right_spin()
sleep(5)

dv.stop()




