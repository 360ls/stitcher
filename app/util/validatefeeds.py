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
    # camera_feed.set_fps()
    # print("Camera FPS: %s" % camera_feed.get_fps())
    if camera_feed.is_valid():
        while camera_feed.has_next():
            frame = camera_feed.get_resized_next()
            title = "Camera Feed %s" % feed_index
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        TextFormatter.print_info("Cleaning up the camera feed.")
        camera_feed.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

if __name__ == "__main__":
    view_valid_camera_feeds()
