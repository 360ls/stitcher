"""
Module for correcting and stitching frames and feeds.
"""

from __future__ import absolute_import, division, print_function
import cv2
import imutils
import numpy as np
from .correction.corrector import correct_distortion
from app.util.feed import CameraFeed, VideoFeed
from app.util.validatefeeds import show_camera_feed
from app.util.textformatter import TextFormatter


def main():
    """
    Main function of the stitch module. Currently simply corrects a single provided frame.
    """
    cube_frame = cv2.imread("app/storage/uncorrected.png")
    resized_cube_frame = imutils.resize(cube_frame, 300)
    cubemap(resized_cube_frame)

def example_correct_single_frame():
    """
    Runs an example of correction of a single frame.
    """
    frame = cv2.imread("app/storage/uncorrected_checker.jpg")
    correct_single_frame(frame)

def correct_single_frame(frame):
    """
    Function to correct distortion on a single frame/image.
    """
    corrected_frame = correct_distortion(frame)
    resized_frame = imutils.resize(frame, 400)
    resized_corrected_frame = imutils.resize(corrected_frame, 400)
    title = "Corrected Image"
    cv2.imshow("Uncorrected Image", resized_frame)
    cv2.imshow(title, resized_corrected_frame)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        print("this happened")
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def correct_single_camera(feed_index=0):
    """
    Function to show corrected distortion for a camera feed.
    """
    camera_feed = CameraFeed(feed_index)
    if camera_feed.is_valid():
        while camera_feed.has_next():
            frame = camera_feed.get_corrected_resized_next()
            title = "Camera Feed %s" % feed_index
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        camera_feed.close()
        cv2.destroyAllWindows()
        TextFormatter.print_info("Cleaning up the camera feed.")
        cv2.waitKey(1)

def correct_single_video(video_path="app/storage/uncorrected.mp4"):
    """
    Function to show corrected distortion for a camera feed.
    """
    video_feed = VideoFeed(video_path)
    if video_feed.is_valid():
        while video_feed.has_next():
            frame = video_feed.get_corrected_resized_next()
            title = "Video Feed"
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        video_feed.close()
        cv2.destroyAllWindows()
        TextFormatter.print_info("Cleaned up the video feed.")
        cv2.waitKey(1)

def cubemap(frame):
    """
    Function to create an example cubemap from a single image.
    """
    left_half = np.concatenate((frame, frame), axis=1)
    right_half = np.concatenate((frame, frame), axis=1)
    full = np.concatenate((left_half, right_half), axis=1)
    cv2.imshow("Cube Map", full)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindows()
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
