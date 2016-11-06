""" Utility module for validating camera feeds. """

from __future__ import absolute_import, division, print_function
import cv2
from .textformatter import TextFormatter


def view_valid_feeds():
    """
    Shows all valid feed views, one after another. The next feed shows when the current is closed.
    """
    valid_feeds = []
    for index in range(6):
        if check_feed(index):
            valid_feeds.append(index)
    for feed in valid_feeds:
        show_feed(feed)

def check_feed(feed_index):
    """
    Checks if the provided index points to a valid camera feed.
    """
    camera_feed = cv2.VideoCapture(feed_index)
    frame = camera_feed.read()[0]
    camera_feed.release()

    # If a frame is read, print message and return True.
    if frame:
        msg = "Index {0} is valid {1}".format(
            TextFormatter.color_text(str(feed_index), "magenta"),
            TextFormatter.get_check())
        print(msg)
        return True
    else:
        msg = "Index {0} is invalid {1}".format(
            TextFormatter.color_text(str(feed_index), "magenta"),
            TextFormatter.get_xmark())
        print(msg)
        return False

def show_feed(feed_index):
    """
    Shows the camera feed pointed to by the provided feed_index.
    """
    feed = CameraStream(index, 400)
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