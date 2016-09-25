from __future__ import print_function
from __future__ import division
from core.panorama import Stitcher
from imutils.video import VideoStream
from core.multistitch import Multistitcher
from utils.configuration import Configuration
import numpy as np
import datetime
import imutils
import time
import cv2
import yaml
import os.path
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", action="store_true")
    return parser.parse_args()

def initialize():
    config = Configuration()
    left_index = config.left_index
    right_index = config.right_index
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
    iterations = 10
    iter_times = []
    config = Configuration()

    # get configuration
    dir_name = config.source_dir
    output_dir = config.dest_dir
    key_frame = config.keyframe
    width = config.width
    img_type = config.format

    stitcher = Multistitcher(dir_name)

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
    stitcher.resizeImages(dir_list, dir_name, width)
    dir_list = filter(lambda x: x != key_frame, dir_list)

    base_img_rgb = cv2.imread(key_frame)

    for i in xrange(iterations):
        print("Starting Iteration #%d" % i)
        start_time = time.time()
        final_img = stitcher.stitchImages(key_frame_file, base_img_rgb, dir_list, output_dir, 0, img_type)
        print("Finished Iteration #%d" % i)
        runtime = time.time() - start_time
        iter_times.append(runtime)
        print("Runtime: %s" % (runtime))

    for i in xrange(iterations):
        msg = "Runtime for Iteration #{0}: {1}s".format(i, iter_times[i])
        print(msg)
    print("Average runtime: %f" % (sum(iter_times)/iterations))

def main():
    args = parse_args()
    if (args.l):
        stitch_local()
    else:
        left_stream, right_stream = initialize()
        stitch_streams(left_stream, right_stream)

if __name__ == "__main__":
    main()
