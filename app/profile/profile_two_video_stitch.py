"""
Module for profiling a two-video stitch for complexity.
"""

from __future__ import absolute_import, division, print_function

import cProfile

from app.util.feed import VideoFeed
from app.stitcher.core.feedhandler import MultiFeedHandler
from app.util.configure import get_configuration

def main():
    """
    Responsible for profiling stitch handler.
    """
    pr = cProfile.Profile()
    pr.enable()
    stitch_handler()
    pr.disable()
    pr.print_stats(sort='time')

def stitch_handler():
    """
    Responsible for handling stitch of two videos.
    """
    config = get_configuration("config/profiles/twovideostitch.yml")
    left_feed = VideoFeed(config['left-video-path'], config['width'], config['height'])
    right_feed = VideoFeed(config['right-video-path'], config['width'], config['height'])

    handler = MultiFeedHandler([left_feed, right_feed])
    handler.stitch_feeds()


if __name__ == "__main__":
    main()
