"""
Module for handling feeds for stitching and streaming.
"""
from __future__ import absolute_import, division, print_function

from abc import ABCMeta, abstractmethod
import subprocess
import cv2
import imutils

from app.util.textformatter import TextFormatter
from .stitcher import Stitcher

class FeedHandler(object):
    """
    Abstract base FeedHandler class.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def stitch_feeds(self, correct, should_stream):
        """
        Takes in a list of feeds and stitches them into one outgoing stream.
        """
        pass


class MultiFeedHandler(FeedHandler):
    """
    Handler for generating a stream from multiple feeds.
    """
    def __init__(self, feeds):
        self.feeds = feeds

    def stitch_feeds(self, correct=False, should_stream=False, output_path=None, width=400, height=200):
        feed_count = len(self.feeds)
        if feed_count == 1:
            stitch(self.feeds, stitch_frame, correct, should_stream, output_path, width, height)
        elif feed_count == 2:
            stitch(self.feeds, stitch_two_frames, correct, should_stream, output_path, width, height)
        elif feed_count == 3:
            stitch(self.feeds, stitch_three_frames, correct, should_stream, output_path, width, height)
        else:
            stitch(self.feeds, stitch_four_frames, correct, should_stream, output_path, width, height)

    def clear_feeds(self):
        for feed in self.feeds:
            feed.close()


def stitch(feeds, stitcher_func, correct, should_stream, output_path, width, height):
    """
    Main stitching function for stitching feeds together.
    """
    left_stitcher = Stitcher()
    right_stitcher = Stitcher()
    combined_stitcher = Stitcher()

    if output_path is not None:
        # Creates video writer for saving of videos.
        if imutils.is_cv3():
            codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        else:
            codec = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
        writer = cv2.VideoWriter(output_path, codec, 20.0, (width, height));

    if all([feed.is_valid() for feed in feeds]):
        while all([feed.has_next() for feed in feeds]):
            if correct is False:
                frames = [feed.get_next(True, False) for feed in feeds]
            else:
                frames = [feed.get_next(True, True) for feed in feeds]
            stitched_frame = stitcher_func(frames,
                                           [left_stitcher, right_stitcher, combined_stitcher])
            stitched_frame = cv2.resize(stitched_frame, (width, height))
            if should_stream:
                print(stitched_frame.tostring())

            if output_path is not None:
                writer.write(stitched_frame)

            cv2.imshow("Result", stitched_frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        # TextFormatter.print_status("[INFO] cleaning up...")

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
    Simply returns the frame of the first index in the frames list.
    """
    return frames[0]

def stitch_two_frames(frames, stitchers):
    """
    Stitches two frames together via the first stitcher in the stitcher array.
    """
    return stitchers[0].stitch(frames[0], frames[1])

def stitch_three_frames(frames, stitchers):
    """
    Stitches three frames together via the first and second stitcher in the stitcher array.
    """
    first_stitch = stitchers[0].stitch(frames[0], frames[1])

    return stitchers[1].stitch(first_stitch, frames[2])

def stitch_four_frames(frames, stitchers):
    """
    Stitches four frames together.
    """
    left_stitch = stitch_two_frames([frames[0], frames[1]], [stitchers[0]])
    right_stitch = stitch_two_frames([frames[2], frames[3]], [stitchers[1]])

    # Stitches the first two stitched images together with the third stitcher in the stitcher list.
    return stitch_two_frames([left_stitch, right_stitch], [stitchers[2]])
