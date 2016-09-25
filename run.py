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
import sys

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

def stitch_videos():
    config = Configuration()
    stitcher = Stitcher()
    left_stream = cv2.VideoCapture(config.left_video)
    right_stream = cv2.VideoCapture(config.right_video)

    while (left_stream.isOpened()):
        left_ret, left_frame = left_stream.read()
        right_ret, right_frame = right_stream.read()

        # resize the frames
        left = imutils.resize(left_frame, width=400)
        right = imutils.resize(right_frame, width=400)

        result = stitcher.stitch([left, right])

        # no homograpy could be computed
        if result is None:
            print("[INFO] homography could not be computed")
            break

        # show the output images
        cv2.imshow("Result", result)
        cv2.imshow("Left Frame", left)
        cv2.imshow("Right Frame", right)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            left_stream.release()
            right_stream.release()
            cv2.destroyAllWindows()
            main()

    left_stream.release()
    right_stream.release()
    cv2.destroyAllWindows()

def main():
    print("Choose Option:")
    print("1) Stitch local images")
    print("2) Stitch from cameras")
    print("3) Stitch from videos")
    print("4) Quit")

    try:
        opt = int(raw_input('Enter option number: '))
    except ValueError:
        print("Please enter a number.") 

    if opt == 1:
        stitch_local()
    elif opt == 2:
        left_stream, right_stream = initialize()
        stitch_streams(left_stream, right_stream)
    elif opt == 3:
        configure_videos()
        stitch_videos()
    elif opt == 4:
        sys.exit(0)
    else:
        print("Invalid option")
        main()

def configure_videos():
    print("Choose Option:")
    print("1) Use preconfigured left/right video streams")
    print("2) Configure streams")

    try:
        opt = int(raw_input('Enter option number: '))
    except ValueError:
        print("Please enter a number.") 

    if opt == 1:
        config = Configuration()
        return config.left_video, config.right_video
    elif opt == 2:
        config = Configuration()
        files = os.listdir(config.video_dir)
        video_files = [f for f in files if f.endswith(".mp4")]
        video_files.sort()
        print("List of video files found:")
        for i in xrange(len(video_files)):
            print(i, video_files[i], sep=') ', end='\n')
        try:
            left = int(raw_input('Choose left video: '))
        except ValueError:
            print("Please enter a number.") 
        try:
            right = int(raw_input('Choose right video: '))
        except ValueError:
            print("Please enter a number.") 
        left_video = os.path.join(config.video_dir, video_files[left])
        right_video = os.path.join(config.video_dir, video_files[right])
        return left_video, right_video

if __name__ == "__main__":
    main()
