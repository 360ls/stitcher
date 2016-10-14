#!/usr/bin/env python

""" The main module for running and testing the stitching algorithm. """

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import os.path
import sys
import glob
import serial
import socket
import pickle
import struct
import cv2
import imutils
import re
import subprocess
from .panorama import Stitcher
from .configuration import Configuration
from .scanner import Scanner
from .configuration import NumField
from .configuration import DirectoryField
from .configuration import FileField
from .formatter import Formatter
from .stream import CameraStream
from .stream import VideoStream
from .distortion_corrector.corrector import correct_distortion

# pylint: disable=W0702
def load_configuration():
    """
    returns configuration object
    """
    try:
        config = Configuration()
        print("{0} {1}"
              .format("Profile parsed. All configuration options valid",
                      Formatter.get_check()))
        return config
    except:
        print("{0} {1}"
              .format("Profile parsed. Invalid configuration. Please reconfigure.",
                      Formatter.get_xmark()))
        sys.exit(-1)

CONFIG = load_configuration()

def main():
    """ The main script for instantiating a CLI to navigate stitching. """
    print_spacer()
    Formatter.print_heading("Choose option:")
    Formatter.print_option(0, "Quit")
    Formatter.print_option(1, "Reconfigure Profile")
    Formatter.print_option(2, "Stitch from cameras")
    Formatter.print_option(3, "Stitch from 2 videos")
    Formatter.print_option(4, "Stitch from 4 videos")
    Formatter.print_option(5, "Stream stitched video")
    Formatter.print_option(6, "Stream validation")

    scanner = Scanner()
    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        reconfigure(CONFIG)
        main()
    elif opt == 2:
        try:
            left_stream, right_stream = initialize(CONFIG)
        except ValueError:
            main()
        stitch_streams(left_stream, right_stream)
        main()
    elif opt == 3:
        left, right = configure_videos(CONFIG)
        stitch_videos(left, right)
        main()
    elif opt == 4:
        stitch_all_videos(CONFIG)
        main()
    elif opt == 5:
        left, right = configure_videos(CONFIG)
        port = CONFIG.port.value
        stream_video(left, right, port)
        main()
    elif opt == 6:
        stream_validation()
    elif opt == 7:
        index = scanner.read_int('Enter camera index: ')
        show_stream(index)
        main()
    elif opt == 0:
        sys.exit(0)
    else:
        print("Invalid option")
        main()

def check_stream(index):
    """
    Checks if a given index is a valid usb camera index
    """
    cap = cv2.VideoCapture(index)
    ret = cap.read()[0]
    cap.release()

    if ret:
        msg = "Index {0} is valid {1}".format(
            Formatter.color_text(str(index), "magenta"),
            Formatter.get_check())
        print(msg)
        return True
    else:
        msg = "Index {0} is invalid {1}".format(
            Formatter.color_text(str(index), "magenta"),
            Formatter.get_xmark())
        print(msg)
        return False

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def check_all_streams():
    valid_streams = []
    for i in range(20):
        if (check_stream(i)):
            valid_streams.append(i)
    print_spacer()
    for stream in valid_streams:
        print ("Camera stream %s is a valid stream." % stream)
    print_spacer()

def preview_all_valid_streams():
    valid_streams = []
    for i in range(20):
        if (check_stream(i)):
            valid_streams.append(i)
    print_spacer()
    for stream in valid_streams:
        show_stream(stream)
    print_spacer()

def print_spacer():
    print ("\n--------------------\n")


def stream_validation():
    print_spacer()
    Formatter.print_option(1, "Check stream")
    Formatter.print_option(2, "Preview stream")
    Formatter.print_option(3, "Identify serial ports")
    Formatter.print_option(4, "Identify valid streams")
    Formatter.print_option(5, "Preview all valid streams")
    Formatter.print_option(0, "Exit")

    scanner = Scanner()
    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        index = scanner.read_int('Enter camera index: ')
        check_stream(index)
        main()
    elif opt == 2:
        index = scanner.read_int('Enter camera index: ')
        show_stream(index)
        main()
    elif opt == 3:
        print(serial_ports())
    elif opt == 4:
        check_all_streams()
    elif opt == 5:
        preview_all_valid_streams()
    elif opt == 0:
        sys.exit(0)
    else:
        print("Invalid option")
        main()

def reconfigure(configuration):
    """ Reconfigures profile.yml """
    Formatter.print_heading("Choose option:")
    Formatter.print_option(1, "View current profile")
    Formatter.print_option(2, "Reconfigure option")
    Formatter.print_option(3, "Return to main options")

    scanner = Scanner()
    opt = scanner.read_int('Enter option number: ')

    if opt == 1:
        Formatter.print_heading("Current configuration:")
        configuration.print_configuration()
        print("")
        reconfigure(configuration)
    elif opt == 2:
        Formatter.print_heading("Choose a field to modify")
        fields = configuration.get_fields()
        fields = [field for field in fields]
        for i in xrange(len(fields)):
            Formatter.print_option(i, fields[i].key)
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
    left_index = config.left_index.value
    right_index = config.right_index.value
    return left_index, right_index

def show_stream(index):
    """ shows stream of given index """
    stream = CameraStream(index, 400)
    if stream.validate():
        while stream.has_next():
            frame = stream.next()
            cv2.imshow("Stream", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        Formatter.print_status("[INFO] cleaning up...")
        stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def stitch_streams(left_index, right_index):
    """ Stitches left and right streams. """
    scanner = Scanner()
    width = scanner.read_int('Enter target resolution: ')
    left_stream = CameraStream(left_index, width)
    right_stream = CameraStream(right_index, width)
    stitcher = Stitcher()

    if left_stream.validate() and right_stream.validate():
        while left_stream.has_next() and right_stream.has_next():
            left_frame = correct_distortion(left_stream.next())
            right_frame = correct_distortion(right_stream.next())
            result = stitcher.stitch([left_frame, right_frame])
            cv2.imshow("Left Stream", left_frame)
            cv2.imshow("Right Stream", right_frame)
            cv2.imshow("Stitched Stream", result)

            # no homograpy could be computed
            if result is None:
                Formatter.print_err("[INFO] homography could not be computed")
                break

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        # do a bit of cleanup
        Formatter.print_status("[INFO] cleaning up...")
        left_stream.close()
        right_stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def stitch_all_streams(first_index, second_index, third_index, fourth_index):
    """ Stitches left and right streams. """
    scanner = Scanner()
    width = scanner.read_int('Enter target resolution: ')
    fst_stitcher = Stitcher()
    snd_stitcher = Stitcher()
    combo_stitcher = Stitcher()

    left_stream = CameraStream(left_index, width)
    right_stream = CameraStream(right_index, width)
    stitcher = Stitcher()

    if left_stream.validate() and right_stream.validate():
        while left_stream.has_next() and right_stream.has_next():
            left_frame = left_stream.next()
            right_frame = right_stream.next()
            result = stitcher.stitch([left_frame, right_frame])
            cv2.imshow("Left Stream", left_frame)
            cv2.imshow("Right Stream", right_frame)
            cv2.imshow("Stitched Stream", result)

            # no homograpy could be computed
            if result is None:
                Formatter.print_err("[INFO] homography could not be computed")
                break

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        # do a bit of cleanup
        Formatter.print_status("[INFO] cleaning up...")
        left_stream.close()
        right_stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def configure_videos(config):
    """ Instantiates a CLI for configuration of videos. """
    print_spacer()
    Formatter.print_heading("Choose option:")
    Formatter.print_option(1, "Use preconfigured left/right video streams")
    Formatter.print_option(2, "Configure streams")
    Formatter.print_option(3, "Return to main options")

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
            Formatter.print_err(
                "No valid video files found. Please reconfigure the video directory")
        sys.exit(0)
    else:
        main()

def stitch_videos(left_video, right_video):
    """ Stitches local videos. """
    stitcher = Stitcher()
    scanner = Scanner()
    width = scanner.read_int('Enter target resolution: ')
    left_stream = VideoStream(left_video, width)
    right_stream = VideoStream(right_video, width)

    if left_stream.validate() and right_stream.validate():
        while left_stream.has_next() and right_stream.has_next():
            left_frame = correct_distortion(left_stream.next())
            right_frame = correct_distortion(right_stream.next())
            result = stitcher.stitch([left_frame, right_frame])

            cv2.imshow("Left Stream", left_frame)
            cv2.imshow("Right Stream", right_frame)
            cv2.imshow("Stitched Stream", result)

            # no homograpy could be computed
            if result is None:
                Formatter.print_err("[INFO] homography could not be computed")
                break

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        # do a bit of cleanup
        Formatter.print_status("[INFO] cleaning up...")
        left_stream.close()
        right_stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def stitch_all_videos(config):
    """ Stitches four local videos. """
    stitcher = Stitcher()
    fst_stitcher = Stitcher()
    snd_stitcher = Stitcher()
    scanner = Scanner()
    width = scanner.read_int('Enter target resolution: ')
    video_dir = config.video_dir.value
    video_files = get_video_files(video_dir)
    video_streams = [VideoStream(path, width) for path in video_files]

    if all([stream.validate() for stream in video_streams]):
        while all([stream.has_next() for stream in video_streams]):
            frames = [stream.next() for stream in video_streams]
            left_result = fst_stitcher.stitch([frames[0], frames[1]])
            right_result = snd_stitcher.stitch([frames[2], frames[3]])
            result = stitcher.stitch([left_result, right_result])
            cv2.imshow("Stitched Stream", result)

            # no homograpy could be computed
            if result is None:
                Formatter.print_err("[INFO] homography could not be computed")
                break

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        # do a bit of cleanup
        Formatter.print_status("[INFO] cleaning up...")
        for stream in video_streams:
            stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

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
            Formatter.print_err("[INFO] homography could not be computed")
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
