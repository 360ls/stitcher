"""
Module responsible for testing functionality of the inputscanner utility.
"""

from __future__ import absolute_import, division, print_function
import imutils
import cv2
from ..util.feed import CameraFeed

def test_frame_resize():
    """
    Checks to make sure resize of a frame is working correcly.
    """
    passed = True
    feed = CameraFeed(0)
    frame = feed.get_next()
    try:
        imutils.resize(frame, 400)
    except AttributeError:
        # This means there was an error in the resize method of get_next()
        passed = False
    assert passed is True


def test_frame_get_resized_next():
    """
    Checks to make sure resizing within get_resized_next method is working.
    """
    passed = True
    feed = CameraFeed(0)
    try:
        feed.get_resized_next()
    except AttributeError:
        # This means there was an error in the resize method of get_resized_next()
        passed = False
    assert passed is True

def test_feed_fps_set():
    """
    Tests to see if setting a custom FPS works. FPS is referenced by the
    index 5 in the enumeration of opencv camera properties.
    """
    feed = cv2.VideoCapture(0)
    fps_value = feed.get(5)
    feed.set(5, 30)
    fps_value_2 = feed.get(5)
    assert fps_value == fps_value_2

def test_feed_default_fps_is_30():
    """
    Tests to make sure fps of the default CameraFeed is 30.
    """
    feed = CameraFeed(0)
    fps_value = feed.get_fps()
    assert fps_value == 30
