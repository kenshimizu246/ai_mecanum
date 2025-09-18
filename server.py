from flask import Flask, jsonify, request, render_template, Response
from flask_socketio import SocketIO, emit

import mecanum_drive as md


from picame2_lib import MyCamera, MyConf, MyThread, evtMgr
import cv2
from time import sleep
import datetime
import threading
from threading import Event, Thread, Lock, current_thread
import multiprocessing
import queue
from queue import Queue

import RPi.GPIO as GPIO

from vl53l0x import MyVL53L0X, DistanceEvent
import VL53L0X
import event

is_sensor = False

VL53_0_XSHUT = 38
VL53_1_XSHUT = 40

vl_stop = False
vl_timing = 0
vl_data = None

drive_mode = "manual" # "auto", "slalom"
drive_status = "manual"
dist_limit = 250

class DriveModeConsts:
    MANUAL = "manual"
    AUTO = "auto"
    SLALOM = "slalom"

class DriveMode(DriveModeConsts):
    def __init__(self):
        self._mode = self.MANUAL

    def set(self, mode):
        self._mode = mode

    def get(self):
        return self._mode

    def is_manual(self):
        return (self._mode == self.MANUAL)

    def is_auto(self):
        return (self._mode == self.AUTO)

    def is_slalom(self):
        return (self._mode == self.SLALOM)

### SERVO UTIL FUNCTIONS ###
angle_0 = 2.5 / 20 * 100
angle_45 = 2.0 / 20 * 100
angle_90 = 1.5 / 20 * 100
angle_135 = 1.0 / 20 * 100
angle_180 = 0.5 / 20 * 100

# BCM.13 GPIO.23 BOARD.33
# BCM.18 GPIO.1  BOARD.12
servo0 = 33
servo1 = 12
frequency = 50

def _do_servo(pwm, angle):
    pwm.ChangeFrequency(50)
    pwm.start(angle)
    sleep(0.3)
    pwm.ChangeDutyCycle(angle)
    pwm.stop()

### SERVER ###
def create_app():
    app = Flask(__name__, static_folder="./templates/images")
    app.config['SECRET_KEY'] = 'secret!'
    app.logger.info('created Flask')
    socketio = SocketIO(app)
    thread_event = Event()
    thread_lock = threading.RLock()

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    dv = md.MecanumDrive(__name__)
    dm = DriveMode()

    GPIO.setup(servo0, GPIO.OUT)
    GPIO.setup(servo1, GPIO.OUT)

    hpwm = GPIO.PWM(servo0, frequency)
    vpwm = GPIO.PWM(servo1, frequency)

    try:
        import bme280_mh_z19 as sensor
        is_sensor = True
        sensor.setup()
        sensor.get_calib_param()
    except OSError:
        print("bme280_mh_z19 error")
        is_sensor = False

    GPIO.setup(VL53_0_XSHUT, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(VL53_1_XSHUT, GPIO.OUT, initial=GPIO.LOW)
    sleep(0.5)

    GPIO.output(VL53_0_XSHUT, GPIO.HIGH)
    sleep(0.1)
    sensor0 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
    sensor0.change_address(0x2B)

    GPIO.output(VL53_1_XSHUT, GPIO.HIGH)
    sleep(0.1)
    sensor1 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
    sensor1.change_address(0x2D)

    sensor0.open()
    sensor0.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
    sensor1.open()
    sensor1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

    vl_timing = sensor0.get_timing()
    if vl_timing < 20000:
        vl_timing = 20000
    print("Read Timing = ", vl_timing/1000, " (msec)")

    q = Queue()
    lock = Lock()

    def vl_worker(q, lock):
        global vl_stop, vl_timing
        while(not vl_stop):
            distance0 = sensor0.get_distance()
            distance1 = sensor1.get_distance()
            # ts = datetime.datetime.now(datetime.UTC)
            ts = None
            q.put({"back": distance0, "front": distance1, "timestamp": ts, "type": "distance"})
            sleep(vl_timing/1000000.00)
        vl_stop = True
        ts = datetime.datetime.now(datetime.UTC)
        q.put({"back": distance0, "front": distance1, "timestamp": ts}) # put dummy before vl_stop = True
        print("worker end.")

    t1 = Thread(target=vl_worker, args=(q, lock))
    t1.daemon = True
    t1.start()

    def is_aut():
        return True

    def find_room():
        dv.right_spin()
        found = False
        while(not found):
            if(vl_data["front"] > 1000):
                dv.stop()
        
    def sensor_publisher(q, lock):
        global vl_stop, vl_data
        print("pub - vl_stop: {}".format(vl_stop))
        while(not vl_stop):
            vl_data = q.get()
            if(vl_data["front"] < dist_limit):
                if(dv.get_status() in ("forward", "right_forward", "left_forward", "right", "left")):
                    print("stop...")
                    stop(False)
                    if(dm.is_auto()):
                         find_room()
            elif(vl_data["back"] < dist_limit):
                if(dv.get_status() in ("backward", "right_backward", "left_backward")):
                    print("stop...")
                    stop(False)
#            print("pub - dd: {}".format(vl_data))

    t2 = Thread(target=sensor_publisher, args=(q, lock))
    t2.daemon = True
    t2.start()

    def sensor_worker(q, lock):
        if(is_sensor):
            data1 = sensor.readData(0x76)
            data2 = sensor.mh_z19.read_all()
            ts = datetime.datetime.now(datetime.UTC)
            data = {**data1, **data2, "timestamp": ts, "type": "distance"}
            # print("background:{}".format(data))

    myt = MyThread()
    myt.start()

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 0

    def background_thread():
        global thread
        try:
            while thread_event.is_set():
                try:
                    socketio.sleep(1)
                    if(is_sensor):
                        data1 = sensor.readData(0x76)
                        data2 = sensor.mh_z19.read_all()
                        data = {**data1, **data2, **vl_data}
                        print("background:{}".format(data))
                        socketio.emit('sensor_data', data, namespace='/data')
                except OSError:
                    print("bme280_mh_z19 error")
        finally:
            thread_event.clear()
            thread = None
 

    @socketio.on('message', namespace='/data')
    def handle_message(message):
        data1 = sensor.readData(0x76)
        data2 = sensor.mh_z19.read_all()
        data = {**data1, **data2}
        print("request:{}".format(data))
        print("message: {} : {}".format(message, data))

    @app.route('/api/stop', methods=['GET'])
    def stop(rtn=True):
        _do_servo(hpwm, angle_90)
        _do_servo(vpwm, angle_45)
        res = dv.stop()
        if(rtn):
            return jsonify({'action': 'stop', 'result': res})

    @app.route('/api/forward', methods=['GET'])
    def forward():
        _do_servo(hpwm, angle_90)
        _do_servo(vpwm, angle_45)
        res = dv.forward()
        return jsonify({'action': 'forward', 'result': res})

    @app.route('/api/backward', methods=['GET'])
    def backward():
        _do_servo(hpwm, angle_90)
        _do_servo(vpwm, angle_45)
        res = dv.backward()
        return jsonify({'action': 'backward', 'result': res})

    @app.route('/api/right', methods=['GET'])
    def right():
        _do_servo(hpwm, angle_0)
        _do_servo(vpwm, angle_45)
        res = dv.right()
        return jsonify({'action': 'right', 'result': res})

    @app.route('/api/left', methods=['GET'])
    def left():
        _do_servo(hpwm, angle_180)
        _do_servo(vpwm, angle_45)
        res = dv.left()
        return jsonify({'action': 'left', 'result': res})

    @app.route('/api/left_forward', methods=['GET'])
    def left_forward():
        _do_servo(hpwm, angle_135)
        _do_servo(vpwm, angle_45)
        res = dv.left_forward()
        return jsonify({'action': 'left_forward', 'result': res})

    @app.route('/api/right_forward', methods=['GET'])
    def right_forward():
        _do_servo(hpwm, angle_45)
        _do_servo(vpwm, angle_45)
        res = dv.right_forward()
        return jsonify({'action': 'right_forward', 'result': res})

    @app.route('/api/left_backward', methods=['GET'])
    def left_backward():
        res = dv.left_backward()
        return jsonify({'action': 'left_backward', 'result': res})

    @app.route('/api/right_backward', methods=['GET'])
    def right_backward():
        res = dv.right_backward()
        return jsonify({'action': 'right_backward', 'result': res})

    @app.route('/api/left_spin', methods=['GET'])
    def left_spin():
        res = dv.left_spin()
        return jsonify({'action': 'left_spin', 'result': res})

    @app.route('/api/right_spin', methods=['GET'])
    def right_spin():
        res = dv.right_spin()
        return jsonify({'action': 'right_spin', 'result': res})

    # Camera Only
    @app.route('/api/frnt_cam_center', methods=['GET'])
    def frnt_cam_center():
        _do_servo(hpwm, angle_90)
        _do_servo(vpwm, angle_45)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_right', methods=['GET'])
    def frnt_cam_right():
        _do_servo(hpwm, angle_0)
        _do_servo(vpwm, angle_45)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_left', methods=['GET'])
    def frnt_cam_left():
        _do_servo(hpwm, angle_180)
        _do_servo(vpwm, angle_45)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_frnt_right', methods=['GET'])
    def frnt_cam_frnt_right():
        _do_servo(hpwm, angle_45)
        _do_servo(vpwm, angle_45)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_frnt_left', methods=['GET'])
    def frnt_cam_frnt_left():
        _do_servo(hpwm, angle_135)
        _do_servo(vpwm, angle_45)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_up', methods=['GET'])
    def frnt_cam_up():
        _do_servo(vpwm, angle_90)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_top', methods=['GET'])
    def frnt_cam_top():
        _do_servo(vpwm, angle_135)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})

    @app.route('/api/frnt_cam_down', methods=['GET'])
    def frnt_cam_down():
        _do_servo(vpwm, angle_0)
        res = "OK"
        return jsonify({'action': 'front_camera_center', 'result': res})


    @app.route('/api/shutdown', methods=['GET'])
    def shutdown():
        _do_servo(hpwm, angle_90)
        _do_servo(vpwm, angle_45)
        res = shutdown_server()
        return jsonify({'action': 'shutdown', 'result': res})

    @app.route('/api/set_manual_mode', methods=['GET'])
    def set_manual_mode():
        drive_mode = "manual"
        stop()
        return jsonify({'action': 'set_manual_mode'})

    @app.route('/api/set_auto_mode', methods=['GET'])
    def set_auto_mode():
        drive_mode = "auto"
        stop()
        return jsonify({'action': 'set_auto_mode'})

    @app.route("/")
    def index():
        return render_template("index.html")

    def gen(_vc):
        print("start gen...")
        global thread
        with thread_lock:
            if thread is None:
                thread_event.set()
                thread = socketio.start_background_task(target=background_thread)
        eq = _vc.add_event_queue()
        try:
            while(evt := eq.get()) is not None:
               frame = evt.get_frame()
               yield (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        finally:
            _vc.remove_event_queue(eq)

    @app.route('/video_feed')
    def video_feed():
        print("video_feed...")
        return Response(gen(myt),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    print("done create_app()")
    return app

if __name__ == '__main__':
    thread = None
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    
