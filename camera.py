import sys
import cv2
import numpy as np

from picame2_lib import (MyCamera, MyConf, parse_detections, draw_detections)

class VideoCamera(object):
    def __init__(self, mycam=None):
        self._camera = mycam

#    def __del__(self):


    def get_frame(self):
        if(self._camera is None):
            return None
        ca = self._camera
        request = ca.capture_request()
        metadata = request.get_metadata()

        detections = parse_detections(metadata, ca)

        image = draw_detections(request, detections, ca)

        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()



