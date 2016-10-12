#!/usr/bin/env python

""" The main module for running and testing the stitching algorithm. """

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import argparse
import os.path
import sys
import socket
import pickle
import struct
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
def main():
    """ The main script for instantiating a CLI to navigate stitching. """
    parsed_args = parse_args()
    if not parsed_args.interactive_mode:
        print("")
        Formatter.print_heading("Choose option:")
        Formatter.print_option(0, "Quit")
        Formatter.print_option(1, "Reconfigure Profile")
        Formatter.print_option(2, "Stitch from cameras")
        Formatter.print_option(3, "Stitch from 2 videos")
        Formatter.print_option(4, "Stitch from 4 videos")
        Formatter.print_option(5, "Stream stitched video")
        Formatter.print_option(6, "Check stream")
        Formatter.print_option(7, "Preview stream")
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
            left_stream, right_stream = initialize(CONFIG)
        except ValueError:
            continue_cli(int_flag)
        stitch_streams(left_stream, right_stream)
        continue_cli(int_flag)
    elif opt == 3:
        left, right = configure_videos(CONFIG, int_flag)
        res = get_res(int_flag, CONFIG)
        stitch_videos(left, right, res)
        continue_cli(int_flag)
    elif opt == 4:
        res = get_res(int_flag, CONFIG)
        stitch_all_videos(CONFIG, res)
        continue_cli(int_flag)
    elif opt == 5:
        left, right = configure_videos(CONFIG, int_flag)
        port = CONFIG.port.value
        stream_video(left, right, port)
        continue_cli(int_flag)
    elif opt == 6:
        index = scanner.read_int('Enter camera index: ')
        check_stream(index)
        continue_cli(int_flag)
    elif opt == 7:
        index = scanner.read_int('Enter camera index: ')
        show_stream(index)
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

def stitch(left_stream, right_stream):
    """
    Stitches frames coming from two streams
    """
    stitcher = Stitcher()
    if left_stream.validate() and right_stream.validate():
        proc = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo','-vcodec', 'rawvideo', '-s', '800x225', '-pix_fmt', 'rgb24', '-vb', '200k', '-r', '24', '-i', '-', '-an', '-f', 'flv', 'rtmp://localhost:1935/live-test/myStream'], stdin=subprocess.PIPE)
	while left_stream.has_next() and right_stream.has_next():
            left_frame = left_stream.next()
            right_frame = right_stream.next()
            result = stitcher.stitch([left_frame, right_frame])

            cv2.imshow("Left Stream", left_frame)
            cv2.imshow("Right Stream", right_frame)
            cv2.imshow("Stitched Stream", result)
	    proc.stdin(result.toString())
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
    stitch(left_stream, right_stream)

def configure_videos(config, int_flag):
    """ Instantiates a CLI for configuration of videos. """
    if int_flag:
        return config.left_video.value, config.right_video.value
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

def stitch_videos(left_video, right_video, res):
    """ Stitches local videos. """
    left_stream = VideoStream(left_video, res)
    right_stream = VideoStream(right_video, res)
    stitch(left_stream, right_stream)

def stitch_all_videos(config, res):
    """ Stitches four local videos. """
    stitcher = Stitcher()
    fst_stitcher = Stitcher()
    snd_stitcher = Stitcher()
    video_dir = config.video_dir.value
    video_files = get_video_files(video_dir)
    video_streams = [VideoStream(path, res) for path in video_files]

    if len(video_streams) < 4:
        Formatter.print_err("Only {0} video files found".format(len(video_streams)))
        return

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
