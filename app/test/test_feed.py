"""
Module responsible for testing functionality of the inputscanner utility.
"""

from __future__ import absolute_import, division, print_function
import imutils
import pytest
from ..util.feed import CameraFeed


opencv = pytest.mark.skipif(
    not pytest.config.getoption("--opencv"),
    reason="Need --opencv option to run."
)

@opencv
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

@opencv
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
    Tests to see if setting a custom FPS works.
    """ 
    # stop_event = threading.Event()
    # thread = threading.Thread(target=add_frames_to_list, args=())
    # thread.start()
    # time.sleep(10)
    # stop_event.set()
    # assert len(frame_list)/duration == 30
    pass
    
def test_feed_default_fps_is_30():
    """
    Tests to make sure fps of the default CameraFeed is 30.
    """
    # feed = CameraFeed(0)
    # assert feed.get_fps() == 30
    pass

def add_frames_to_list():
    #     feed = CameraFeed(0)
    # frame_list = []
    # while not stop_event.is_set():
    #     frame = feed.get_resized_next()
    #     frame_list.appen(frame)
    # return frame_list
    pass
