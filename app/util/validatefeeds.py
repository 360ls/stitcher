""" Utility module for validating camera feeds. """

from __future__ import absolute_import, division, print_function
import cv2
from .textformatter import TextFormatter
from .feed import CameraFeed, VideoFeed


def view_valid_camera_feeds():
    """
    Shows all valid feed views, one after another. The next feed shows when the current is closed.
    """
    valid_feeds = []
    TextFormatter.print_heading("Checking for valid streams.")
    
    try:
        for index in xrange(6):
            if check_feed(index):
                valid_feeds.append(index)
    except NameError:
        for index in range(6):
            if check_feed(index):
                valid_feeds.append(index)

    TextFormatter.print_heading("Valid Streams:")
    for feed in valid_feeds:
        show_camera_feed(feed)

def check_feed(feed_index):
    """
    Checks if the provided index points to a valid camera feed.
    """
    camera_feed = CameraFeed(feed_index)
    return camera_feed.is_valid()

def show_camera_feed(feed_index):
    """
    Shows the camera feed pointed to by the provided feed_index.
    """
    camera_feed = CameraFeed(feed_index)
    camera_feed.show()

if __name__ == "__main__":
    view_valid_camera_feeds()
