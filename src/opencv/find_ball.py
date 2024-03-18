#!/usr/bin/env python3

import sys
import rospy
import cv2
import time

from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from src.blob_detector import *

class BlobDetector:
    def __init__(self, thr_min, thr_max, blur=15, blob_params=None, detection_window=None):
        self.set_threshold(thr_min, thr_max)
        self.set_blur(blur)
        self.set_blob_params(blob_params)
        self.detection_window = detection_window
        self._t0 = time.time()
        self.blob_point = Point()
        print(">> Publishing image to topic image_blob")
        self.image_pub = rospy.Publisher("/blob/image_blob", Image, queue_size=1)
        self.mask_pub = rospy.Publisher("/blob/image_mask", Image, queue_size=1)
        print(">> Publishing position to topic point_blob")
        self.blob_pub = rospy.Publisher("/blob/point_blob", Point, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
        print("<< Subscribed to topic /image_raw")

    def set_threshold(self, thr_min, thr_max):
        self._threshold = [thr_min, thr_max]

    def set_blur(self, blur):
        self._blur = blur

    def set_blob_params(self, blob_params):
        self._blob_params = blob_params

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        (rows, cols, channels) = cv_image.shape
        if cols > 60 and rows > 60:
            keypoints, mask = blob_detect(cv_image, self._threshold[0], self._threshold[1], self._blur,
                                          blob_params=self._blob_params, search_window=self.detection_window)
            cv_image = blur_outside(cv_image, 10, self.detection_window)
            cv_image = draw_window(cv_image, self.detection_window, line=1)
            cv_image = draw_frame(cv_image)
            cv_image = draw_keypoints(cv_image, keypoints)

            try:
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
                self.mask_pub.publish(self.bridge.cv2_to_imgmsg(mask, "8UC1"))
            except CvBridgeError as e:
                print(e)

            for i, keyPoint in enumerate(keypoints):
                x = keyPoint.pt[0]
                y = keyPoint.pt[1]
                s = keyPoint.size
                print("kp %d: s = %3d   x = %3d  y= %3d" % (i, s, x, y))

                x, y = get_blob_relative_position(cv_image, keyPoint)

                self.blob_point.x = x
                self.blob_point.y = y
                self.blob_pub.publish(self.blob_point)
                break

            fps = 1.0 / (time.time() - self._t0)
            self._t0 = time.time()

def main(args):
    rospy.init_node('blob_detector', anonymous=True)
    blue_min = (20, 255, 0)
    blue_max = (255, 255, 255)

    blur = 5

    x_min = 0.1
    x_max = 0.9
    y_min = 0.4
    y_max = 0.9

    detection_window = [x_min, y_min, x_max, y_max]

    params = cv2.SimpleBlobDetector_Params()

    params.minThreshold = 0
    params.maxThreshold = 100

    params.filterByArea = True
    params.minArea = 20
    params.maxArea = 20000

    params.filterByCircularity = True
    params.minCircularity = 0.1

    params.filterByConvexity = True
    params.minConvexity = 0.2

    params.filterByInertia = True
    params.minInertiaRatio = 0.7

    ic = BlobDetector(blue_min, blue_max, blur, params, detection_window)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
