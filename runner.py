from __future__ import print_function
from core.panorama import Stitcher
from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import time
import cv2
import yaml
import os.path

config_file = "config/profile.yml"

def setup():
    if not os.path.isfile(config_file):
        raise ValueError('Configuration file does not exist.')
    with open(config_file, 'r') as file:
        doc = yaml.load(file)
        left_index = doc["left-index"]
        right_index = doc["right-index"]
    return left_index, right_index

def initialize(left_index, right_index):
    # initialize the video streams and allow them to warmup
    print("[INFO] starting cameras...")
    leftStream = VideoStream(src=left_index).start()
    rightStream = VideoStream(src=right_index).start()

    return leftStream, rightStream

def stream(leftStream, rightStream):
    time.sleep(2.0)
    stitcher = Stitcher()

    # loop over frames from the video streams
    while True:
        # grab the frames from their respective video streams
        left = leftStream.read()
        right = rightStream.read()

        # resize the frames
        left = imutils.resize(left, width=400)
        right = imutils.resize(right, width=400)

        # stitch the frames together to form the panorama
        # IMPORTANT: you might have to change this line of code
        # depending on how your cameras are oriented; frames
        # should be supplied in left-to-right order
        result = stitcher.stitch([left, right])

        # no homograpy could be computed
        if result is None:
                print("[INFO] homography could not be computed")
                break

        # show the output images
        cv2.imshow("Result", result)
        cv2.imshow("Left Frame", left)
        cv2.imshow("Right Frame", right)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

    # do a bit of cleanup
    print("[INFO] cleaning up...")
    cv2.destroyAllWindows()
    leftStream.stop()
    rightStream.stop()


def main():
    left_index, right_index = setup()
    left_stream, right_stream = initialize(left_index, right_index)
    stream(left_stream, right_stream)

if __name__ == "__main__":
    main()
