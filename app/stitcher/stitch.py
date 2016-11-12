"""
Module for correcting and stitching frames and feeds.
"""

from __future__ import absolute_import, division, print_function
import cv2
import imutils
import numpy as np
from .correction.corrector import correct_distortion


def main():
    """
    Main function of the stitch module. Currently simply corrects a single provided frame.
    """
    frame = cv2.imread("app/storage/uncorrected_checker.jpg")
    cube_frame = cv2.imread("app/storage/uncorrected.png")
    resized_frame = imutils.resize(frame, 300)
    resized_cube_frame = imutils.resize(cube_frame, 300)
    correct_single_frame(resized_frame)
    cubemap(resized_cube_frame)

def correct_single_frame(frame):
    """
    Function to correct distortion on a single frame/image.
    """
    corrected_frame = correct_distortion(frame)
    title = "Corrected Image"
    cv2.imshow("Uncorrected Image", frame)
    cv2.imshow(title, corrected_frame)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        print("this happened")
        cv2.destroyAllWindows()
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
