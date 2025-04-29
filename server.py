from flask import Flask, jsonify, request, render_template, Response

import mecanum_drive as md

import picame2_lib as pc
from picame2_lib import MyCamera, MyConf
# from camera import VideoCamera
import cv2

def create_app():
    myc = pc.MyCamera(pc.MyConf())

    app = Flask(__name__, static_folder="./templates/images")
    app.logger.info('created Flask')

    dv = md.MecanumDrive(__name__)
    app.logger.info('created mecanum drive')

    app.logger.info('Camera initialization has done!')

#    @app.before_first_request
#    def activate_job():
#        def run_job():
#            while True:
#                print("Run recurring task")
#                time.sleep(3)
#
#        thread = threading.Thread(target=run_job)
#        thread.start()

#     @app.before_request
#    @app.before_first_request
#    def init():
#        print("MyCamera start!")
#        myc = pc.MyCamera(pc.MyConf())
#        print("MyCamera done!")

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 0

    @app.route('/api/stop', methods=['GET'])
    def stop():
        res = dv.stop()
        return jsonify({'action': 'stop', 'result': res})

    @app.route('/api/forward', methods=['GET'])
    def forward():
        res = dv.forward()
        return jsonify({'action': 'forward', 'result': res})

    @app.route('/api/backward', methods=['GET'])
    def backward():
        res = dv.backward()
        return jsonify({'action': 'backward', 'result': res})

    @app.route('/api/right', methods=['GET'])
    def right():
        res = dv.right()
        return jsonify({'action': 'right', 'result': res})

    @app.route('/api/left', methods=['GET'])
    def left():
        res = dv.left()
        return jsonify({'action': 'left', 'result': res})

    @app.route('/api/left_forward', methods=['GET'])
    def left_forward():
        res = dv.left_forward()
        return jsonify({'action': 'left_forward', 'result': res})

    @app.route('/api/right_forward', methods=['GET'])
    def right_forward():
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

    @app.route('/api/shutdown', methods=['GET'])
    def shutdown():
        res = shutdown_server()
        return jsonify({'action': 'shutdown', 'result': res})

    @app.route("/")
    def index():
        return render_template("index.html")

    def gen(_vc):
        while True:
            app.logger.info('try to get frame.')
            frame = _vc.get_frame()
            app.logger.info('got frame.')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            app.logger.info('loop done.')

    @app.route('/video_feed')
    def video_feed():
        # return Response(gen(VideoCamera(myc)),
        return Response(gen(myc),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    print("done create_app()")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    
