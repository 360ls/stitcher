from __future__ import print_function
from core.panorama import Stitcher
from imutils.video import VideoStream
from core.multistitch import *
import numpy as np
import datetime
import imutils
import time
import cv2
import yaml
import os.path
import argparse
import time

config_file = "config/profile.yml"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", action="store_true")
    return parser.parse_args()

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
    time.sleep(0.5)
    print("[INFO] starting cameras...")
    leftStream = VideoStream(src=left_index).start()
    rightStream = VideoStream(src=right_index).start()

    return leftStream, rightStream

def stitch_streams(leftStream, rightStream):
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

def stitch_local():
    # get user input
    dir_name = raw_input('Enter images directory: ')
    output_dir = raw_input('Enter output directory: ')
    key_frame = raw_input('Enter key frame (full path): ')
    width = raw_input('Enter image width (resize): ')
    img_type = raw_input('Enter image type: ')

    start_time = time.time()
    # Key frame
    key_frame_file = key_frame.split('/')[-1]

    # Open the directory given in the arguments
    dir_list = []
    try:
        dir_list = os.listdir(dir_name)
        dir_list = filter(lambda x: x.find(img_type) > -1, dir_list)

    except:
        print >> sys.stderr, ("Unable to open directory: %s" % dir_name)
        sys.exit(-1)

    dir_list = map(lambda x: dir_name + "/" + x, dir_list)
    resizeImages(dir_list, dir_name, width)
    dir_list = filter(lambda x: x != key_frame, dir_list)

    base_img_rgb = cv2.imread(key_frame)

    final_img = stitchImages(key_frame_file, base_img_rgb, dir_list, output_dir, 0, img_type)
    print("Finished")
    print("Runtime: %s" % (time.time() - start_time))

def main():
    args = parse_args()
    if (args.l):
        stitch_local()
    else:
        left_index, right_index = setup()
        left_stream, right_stream = initialize(left_index, right_index)
        stitch_streams(left_stream, right_stream)

if __name__ == "__main__":
    main()
