#!/usr/bin/env python

""" The main module for running and testing the stitching algorithm. """

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import subprocess
import argparse
import os.path
import sys
import glob
import socket
import pickle
import struct
import serial
import cv2
import imutils
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
from .stream_handler import SingleStreamHandler
from .stream_handler import MultiStreamHandler

def parse_args():
    """
    returns parsed arugments from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', action='store_true', default=False,
                        dest='interactive_mode',
                        help='Set interactive mode off')
    parser.add_argument('--option', action='store',
                        type=int,
                        dest='option_num',
                        help='Option number')
    return parser.parse_args()

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

# pylint: disable=R0915
# pylint: disable=R0912
def main():
    """ The main script for instantiating a CLI to navigate stitching. """
    parsed_args = parse_args()
    if not parsed_args.interactive_mode:
        print_spacer()
        Formatter.print_heading("Choose option:")
        Formatter.print_option(0, "Quit")
        Formatter.print_option(1, "Reconfigure Profile")
        Formatter.print_option(2, "Stitch from cameras")
        Formatter.print_option(3, "Stitch from 2 videos")
        Formatter.print_option(4, "Stitch from 4 videos")
        Formatter.print_option(5, "Stream stitched video")
        Formatter.print_option(6, "Stream validation")
        Formatter.print_option(7, "Stitch from 2 corrected videos")
        Formatter.print_option(8, "Stitch from 2 corrected cameras")
        scanner = Scanner()
        opt = scanner.read_int('Enter option number: ')
    else:
        opt = parsed_args.option_num

    int_flag = parsed_args.interactive_mode

    if opt == 1:
        reconfigure(CONFIG)
        continue_cli(int_flag)
    elif opt == 2:
        try:
            left_index, right_index = initialize(CONFIG)
        except ValueError:
            continue_cli(int_flag)
        res = get_res(int_flag, CONFIG)
        lstream = CameraStream(left_index, res)
        rstream = CameraStream(right_index, res)
        stitch_uncorrected_streams([lstream, rstream])
        continue_cli(int_flag)
    elif opt == 3:
        left, right = configure_videos(CONFIG, int_flag)
        res = get_res(int_flag, CONFIG)
        left_video_stream = VideoStream(left, res)
        right_video_stream = VideoStream(right, res)
        stitch_uncorrected_streams([left_video_stream, right_video_stream])
        continue_cli(int_flag)
    elif opt == 4:
        res = get_res(int_flag, CONFIG)
        video_dir = CONFIG.video_dir.value
        video_streams = get_video_streams(video_dir, res)
        stitch_uncorrected_streams(video_streams)
        continue_cli(int_flag)
    elif opt == 5:
        try:
            left_index, right_index = initialize(CONFIG)
        except ValueError:
            continue_cli(int_flag)
        res = get_res(int_flag, CONFIG)
        lstream = CameraStream(left_index, res)
        rstream = CameraStream(right_index, res)
        stream_stitched_streams([lstream, rstream])
        continue_cli(int_flag)
    elif opt == 6:
        stream_validation()
        continue_cli(int_flag)
    elif opt == 7:
        left, right = configure_videos(CONFIG, int_flag)
        res = get_res(int_flag, CONFIG)
        left_video_stream = VideoStream(left, res)
        right_video_stream = VideoStream(right, res)
        stitch_corrected_streams([left_video_stream, right_video_stream])
        continue_cli(int_flag)
    elif opt == 8:
        try:
            left_index, right_index = initialize(CONFIG)
        except ValueError:
            continue_cli(int_flag)
        res = get_res(int_flag, CONFIG)
        lstream = CameraStream(left_index, res)
        rstream = CameraStream(right_index, res)
        stitch_corrected_streams([lstream, rstream])
        continue_cli(int_flag)
    elif opt == 0:
        sys.exit(0)
    else:
        print("Invalid option")
        main()

def continue_cli(int_flag):
    """
    Continues CLI if in interactive mode
    """
    if int_flag:
        sys.exit(0)
    else:
        main()

def get_res(int_flag, config):
    """
    Returns configured resolution or resolution from input if interactive
    """
    if int_flag:
        return config.resolution.value
    else:
        scanner = Scanner()
        res = scanner.read_int('Enter target resolution: ')
        return res

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
            ser = serial.Serial(port)
            ser.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def check_all_streams():
    """
    Lists all connected camera streams
    """
    valid_streams = []
    for i in range(20):
        if check_stream(i):
            valid_streams.append(i)
    print_spacer()
    for stream in valid_streams:
        print ("Camera stream %s is a valid stream." % stream)
    print_spacer()

def preview_all_valid_streams():
    """
    Shows preview of all valid camera streams
    """
    valid_streams = []
    for i in range(20):
        if check_stream(i):
            valid_streams.append(i)
    print_spacer()
    for stream in valid_streams:
        show_stream(stream)
    print_spacer()

def print_spacer():
    """
    Prints separator line
    """
    print ("\n--------------------\n")

def stream_validation():
    """
    CLI option for validating streams
    """
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

def stitch_uncorrected_stream(stream):
    """ Stitches single stream """
    handler = SingleStreamHandler(stream)
    handler.stitch_streams()

def stitch_corrected_stream(stream):
    """ Stitches single stream """
    handler = SingleStreamHandler(stream)
    handler.stitch_corrected_streams()

def stitch_uncorrected_streams(streams):
    """ Stitches left and right streams. """
    handler = MultiStreamHandler(streams)
    handler.stitch_streams()

def stitch_corrected_streams(streams):
    """ Stitches left and right streams. """
    handler = MultiStreamHandler(streams)
    handler.stitch_corrected_streams()

def stream_stitched_stream(stream):
    handler = SingleStreamHandler(stream)
    handler.stream_rtmp()

def stream_stitched_streams(streams):
    handler = MultiStreamHandler(streams)
    handler.stream_rtmp()

def configure_videos(config, int_flag):
    """ Instantiates a CLI for configuration of videos. """
    if int_flag:
        return config.left_video.value, config.right_video.value

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

def get_video_files(src_dir):
    """ Gets list of video files for inclusion in video configuration CLI. """
    files = os.listdir(src_dir)
    video_files = [f for f in files if f.endswith(".mp4") or f.endswith(".MP4")]
    video_files.sort()
    video_paths = [os.path.join(src_dir, path) for path in video_files]
    return video_paths

def get_video_streams(src_dir, res):
    video_files = get_video_files(src_dir)
    return [VideoStream(filepath, res) for filepath in video_files]

if __name__ == "__main__":
    main()
