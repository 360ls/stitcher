"""
Stream handler module
"""
from abc import ABCMeta, abstractmethod
import cv2
from .formatter import Formatter
from .distortion_corrector.corrector import correct_distortion
from .panorama import Stitcher

class StreamHandler(object):
    """
    Abstract base stream class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def stitch_streams(self):
        """
        Takes in a list of streams and stitches them into one stream
        """
        pass

    @abstractmethod
    def stitch_corrected_streams(self):
        """
        Takes in a list of streams and stitches them into one stream
        after applying distortion corrections
        """
        pass

class SingleStreamHandler(StreamHandler):
    """
    Stream handler for a single video stream
    """
    def __init__(self, stream):
        self.stream = stream

    def stitch_streams(self):
        stitch([self.stream], identity, stitch_frame)

    def stitch_corrected_streams(self):
        stitch([self.stream], correct_distortion, stitch_frame)

class MultiStreamHandler(StreamHandler):
    """
    Stream handler for multiple video streams
    """
    def __init__(self, streams):
        self.streams = streams

    def stitch_streams(self):
        stream_count = len(self.streams)
        if stream_count < 4:
            stitch(self.streams, identity, stitch_two_frames)
        else:
            stitch(self.streams, identity, stitch_four_frames)

    def stitch_corrected_streams(self):
        stream_count = len(self.streams)
        if stream_count < 4:
            stitch(self.streams, correct_distortion, stitch_two_frames)
        else:
            stitch(self.streams, correct_distortion, stitch_four_frames)

def stitch(streams, correction_func, stitcher_func):
    left_stitcher = Stitcher()
    right_stitcher = Stitcher()
    combined_stitcher = Stitcher()

    if all([stream.validate for stream in streams]):
        while all([stream.has_next() for stream in streams]):
            frames = [correction_func(stream.next()) for stream in streams]
            stitched_frame = stitcher_func(frames, [left_stitcher, right_stitcher, combined_stitcher])

            cv2.imshow("Result", stitched_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        Formatter.print_status("[INFO] cleaning up...")

        for stream in streams:
            stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def identity(frame):
    return frame

def stitch_frame(frames, stitchers):
    return frames[0]

def stitch_two_frames(frames, stitchers):
    return stitchers[0].stitch([frames[0], frames[1]])

def stitch_four_frames(frames, stitchers):
    left_stitch = stitch_two_frames([frames[0], frames[1]], [stitchers[0]])
    right_stitch = stitch_two_frames([frames[2], frames[3]], [stitchers[1]])
    return stitch_two_frames([left_stitch, right_stitch], [stitchers[2]])
