"""
Module for correcting and stitching frames and feeds. Used as a driver from the electron app.
"""

from __future__ import absolute_import, division, print_function

import argparse
import signal

from app.util.feed import CameraFeed

from .core.feedhandler import MultiFeedHandler

def main():
    """
    Responsible for handling stitch call from the command line.
    """
    opts = parse_args()

    if opts.use_config:
        config = opts.config_profile
        should_preview = config['just_preview']
        width = config['width']
        height = config['height']
        index = config['camera_index']
        left_index = config['left_index']
        right_index = config['right_index']
        dest = config['output_path']
        url = config['rtmp_url']
    else:
        should_preview = opts.just_preview
        width = opts.width
        height = opts.height
        index = opts.camera_index
        left_index = opts.left_index
        right_index = opts.right_index
        dest = opts.output_path
        url = opts.rtmp_url

    handler = get_feedhandler(should_preview, width, height, index, left_index, right_index)

    if should_preview:
        preview(handler, width, height)
    else:
        stream_and_record(handler, width, height, dest, url)

    def interrupt_handler(signum, frame): # pylint: disable=unused-argument
        """
        Interrupt handler to clean up feeds
        """
        # When everything is done, release the capture and close all windows.
        handler.kill()

    # Register interrupt handlers
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

def preview(handler, width, height):
    """
    Preview camera stream
    """
    handler.stitch_feeds(False, None, width, height)

def stream_and_record(handler, width, height, dest, url):
    """
    Stream the camera feed and save it to a file
    """
    handler.stitch_feeds(True, dest, width, height, url)

def get_feedhandler(should_preview, width, height, preview_index, left_index, right_index): # pylint: disable=too-many-arguments
    """
    Get appropriate feed handler
    """
    if should_preview:
        handler = get_single_handler(width, height, preview_index)
    else:
        handler = get_multi_handler(width, height, left_index, right_index)

    return handler

def get_single_handler(width, height, index):
    """
    Returns a handler for single stream
    """
    return MultiFeedHandler([CameraFeed(index, width, height)])

def get_multi_handler(width, height, left_index, right_index):
    """
    Returns a handler for multiple streams
    """
    left_feed = CameraFeed(left_index, width, height)
    right_feed = CameraFeed(right_index, width, height)
    return MultiFeedHandler([left_feed, right_feed])

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
    parser.add_argument('--stitch', action='store_true', dest='should_stitch',
                        help='Indicates whether stitching should occur.')
    parser.add_argument('--profile', action='store', dest="config_profile",
                        help='File path of configuration profile to use.')
    parser.add_argument('--url', action='store', type=str, dest='rtmp_url',
                        default="rtmp://54.227.214.22:1935/live/myStream",
                        help='RTMP url to stream to.')
    parser.add_argument('--default', action='store_true',
                        default=False, dest='use_config',
                        help='Use configuration values.')

    return parser.parse_args()

if __name__ == "__main__":
    main()
