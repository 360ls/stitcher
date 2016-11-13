#!/usr/bin/env python

"""
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images

usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]

default values:
    --debug:    ./output/
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
"""

from __future__ import print_function
import os
import sys
import getopt
from glob import glob
import numpy as np
import cv2
import imutils

# pylint: disable=R0914
def main():
    """
    Calibration routine
    """
    args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size='])
    args = dict(args)
    args.setdefault('--debug', './output/')
    args.setdefault('--square_size', 1.0)
    if not img_mask:
        img_mask = 'inputs/*'
    else:
        img_mask = img_mask[0]

    img_names = glob(img_mask)
    debug_dir = args.get('--debug')
    if not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)
    square_size = float(args.get('--square_size'))

    pattern_size = (9, 6)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    height, width = 0, 0
    for filename in img_names:
        print('processing %s... ' % filename, end='')
        img = cv2.imread(filename, 0)
        if img is None:
            print("Failed to load", filename)
            continue

        height, width = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if not found:
            print('Chessboard not found.')
            continue

        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print('ok')

    # calculate camera distortion
    rms, camera_matrix, dist_coefs, _, _ = cv2.calibrateCamera(obj_points,
                                                               img_points,
                                                               (width, height),
                                                               None, None)

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())

    dist_coefs = dist_coefs.ravel()
    for i in range(3):
        i = i+2
        dist_coefs[i] = 0
    print(dist_coefs)
    verify_calibration(camera_matrix, dist_coefs)
    cv2.destroyAllWindows()

def splitfilename(filename):
    """
    splits file name into parent directory, name and extension
    """
    path, filename = os.path.split(filename)
    name, ext = os.path.splitext(filename)
    return path, name, ext

if __name__ == "__main__":
    main()

def verify_calibration(camera_matrix, distortion_coefficients):
    """
    Verifies calibration of a test image
    based on an incoming camera_matrix and a
    set of distortion_coefficients pre-determined during calibration.
    """

    # Read in the image for correction
    src = cv2.imread("inputs/104_0009.JPG")
    height, width = src.shape[:2]

    # Correct the radial distortion
    newcamera, _ = cv2.getOptimalNewCameraMatrix(camera_matrix,
                                                 distortion_coefficients,
                                                 (width, height), 0)
    newimg = cv2.undistort(src, camera_matrix, distortion_coefficients, None, newcamera)

    # Display a comparison between the original image and the corrected image
    cv2.imshow("original", imutils.resize(src, width=720))
    cv2.imshow("corrected", imutils.resize(newimg, width=720))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
