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


pin0=7
pin1=11
pin2=13
pin3=15
pin4=16
pin5=18
pin6=22
pin7=36

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin0, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin5, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin6, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin7, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(pin0, GPIO.HIGH)
GPIO.output(pin0, GPIO.LOW)

def stop(self):
    GPIO.output(pin0, GPIO.LOW)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)
    GPIO.output(pin3, GPIO.LOW)
    GPIO.output(pin4, GPIO.LOW)
    GPIO.output(pin5, GPIO.LOW)
    GPIO.output(pin6, GPIO.LOW)
    GPIO.output(pin7, GPIO.LOW)
    return "OK"


GPIO.output(pin0, GPIO.HIGH)
GPIO.output(pin2, GPIO.HIGH)
sleep(3)
GPIO.output(pin0, GPIO.LOW)
GPIO.output(pin2, GPIO.LOW)

















