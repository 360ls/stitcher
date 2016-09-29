#!/usr/bin/env python

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
import utils.scanner as scanner
import socket
import sys
import pickle
import struct

def main():
    print("Choose Option:")
    print("0) Quit")
    print("1) Stitch local images")
    print("2) Stitch from cameras")
    print("3) Stitch from 2 videos")
    print("4) Stitch from 4 videos")
    print("5) Stream stitched video")

    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        stitch_local()
    elif opt == 2:
        left_stream, right_stream = initialize()
        stitch_streams(left_stream, right_stream)
    elif opt == 3:
        left, right = configure_videos()
        stitch_videos(left, right)
    elif opt == 4:
        stitch_all_videos()
    elif opt == 5:
        left, right = configure_videos()
        stream_video(left, right)
    elif opt == 0:
        sys.exit(0)
    else:
        print("Invalid option")
        main()

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

def configure_videos():
    print("Choose Option:")
    print("1) Use preconfigured left/right video streams")
    print("2) Configure streams")
    print("3) Return to main options")

    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        config = Configuration()
        return config.left_video, config.right_video
    elif opt == 2:
        config = Configuration()
        files = os.listdir(config.video_dir)
        video_files = [f for f in files if f.endswith(".mp4") or f.endswith(".MP4")]
        if len(video_files) > 0:
		video_files.sort()

        	print("List of video files found:")

        	for i in xrange(len(video_files)):
            		print(i, video_files[i], sep=') ', end='\n')

        	left = scanner.read_int('Choose left video: ')
        	right = scanner.read_int('Choose right video: ')

        	left_video = os.path.join(config.video_dir, video_files[left])
        	right_video = os.path.join(config.video_dir, video_files[right])
        	return left_video, right_video
	else:
		print("Sorry, no valid files found for configuration. Please try again.")
		sys.exit(0)
    elif opt == 3:
        main()
    else:
        sys.exit(0)

def stitch_videos(left_video, right_video):
    stitcher = Stitcher()
    left_stream = cv2.VideoCapture(left_video)
    right_stream = cv2.VideoCapture(right_video)

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

def stitch_all_videos():
    stitcher = Stitcher()
    fst_stitcher = Stitcher()
    snd_stitcher = Stitcher()
    config = Configuration()
    video_dir = config.video_dir
    video_files = get_video_files(video_dir)
    video_streams = [cv2.VideoCapture(path) for path in video_files]

    while (video_streams[0].isOpened() and
           video_streams[1].isOpened() and
           video_streams[2].isOpened() and
           video_streams[3].isOpened()
           ):
        video_frames = [stream.read()[1] for stream in video_streams]
        resized_frames = [imutils.resize(frame, width=400) for frame in video_frames]

        left_result = fst_stitcher.stitch([video_frames[0], video_frames[1]])
        right_result = snd_stitcher.stitch([video_frames[2], video_frames[3]])
        result = stitcher.stitch([left_result, right_result])

        # no homograpy could be computed
        if left_result is None or right_result is None:
            print("[INFO] homography could not be computed")
            break

        cv2.imshow("Result", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            for stream in video_streams:
                stream.release()
            cv2.destroyAllWindows()
            main()

def stream_video(left_video, right_video):
    stitcher = Stitcher()

    left_stream = cv2.VideoCapture(left_video)
    right_stream = cv2.VideoCapture(right_video)

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost',8089))

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

        data = pickle.dumps(result)
        clientsocket.sendall(struct.pack("L", len(data))+data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            left_stream.release()
            right_stream.release()
            cv2.destroyAllWindows()
            main()

    left_stream.release()
    right_stream.release()
    cv2.destroyAllWindows()

def get_video_files(src_dir):
    files = os.listdir(src_dir)
    video_files = [f for f in files if f.endswith(".mp4") or f.endswith(".MP4")]
    video_files.sort()
    video_paths = [os.path.join(src_dir, path) for path in video_files]
    return video_paths

if __name__ == "__main__":
    main()
