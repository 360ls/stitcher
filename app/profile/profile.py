"""
Module for profiling a stitcher complexity.
"""

from __future__ import absolute_import, division, print_function

import argparse
import cProfile

from app.util.feed import CameraFeed
from app.util.feed import VideoFeed
from app.stitcher.core.feedhandler import MultiFeedHandler
from app.util.configure import get_configuration

def main():
    """
    Responsible for profiling stitch handler.
    """
    args = parse_args()
    pr = cProfile.Profile()
    pr.enable()
    if args.profile_single_stitch:
        stitch_single()
    else:
        stitch_double()
    pr.disable()
    pr.print_stats(sort='time')

def stitch_single():
    """
    Responsible for handling stitch of one camera.
    """
    config = get_configuration("config/profiles/singlecamerastitch.yml")
    camera_feed = CameraFeed(config['camera-index'], config['width'], config['height'])

    handler = MultiFeedHandler([camera_feed])
    handler.stitch_feeds(
        config['should-stream'], config['output-path'],
        config['width'], config['height'], config['rtmp_url'])

def stitch_double():
    """
    Responsible for handling stitch of two videos.
    """
    config = get_configuration("config/profiles/twovideostitch.yml")
    left_feed = VideoFeed(config['left-video-path'], config['width'], config['height'])
    right_feed = VideoFeed(config['right-video-path'], config['width'], config['height'])

    handler = MultiFeedHandler([left_feed, right_feed])
    handler.stitch_feeds()

def parse_args():
    """
    Returns parsed arguments
    """
    parser = argparse.ArgumentParser(description="Stitcher profiler")
    parser.add_argument('--single', dest='profile_single_stitch',
                        action='store_true', default=False)
    parser.add_argument('--double', dest='profile_double_stitch',
                        action='store_true', default=False)
    return parser.parse_args()

if __name__ == "__main__":
    main()
