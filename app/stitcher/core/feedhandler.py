"""
Module for handling feeds for stitching and streaming.
"""
from abc import ABCMeta, abstractmethod
import subprocess
import cv2
from app.util.textformatter import TextFormatter
from ..correction.corrector import correct_distortion
from .stitcher import Stitcher

class FeedHandler(object):
    """
    Abstract base FeedHandler class.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def stitch_feeds(self):
        """
        Takes in a list of feeds and stitches them into one stream
        """
        pass

    @abstractmethod
    def stitch_corrected_feeds(self):
        """
        Takes in a list of feeds and stitches them into one stream
        after applying distortion correction
        """
        pass

    @abstractmethod
    def stream_rtmp(self):
        """
        Streams frames to RTMP
        """
        pass

class SingleFeedHandler(FeedHandler):
    """
    Handler for generating a stream from a single feed.
    """
    def __init__(self, stream):
        self.stream = stream

    def stitch_streams(self):
        stitch([self.stream], identity, stitch_frame, False)

    def stitch_corrected_streams(self):
        stitch([self.stream], correct_distortion, stitch_frame, False)

    def stream_rtmp(self):
        stitch([self.stream], identity, stitch_frame, True)

class MultiFeedHandler(FeedHandler):
    """
    Handler for generating a stream from multiple feeds.
    """
    def __init__(self, streams):
        self.streams = streams

    def stitch_streams(self):
        stream_count = len(self.streams)
        if stream_count < 4:
            stitch(self.streams, identity, stitch_two_frames, False)
        else:
            stitch(self.streams, identity, stitch_four_frames, False)

    def stitch_corrected_streams(self):
        stream_count = len(self.streams)
        if stream_count < 4:
            stitch(self.streams, correct_distortion, stitch_two_frames, False)
        else:
            stitch(self.streams, correct_distortion, stitch_four_frames, False)

    def stream_rtmp(self):
        stitch(self.streams, identity, stitch_frame, True)


def stitch(streams, correction_func, stitcher_func, should_stream):
    """
    Generic stitching function
    """
    left_stitcher = Stitcher()
    right_stitcher = Stitcher()
    combined_stitcher = Stitcher()

    if should_stream:
        proc = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec',
                                 'rawvideo', '-s', '800x250', '-pix_fmt', 'bgr24',
                                 '-r', '5', '-i', '-', '-an', '-f',
                                 'flv', 'rtmp://54.208.55.156:1935/live/myStream']
                                , stdin=subprocess.PIPE)


    if all([stream.validate for stream in streams]):
        while all([stream.has_next() for stream in streams]):
            frames = [correction_func(stream.next()) for stream in streams]
            stitched_frame = stitcher_func(frames,
                                           [left_stitcher, right_stitcher, combined_stitcher])

            if should_stream:
                proc.stdin.write(stitched_frame.tostring())

            cv2.imshow("Result", stitched_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        TextFormatter.print_status("[INFO] cleaning up...")

        for stream in streams:
            stream.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def identity(frame):
    """
    Identity function
    """
    return frame

def stitch_frame(frames, _):
    """
    Stitching for single frame
    """
    return frames[0]

def stitch_two_frames(frames, stitchers):
    """
    Stitching for two frames
    """
    return stitchers[0].stitch([frames[0], frames[1]])

def stitch_four_frames(frames, stitchers):
    """
    Stitching for four frames
    """
    left_stitch = stitch_two_frames([frames[0], frames[1]], [stitchers[0]])
    right_stitch = stitch_two_frames([frames[2], frames[3]], [stitchers[1]])
    return stitch_two_frames([left_stitch, right_stitch], [stitchers[2]])
