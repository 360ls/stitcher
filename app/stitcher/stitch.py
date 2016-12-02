"""
Module for correcting and stitching frames and feeds. Used as a driver from the electron app.
"""

from __future__ import absolute_import, division, print_function

import argparse
import cv2
import signal

from app.util.feed import CameraFeed, VideoFeed
from app.util.configure import get_configuration

from .core.feedhandler import MultiFeedHandler

feedhandler = None

def main():
    """
    Responsible for handling stitch call from the command line.
    """
    # stitch_two_videos()
    handle_arguments()
    # stitch_two_videos()

def handle_arguments():
    """
    Handles command line arguments and drive corresponding stitching tasks.
    """
    parsed_args = parse_args()

    config_profile = parsed_args.config_profile

    width = parsed_args.width
    height = parsed_args.height
    just_preview = parsed_args.just_preview

    output_path = parsed_args.output_path

    should_stream = parsed_args.should_stream
    rtmp_url = parsed_args.rtmp_url

    should_stitch = parsed_args.should_stitch

    signal.signal(signal.SIGINT, electron_handler)
    signal.signal(signal.SIGTERM, electron_handler)

    """
    If a right index value is provided, we know to instantiate the left and right feeds.
    Otherwise, a single feed is instantiated from the camera index value.
    """

    if config_profile:
        config = get_configuration(config_profile)
        left_feed = VideoFeed(config['left-video-path'], 400, 300)
        right_feed = VideoFeed(config['right-video-path'], 400, 300)

        handler = MultiFeedHandler([left_feed, right_feed])
        handler.stitch_feeds()
    else:
        if parsed_args.right_index is not None and should_stitch is not False:
            left_feed = CameraFeed(parsed_args.left_index, width, height)
            right_feed = CameraFeed(parsed_args.right_index, width, height)

            # Creates a handler for left and right feeds
            global feedhandler
            feedhandler = MultiFeedHandler([left_feed, right_feed])
        else:
            feed = CameraFeed(parsed_args.camera_index, width, height)

            # Creates a handler for single feed
            global feedhandler
            feedhandler = MultiFeedHandler([feed])

        if just_preview:
            feedhandler.stitch_feeds(True, False, None, width, height)
        else:
            # Stream will be saved to output_path, also streaming if should_stream is True
            feedhandler.stitch_feeds(True, should_stream, output_path, width, height, rtmp_url)

def electron_handler(signum, frame):
    # When everything is done, release the capture and close all windows.
    if feedhandler:
        feedhandler.kill()


def stitch_single_video(config_profile="config/profiles/standard.yml"):
    """
    Stitches (sorta) one video based on settings in the config profile.
    """

    config = get_configuration(config_profile)
    feed = VideoFeed(config['left-video-path'], 400, 300)
    handler = MultiFeedHandler([feed])
    handler.stitch_feeds()

def stitch_two_videos(config_profile="config/profiles/standard.yml"):
    """
    Stitches two videos together based on settings in the config profile.
    """

    # Retrieves configuration and sets left and right feeds.
    config = get_configuration(config_profile)
    left_feed = VideoFeed(config['left-video-path'], 400, 300)
    right_feed = VideoFeed(config['right-video-path'], 400, 300)

    handler = MultiFeedHandler([left_feed, right_feed])
    handler.stitch_feeds()

def stitch_two_corrected_videos(config_profile="config/profiles/standard.yml"):
    """
    Stitches two corredted videos together based on settings in the config profile.
    """

    # Retrieves configuration and sets left and right feeds.
    config = get_configuration(config_profile)
    left_feed = VideoFeed(config['left-video-path'], 400, 300)
    right_feed = VideoFeed(config['right-video-path'], 400, 300)

    handler = MultiFeedHandler([left_feed, right_feed])
    print("got here")
    handler.stitch_feeds(True, False)

def parse_args():
    """
    Returns parsed arguments from command line.
    """

    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Facilitates command line stitching interaction.")

    # Adds arguments to the parser for interactive mode and options.
    parser.add_argument('-f', action='store', default=None,
                        type=str,
                        dest='output_path',
                        help='File path for stream output (excluding extension).')
    parser.add_argument('-i', action='store',
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
    parser.add_argument('--leftIndex', action='store',
                        type=int,
                        dest='left_index',
                        help='Left camera index for stitching.')
    parser.add_argument('--rightIndex', action='store',
                        type=int,
                        dest='right_index',
                        help='Right camera index for stitching.')
    parser.add_argument('--stitch', action='store_true',
                        dest='should_stitch',
                        help='Indicates whether stitching should occur.')
    parser.add_argument('--profile', action='store', dest="config_profile", default=None,
                        help='File path of configuration profile to use.')
    parser.add_argument('--url', action='store', type=str, dest='rtmp_url',
                        help='RTMP url to stream to.')

    return parser.parse_args()

if __name__ == "__main__":
    main()
