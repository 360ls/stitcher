"""
Module for correcting and stitching frames and feeds. Used as a driver from the electron app.
"""

from __future__ import absolute_import, division, print_function

import argparse
import sys
import subprocess
import cv2

from app.util.feed import CameraFeed, VideoFeed
from app.util.configure import get_configuration

from .core.feedhandler import SingleFeedHandler, MultiFeedHandler



def main():

    stitch_two_videos()

def stitch_two_videos(config_profile="config/profile.yml"):
    """
    Stitches two videos together based on settings in the configuration profile.
    """

    # Retrieves configuration and sets left and right feeds.
    config = get_configuration(config_profile)
    left_feed = VideoFeed(config['left-video-path'])
    right_feed = VideoFeed(config['right-video-path'])

    # handler = MultiFeedHandler([left_feed, right_feed])
    # print("got here")
    # handler.stitch_feeds()

    handler = SingleFeedHandler(left_feed)
    handler.stitch_feeds()



def electron_driver():

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



def parse_args():
    """
    Returns parsed arguments from command line.
    """

    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Facilitates command line stitching interaction.")

    # Adds arguments to the parser for interactive mode and options.
    parser.add_argument('-f', action='store', required=True,
                        type=str,
                        dest='output_path',
                        help='File path for stream output (excluding extension).')
    parser.add_argument('-i', default=0, action='store',
                        type=int,
                        dest='camera_index',
                        help='Index of camera feed to be captured.')
    parser.add_argument('-p', action='store_true', default=False,
                        dest='just_preview',
                        help='Preview camera feed without writing to file or streaming.')
    parser.add_argument('-s', action='store_true', default=False,
                        dest='should_stream',
                        help='Indicates whether result should be streamed.')
    parser.add_argument('--width', action='store', default=640,
                        type=int,
                        dest='width',
                        help='Width dimension of output video')
    parser.add_argument('--height', action='store', default=480,
                        type=int,
                        dest='height',
                        help='Height dimension of output video')
    parser.add_argument('--url', action='store', default="rtmp://152.23.133.52:1935/live/myStream",
                        type=str,
                        dest='rtmp_url',
                        help='RTMP url to stream to.')
    parser.add_argument('--leftIndex', action='store', default=1,
                        type=int,
                        dest='left_index',
                        help='Left camera index for stitching.')
    parser.add_argument('--rightIndex', action='store', default=1,
                        type=int,
                        dest='right_index',
                        help='Right camera index for stitching.')
    parser.add_argument('--stitch', action='store_true', default=False,
                        dest='should_stitch',
                        help='Indicates whether stitching should occur.')

    return parser.parse_args()

if __name__ == "__main__":
    main()