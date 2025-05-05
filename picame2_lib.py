import sys
from functools import lru_cache

import cv2
import numpy as np
import time
import threading
import multiprocessing
import queue

from picamera2 import MappedArray, Picamera2
from picamera2.devices import IMX500
from picamera2.devices.imx500 import (NetworkIntrinsics, postprocess_nanodet_detection)

mycam = None
gcnt = 0
gframe = None

class Detection:
    def __init__(self, coords, category, conf, metadata):
        """Create a Detection object, recording the bounding box, category and confidence."""
        global mycam
        self.category = category
        self.conf = conf
        self.box = mycam._imx500.convert_inference_coords(coords, metadata, mycam._picam2)

def parse_detections(metadata):
    global mycam
    myconf = mycam.get_myconf()
    bbox_normalization = mycam.get_bbox_normalization()
    threshold = myconf._threshold
    iou = myconf._iou
    max_detections = myconf._max_detections
    np_outputs = mycam.get_outputs(metadata)
    input_w, input_h = mycam.get_input_size()
    if np_outputs is None:
        return None
    if mycam.get_postprocess() == "nanodet":
        boxes, scores, classes = postprocess_nanodet_detection(outputs=np_outputs[0], conf=threshold, iou_thres=iou,
                                          max_out_dets=max_detections)[0]
        from picamera2.devices.imx500.postprocess import scale_boxes
        boxes = scale_boxes(boxes, 1, 1, input_h, input_w, False, False)
    else:
        boxes, scores, classes = np_outputs[0][0], np_outputs[1][0], np_outputs[2][0]
        if bbox_normalization:
            boxes = boxes / input_h
        boxes = np.array_split(boxes, 4, axis=1)
        boxes = zip(*boxes)
#        Detection(box, category, score, metadata, mycam.convert_inference_coords(coords, metadata))
    detections = [
        Detection(box, category, score, metadata)
        for box, score, category in zip(boxes, scores, classes)
        if score > threshold
    ]
    print("detections:{}".format(len(detections)))
    return detections


def draw_detections(jobs):
    print("start draw_detections...")
    global mycam
    global gcnt
    global gframe
    labels = mycam.get_labels()
    last_detections = []
    while(job := jobs.get()) is not None:
        request, async_result = job
        try:
            if(async_result is not None):
                detections = async_result.get()

            if request is None:
                print("Request is None!")
                continue

            if mycam is None:
                print("mycam is None!")
                continue

            if detections is None:
                    detections = last_detections
            last_detections = detections

            with MappedArray(request, 'main') as m:
                for detection in detections:
                    x, y, w, h = detection.box
                    label = f"{labels[int(detection.category)]} ({detection.conf:.2f})"
                    (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    text_x = x + 5
                    text_y = y + 15
                    overlay = m.array.copy()
                    cv2.rectangle(overlay,
                                  (text_x, text_y - text_height),
                                  (text_x + text_width, text_y + baseline),
                                  (255, 255, 255),  # Background color (white)
                                  cv2.FILLED)
                    alpha = 0.3
                    cv2.addWeighted(overlay, alpha, m.array, 1 - alpha, 0, m.array)
                    cv2.putText(m.array, label, (text_x, text_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
                if mycam.get_preserve_aspect_ratio():
                    b_x, b_y, b_w, b_h = mycam.get_roi_scaled(request)
                    color = (255, 0, 0)  # red
                    cv2.putText(m.array, "ROI", (b_x + 5, b_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    cv2.rectangle(m.array, (b_x, b_y), (b_x + b_w, b_y + b_h), (255, 0, 0, 0))
                ret, buffer = cv2.imencode('.jpg', m.array.copy())
                gframe = buffer.tobytes()
                gcnt = gcnt + 1
                print("put frame:{}:{}".format(gcnt, len(gframe)))

        finally:
            request.release()


class MyConf:
    def __init__(self):
        self._threshold = 0.55
        self._iou = 0.65
        self._max_detections = 10
        self._model = "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"

class MyCamera():
    def __init__(self, myconf=None):
        if(myconf is None):
            self._myconf = MyConf()
        else:
            self._myconf = myconf

        imx500 = IMX500(self._myconf._model)
        self._intrinsics = imx500.network_intrinsics
        self._intrinsics.update_with_defaults()
        self._picam2 = Picamera2(imx500.camera_num)
        main = {'format': 'RGB888'}
        self._config = self._picam2.create_preview_configuration(main, controls={"FrameRate": self._intrinsics.inference_rate}, buffer_count=12)
        imx500.show_network_fw_progress_bar()
        self._imx500 = imx500
        self._labels = None
        self._picam2.start(self._config, show_preview=False)

    def capture_request(self):
        return self._picam2.capture_request()

    def get_outputs(self, metadata):
        return self._imx500.get_outputs(metadata, add_batch=True)
       
    def get_input_size(self):
        return self._imx500.get_input_size()
 
    def get_bbox_normalization(self):
        return self._intrinsics.bbox_normalization

    def get_postprocess(self):
        return self._intrinsics.postprocess

    def convert_inference_coords(self, coords, metadata):
        return self._imx500.convert_inference_coords(coords, metadata, self._picam2)

    def get_picamera(self):
        return self._picam2

    def get_preserve_aspect_ratio(self):
        return self._intrinsics.preserve_aspect_ratio

    def get_roi_scaled(self, request):
        return self._imx500.get_roi_scaled(request)

    def get_myconf(self):
        return self._myconf

    def get_frame(self):
        global gcnt
        global gframe
        return (gcnt, gframe)

    def get_labels(self):
        if(not self._labels):
            labels = self._intrinsics.labels
            if self._intrinsics.ignore_dash_labels:
                labels = [label for label in labels if label and label != "-"]
            self._labels = labels
        return self._labels

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()

    def get_frame(self):
        global gcnt
        global gframe
        return (gcnt, gframe)

    def run(self):
        global mycam
        mycam = MyCamera(MyConf())
        pool = multiprocessing.Pool(processes=4)
        jobs = queue.Queue()
        thread = threading.Thread(target=draw_detections, args=(jobs,))
        thread.start()

        while True:
            request = mycam.capture_request()
            metadata = request.get_metadata()
            if metadata:
                async_result = pool.apply_async(parse_detections, (metadata, ))
                jobs.put((request, async_result))
            else:
                request.release()


