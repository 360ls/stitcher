"""
Module for correcting and stitching frames and feeds.
"""

from __future__ import absolute_import, division, print_function
import argparse
import imutils
import numpy as np
import cv2
from app.util.feed import CameraFeed, VideoFeed
from app.util.textformatter import TextFormatter
from .correction.corrector import correct_distortion
from .core.stitcher import Stitcher

def main():
    """
    Main function of the stitch module. Responsible for handling command line options.
    """
    parsed_args = parse_args()
    option = parsed_args.option_num

    if option == 1:
        example_correct_single_frame()
    elif option == 2:
        example_cubemap()
    elif option == 3:
        example_single_stitch()
    else:
        TextFormatter.print_error("Please enter an option argument.")

def example_correct_single_frame():
    """
    Runs an example of correction of a single frame.
    """
    frame = cv2.imread("app/storage/uncorrected_checker.jpg")
    correct_single_frame(frame)

def example_cubemap():
    """
    Creates a cubemap from a series of images.
    """
    cube_frame = cv2.imread("app/storage/uncorrected.png")
    resized_cube_frame = imutils.resize(cube_frame, 300)
    cubemap(resized_cube_frame)

def example_single_stitch():
    """
    Runs an example double stitch.
    """
    img1 = cv2.imread("app/storage/stitch_tester/yard1.jpg")
    img2 = cv2.imread("app/storage/stitch_tester/yard2.jpg")
    img3 = cv2.imread("app/storage/stitch_tester/yard3.jpg")
    img4 = cv2.imread("app/storage/stitch_tester/yard4.jpg")
    img1 = imutils.resize(img1, 400)
    img2 = imutils.resize(img2, 400)
    img3 = imutils.resize(img3, 400)
    img4 = imutils.resize(img4, 400)

    stitcher = Stitcher()
    stitcher.show_stitch(img1, img2)
    stitcher.reset()
    stitcher.show_stitch(img1, img4)

def example_double_stitch():
    """
    Runs an example double stitch.
    """
    img1 = cv2.imread("app/storage/stitch_tester/yard1.jpg")
    img2 = cv2.imread("app/storage/stitch_tester/yard2.jpg")
    img3 = cv2.imread("app/storage/stitch_tester/yard3.jpg")
    img4 = cv2.imread("app/storage/stitch_tester/yard4.jpg")
    img1 = imutils.resize(img1, 400)
    img2 = imutils.resize(img2, 400)
    img3 = imutils.resize(img3, 400)
    img4 = imutils.resize(img4, 400)

    stitcher = Stitcher()
    stitcher.double_stitch(img1, img2, img3)


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
    camera_feed.show(True)

def correct_single_video(video_path="app/storage/uncorrected.mp4"):
    """
    Function to show corrected distortion for a camera feed.
    """
    video_feed = VideoFeed(video_path)
    video_feed.show_corrected()

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

def parse_args():
    """
    Returns parsed arguments from command line input.
    """

    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Determines type of capture.")

    parser.add_argument('--option', action='store',
                        type=int,
                        dest='option_num',
                        help='Option number for selected stitching and streaming option.')
    return parser.parse_args()

if __name__ == "__main__":
    main()
