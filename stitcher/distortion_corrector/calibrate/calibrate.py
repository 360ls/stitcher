#!/usr/bin/env python

'''
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images

usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]

default values:
    --debug:    ./output/
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

from __future__ import print_function
import numpy as np
import cv2
import os
import sys
import getopt
from glob import glob
from verify_calibration import verify_calibration

def main():
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
    h, w = 0, 0
    img_names_undistort = []
    for fn in img_names:
        print('processing %s... ' % fn, end='')
        img = cv2.imread(fn, 0)
        if img is None:
            print("Failed to load", fn)
            continue

        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        # if debug_dir:
        #     vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        #     cv2.drawChessboardCorners(vis, pattern_size, corners, found)
        #     path, name, ext = splitfn(fn)
        #     outfile = debug_dir + name + '_chess.png'
        #     cv2.imwrite(outfile, vis)
        #     if found:
        #         img_names_undistort.append(outfile)

        if not found:
            print('Chessboard not found.')
            continue

        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print('ok')

    # calculate camera distortion
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())
    # K = np.array([[5.37986935e+02, 0, 1.14161919e+03], [0, 5.37766809e+02, 8.73291935e+02], [0, 0, 1]])
    # d = np.array([-0.11199349, 0.0096919, 0, 0, 0]) # just use first two terms (no translation)
    dist_coefs = dist_coefs.ravel()
    for i in range(3):
        i = i+2
        dist_coefs[i] = 0
    print(dist_coefs)
    verify_calibration(camera_matrix, dist_coefs)
    cv2.destroyAllWindows()

def splitfn(fn):
    path, fn = os.path.split(fn)
    name, ext = os.path.splitext(fn)
    return path, name, ext

if __name__ == "__main__":
    main()

