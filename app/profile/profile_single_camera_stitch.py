"""
Module for profiling a single-camera stitch.
"""

from __future__ import absolute_import, division, print_function

import cProfile

from app.util.feed import CameraFeed
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
    Responsible for handling stitch of one camera.
    """
    config = get_configuration("config/profiles/singlecamerastitch.yml")
    camera_feed = CameraFeed(config['camera-index'], config['width'], config['height'])

    handler = MultiFeedHandler([camera_feed])
    handler.stitch_feeds(config['should-stream'], config['output-path'], config['width'], config['height'], config['rtmp_url'])


if __name__ == "__main__":
    main()
