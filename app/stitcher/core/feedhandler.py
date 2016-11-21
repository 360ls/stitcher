"""
Module for handling feeds for stitching and streaming.
"""
from __future__ import absolute_import, division, print_function
from abc import ABCMeta, abstractmethod
import subprocess
import cv2
from app.util.textformatter import TextFormatter
from .stitcher import Stitcher

class FeedHandler(object):
    """
    Abstract base FeedHandler class.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def stitch_feeds(self):
        """
        Takes in a list of feeds and stitches them into one outgoing stream
        """
        pass

    @abstractmethod
    def stitch_corrected_feeds(self):
        """
        Takes in a list of feeds and stitches them into one outgoing stream
        after applying distortion correction.
        """
        pass

    @abstractmethod
    def stream_rtmp(self):
        """
        Streams frames to RTMP.
        """
        pass

class SingleFeedHandler(FeedHandler):
    """
    Handler for generating a stream from a single feed.
    """
    def __init__(self, feed):
        self.feed = feed

    def stitch_feeds(self):
        stitch([self.feed], stitch_frame, False)

    def stitch_corrected_feeds(self):
        stitch([self.feed], stitch_frame, False)

    def stream_rtmp(self):
        stitch([self.feed], stitch_frame, True)

class MultiFeedHandler(FeedHandler):
    """
    Handler for generating a stream from multiple feeds.
    """
    def __init__(self, feeds):
        self.feeds = feeds

    def stitch_feeds(self):
        feed_count = len(self.feeds)
        if feed_count < 4:
            stitch(self.feeds, stitch_two_frames, False)
        else:
            stitch(self.feeds, stitch_four_frames, False)

    def stitch_corrected_feeds(self):
        feed_count = len(self.feeds)
        if feed_count < 4:
            stitch(self.feeds, stitch_two_frames, False)
        else:
            stitch(self.feeds, stitch_four_frames, False)

    def stream_rtmp(self):
        stitch(self.feeds, stitch_frame, True)


def stitch(feeds, stitcher_func, should_stream):
    """
    Main stitching function for stitching feeds together.
    """
    left_stitcher = Stitcher()
    right_stitcher = Stitcher()
    combined_stitcher = Stitcher()

    if should_stream:
        proc = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec',
                                 'rawvideo', '-s', '800x250', '-pix_fmt', 'bgr24',
                                 '-r', '5', '-i', '-', '-an', '-f',
                                 'flv', 'rtmp://54.208.55.156:1935/live/360ls']
                                , stdin=subprocess.PIPE)


    if all([feed.is_valid() for feed in feeds]):
        while all([feed.has_next() for feed in feeds]):
            frames = [feed.get_next(True, False) for feed in feeds]
            stitched_frame = stitcher_func(frames,
                                           [left_stitcher, right_stitcher, combined_stitcher])

            if should_stream:
                proc.stdin.write(stitched_frame.tostring())

            cv2.imshow("Result", stitched_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        TextFormatter.print_status("[INFO] cleaning up...")

        for feed in feeds:
            feed.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def identity(frame):
    """
    Identity function to return an input frame.
    """
    return frame

def stitch_frame(frames, _):
    """
    Stitching for single frame.
    Simple returns the frame of the first index in the frames list.
    """
    return frames[0]

def stitch_two_frames(frames, stitchers):
    """
    Stitches two frames together via the first stitcerh in the stitcher array.
    """
    return stitchers[0].stitch([frames[0], frames[1]])

def stitch_four_frames(frames, stitchers):
    """
    Stitches four frames together.
    """
    left_stitch = stitch_two_frames([frames[0], frames[1]], [stitchers[0]])
    right_stitch = stitch_two_frames([frames[2], frames[3]], [stitchers[1]])

    # Stitches the first two stitched images together with the third stitcher in the stitcher list.
    return stitch_two_frames([left_stitch, right_stitch], [stitchers[2]])
