"""
Module for defining wrappers to OpenCV incoming feeds.
"""
from __future__ import absolute_import, division, print_function
from abc import ABCMeta, abstractmethod
import imutils
import cv2
from .textformatter import TextFormatter

class Feed(object):
    """
    Abstract feed class for representing a feed.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def has_next(self):
        """
        Returns True if feed has remaining frames.
        """
        pass

    @abstractmethod
    def get_next(self):
        """
        Returns the next frame from feed.
        """
        pass

    @abstractmethod
    def is_valid(self):
        """
        Returns True if feed is valid.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes feed object.
        """
        pass

class CameraFeed(Feed):
    """
    Wrapper class for incoming camera feed.
    """
    def __init__(self, feed_index, width=400):
        self.feed_index = feed_index
        self.camera_feed = cv2.VideoCapture(feed_index)
        self.width = width

    def is_valid(self):
        """
        Declares whether or not the CameraStream instance is a valid stream.
        Similar in meaning to has_next(self), but with output.
        """
        frame = self.camera_feed.grab()
        self.camera_feed.release()
        self.camera_feed = cv2.VideoCapture(self.feed_index)

        # If a frame is read, print message and return True.
        if frame:
            msg = "Index {0} is valid {1}".format(
                TextFormatter.color_text(str(self.feed_index), "magenta"),
                TextFormatter.get_check())
            print(msg)
            return True
        else:
            msg = "Index {0} is invalid {1}".format(
                TextFormatter.color_text(str(self.feed_index), "magenta"),
                TextFormatter.get_xmark())
            print(msg)
            return False

    def has_next(self):
        """
        Declares if the CameraFeed has a next frame.
        """
        return self.camera_feed.grab()

    def get_next(self):
        """
        Gets the next frame in the CameraFeed.
        """
        frame = self.camera_feed.retrieve()
        frame = imutils.resize(frame, width=self.width)
        return frame

    def close(self):
        """
        Closes the CameraFeed.
        """
        self.camera_feed.release()

class VideoFeed(Feed):
    """ Wrapper class for video feed. """
    def __init__(self, path, width=400):
        self.path = path
        self.video_feed = cv2.VideoCapture(path)
        self.width = width

    def is_valid(self):
        """
        Declares whether or not the VideoStream instance is a valid stream.
        Similar in meaning to has_next(self), but with output.
        """
        frame = self.video_feed.grab()
        self.video_feed.release()
        self.video_feed = cv2.VideoCapture(self.path)

        if frame:
            msg = "Video file {0} is valid {1}".format(
                TextFormatter.color_text(str(self.path), "magenta"),
                TextFormatter.get_check())
            print(msg)
            return True
        else:
            msg = "Video file {0} is invalid {1}".format(
                TextFormatter.color_text(str(self.path), "magenta"),
                TextFormatter.get_xmark())
            print(msg)
            return False

    def has_next(self):
        """
        Declares if the VideoFeed has a next frame.
        """
        return self.video_feed.grab()

    def get_next(self):
        """
        Gets the next frame in the VideoFeed.
        """
        frame = self.video_feed.retrieve()
        frame = imutils.resize(frame, width=self.width)
        return frame

    def close(self):
        """
        Closes the VideoFeed.
        """
        self.video_feed.release()
