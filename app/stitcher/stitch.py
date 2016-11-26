"""
Module for correcting and stitching frames and feeds. Can be used as a driver from the electron app.
"""

from __future__ import absolute_import, division, print_function
import argparse
import imutils
import numpy as np
import cv2
from app.util.feed import CameraFeed, VideoFeed
from app.util.textformatter import TextFormatter
from .correction.corrector import correct_distortion
from .core.stitcher import Stitcher
from .core.feedhandler import SingleFeedHandler, MultiFeedHandler

def main():

    def cleanup(signal_num, frame):
        """
        Handles release of feed after electron application is done with it.
        """
        feed.close
        video_output.release()
        cv2.destroyAllWindows()
        sys.exit(0)

    parsed_args = parse_args()

    output_path = parsed_args.output_path
    camera_index = parsed_args.camera_index
    just_preview = parsed_args.just_preview
    should_stream = parsed_args.should_stream
    width = parsed_args.width
    height = parsed_args.height
    rtmp_url = parsed_args.rtmp_url
    left_index = parsed_args.left_index
    right_index = parsed_args.right_index
    should_stitch = parsed_args.should_stitch

    if should_stitch:
        feed1 = CameraFeed(left_index)
        feed2 = CameraFeed(right_index)
        handler = MultiFeedHandler

        if should_stream:
            handler.stitch_feeds([feed1, feed2], True)
        else:
            handler.stitch_feeds([feed1, feed2])


    # What is this exactly?
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    extension = ''

    # Sets up the writing for writing data from camera feed.
    destination = output_path + extension
    feed = CameraFeed(camera_index)
    codec = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    video_output = cv2.VideoWriter(destination, codec, 20.0, (width, height))
    dimensions = str(width) + 'x' + str(height)

    if should_stream:
        proc = subprocess.Popen([
            'ffmpeg', '-y', '-f', 'rawvideo',
            '-s', dimensions, '-pix_fmt', 'bgr24', '-i','pipe:0','-vcodec',
            'libx264','-pix_fmt','uyvy422','-r','28','-an', '-f','flv',
            rtmp_url], stdin=subprocess.PIPE)

    while True:

        frame = feed.get_next(True, False)

        if not just_preview:
            video_output.write(frame)
        if should_stream:
            proc.stdin.write(frame.toString())

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
