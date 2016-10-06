"""
Wrapper classes for OpenCV streams
"""
from abc import ABCMeta, abstractmethod
import imutils
import cv2
from .formatter import Formatter

class Stream(object):
    """
    Abstract base stream class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def has_next(self):
        """ returns True if stream has remaining frames """
        pass

    @abstractmethod
    def next(self):
        """ returns the next frame from stream """
        pass

    @abstractmethod
    def validate(self):
        """ returns True if stream is valid """
        pass

    @abstractmethod
    def close(self):
        """ closes stream object """
        pass

class CameraStream(Stream):
    """ wrapper class for camera stream """
    def __init__(self, index, width):
        self.index = index
        self.stream = cv2.VideoCapture(index)
        self.width = width

    def validate(self):
        ret = self.stream.read()[0]
        self.stream.release()
        self.stream = cv2.VideoCapture(self.index)

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

    def next(self):
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
