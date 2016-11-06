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

class CameraStream(Stream):
    """ Wrapper class for incoming camera feed. """
    def __init__(self, index, width):
        self.index = index
        self.feed = cv2.VideoCapture(index)
        self.width = width

    def is_valid(self):
        frame = self.feed.read()[0]
        self.feed.release()
        self.feed = cv2.VideoCapture(self.index)

        if ret:
            msg = "Index {0} is valid {1}".format(
                Formatter.color_text(str(self.index), "magenta"),
                Formatter.get_check())
            print msg
            return True
        else:
            msg = "Index {0} is invalid {1}".format(
                Formatter.color_text(str(self.index), "magenta"),
                Formatter.get_xmark())
            print msg
            return False

    def has_next(self):
        return True

    def get_next(self):
        frame = self.stream.read()[1]
        frame = imutils.resize(frame, width=self.width)
        return frame

    def close(self):
        self.stream.release()

class VideoStream(Stream):
    """ wrapper class for video stream """
    def __init__(self, path, width):
        self.path = path
        self.stream = cv2.VideoCapture(path)
        self.width = width

    def validate(self):
        ret = self.stream.read()[0]
        self.stream.release()
        self.stream = cv2.VideoCapture(self.path)

        if ret:
            msg = "Video file {0} is valid {1}".format(
                Formatter.color_text(str(self.path), "magenta"),
                Formatter.get_check())
            print msg
            return True
        else:
            msg = "Video file {0} is invalid {1}".format(
                Formatter.color_text(str(self.path), "magenta"),
                Formatter.get_xmark())
            print msg
            return False

    def has_next(self):
        return self.stream.isOpened()

    def next(self):
        frame = self.stream.read()[1]
        frame = imutils.resize(frame, width=self.width)
        return frame

    def close(self):
        self.stream.release()
