#!/usr/bin/env python

""" The main module for running and testing the stitching algorithm. """

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import time
import os.path
import sys
import socket
import pickle
import struct
import cv2
import imutils
from imutils.video import VideoStream
from .panorama import Stitcher
from .configuration import Configuration
from .scanner import Scanner
from .configuration import NumField
from .configuration import DirectoryField
from .configuration import FileField

def main():
    """ The main script for instantiating a CLI to navigate stitching. """
    config = Configuration()
    print("Choose Option:")
    print("0) Quit")
    print("1) Reconfigure Profile")
    print("2) Stitch from cameras")
    print("3) Stitch from 2 videos")
    print("4) Stitch from 4 videos")
    print("5) Stream stitched video")

    scanner = Scanner()
    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        reconfigure(config)
        main()
    elif opt == 2:
        left_stream, right_stream = initialize(config)
        stitch_streams(left_stream, right_stream)
        main()
    elif opt == 3:
        left, right = configure_videos(config)
        stitch_videos(left, right)
        main()
    elif opt == 4:
        stitch_all_videos(config)
        main()
    elif opt == 5:
        left, right = configure_videos(config)
        port = config.port.value
        stream_video(left, right, port)
        main()
    elif opt == 0:
        sys.exit(0)
    else:
        print("Invalid option")
        main()

def reconfigure(configuration):
    """ Reconfigures profile.yml """
    print("Choose Option")
    print("1) View current profile")
    print("2) Reconfigure option")
    print("3) Return to main options")
    scanner = Scanner()
    opt = scanner.read_int('Enter option number: ')
    if opt == 1:
        print ("Here is the current configuration:")
        configuration.print_configuration()
        reconfigure(configuration)
    elif opt == 2:
        print("Choose a field to modify")
        fields = configuration.get_fields()
        fields = [field for field in fields]
        for i in xrange(len(fields)):
            print("{0}) {1}".format(i, fields[i].key))
        opt = scanner.read_int('Choose field: ')
        field = fields[opt]

        print("Current value for {0}: {1}".format(field.key, field.value))
        prompt = "Enter new value: "
        if isinstance(field, NumField):
            new_val = scanner.read_int(prompt)
        elif isinstance(field, DirectoryField) or isinstance(field, FileField):
            new_val = scanner.read_string(prompt)
        try:
            configuration.set(field.key, new_val)
        except (KeyError, ValueError):
            reconfigure(configuration)

    else:
        main()

def initialize(config):
    """ Initializes stream from cameras. """
    left_index = config.left_index
    right_index = config.right_index
    # initialize the video streams and allow them to warmup
    time.sleep(0.5)
    print("[INFO] starting cameras...")
    left_stream = VideoStream(src=left_index).start()
    right_stream = VideoStream(src=right_index).start()

    return left_stream, right_stream

def stitch_streams(left_stream, right_stream):
    """ Stitches left and right streams. """
    stitcher = Stitcher()

    # loop over frames from the video streams
    while True:
        # grab the frames from their respective video streams
        left = left_stream.read()
        right = right_stream.read()

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
    left_stream.stop()
    right_stream.stop()

def configure_videos(config):
    """ Instantiates a CLI for configuration of videos. """
    print("Choose Option:")
    print("1) Use preconfigured left/right video streams")
    print("2) Configure streams")
    print("3) Return to main options")

    scanner = Scanner()
    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        return config.left_video.value, config.right_video.value
    elif opt == 2:
        files = os.listdir(config.video_dir.value)
        video_files = [f for f in files if f.endswith(".mp4") or f.endswith(".MP4")]
        if len(video_files) > 0:
            video_files.sort()

            print("List of video files found:")

            for i in xrange(len(video_files)):
                print(i, video_files[i], sep=') ', end='\n')

            left = scanner.read_int('Choose left video: ')
            right = scanner.read_int('Choose right video: ')

            left_video = os.path.join(config.video_dir.value, video_files[left])
            right_video = os.path.join(config.video_dir.value, video_files[right])
            return left_video, right_video
        else:
            print("Sorry, no valid files found for configuration. Please try again.")
        sys.exit(0)
    else:
        main()

def stitch_videos(left_video, right_video):
    """ Stitches local videos. """
    stitcher = Stitcher()
    left_stream = cv2.VideoCapture(left_video)
    right_stream = cv2.VideoCapture(right_video)

    while left_stream.isOpened() and right_stream.isOpened():
        left_frame = left_stream.read()[1]
        right_frame = right_stream.read()[1]

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

def stitch_all_videos(config):
    """ Stitches four local videos. """
    stitcher = Stitcher()
    fst_stitcher = Stitcher()
    snd_stitcher = Stitcher()
    video_dir = config.video_dir.value
    video_files = get_video_files(video_dir)
    video_streams = [cv2.VideoCapture(path) for path in video_files]

    while (video_streams[0].isOpened() and
           video_streams[1].isOpened() and
           video_streams[2].isOpened() and
           video_streams[3].isOpened()):
        video_frames = [stream.read()[1] for stream in video_streams]
        resized_frames = [imutils.resize(frame, width=400) for frame in video_frames]

        left_result = fst_stitcher.stitch([resized_frames[0], resized_frames[1]])
        right_result = snd_stitcher.stitch([resized_frames[2], resized_frames[3]])
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

def stream_video(left_video, right_video, port):
    """ Streams video to socket. """
    stitcher = Stitcher()

    left_stream = cv2.VideoCapture(left_video)
    right_stream = cv2.VideoCapture(right_video)

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', port))

    while left_stream.isOpened() and right_stream.isOpened():
        left_frame = left_stream.read()[1]
        right_frame = right_stream.read()[1]

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

    left_stream.release()
    right_stream.release()
    cv2.destroyAllWindows()

def get_video_files(src_dir):
    """ Gets list of video files for inclusion in video configuration CLI. """
    files = os.listdir(src_dir)
    video_files = [f for f in files if f.endswith(".mp4") or f.endswith(".MP4")]
    video_files.sort()
    video_paths = [os.path.join(src_dir, path) for path in video_files]
    return video_paths

if __name__ == "__main__":
    main()
