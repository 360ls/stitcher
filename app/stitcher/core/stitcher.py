
"""
This module encapsulates the Stitcher class to enable stitching of images/frames.
"""
from __future__ import absolute_import, division, print_function

import numpy as np
import imutils
import cv2

class Stitcher(object):
    """ Creates a single stitched frame from two frames """

    def __init__(self):
        """ Initializes homography matrix and checks opencv version """
        self.isv3 = imutils.is_cv3()
        self.homography = None

    def stitch(self, frame1, frame2):
        """
        Responsible for computing homography for and warping images.
        Returns a stitched composition of frame1 and frame2.
        """
        if self.homography is None:
            self.homography = compute_homography(frame1, frame2)

        if self.homography is not False:
            result = warp_images(frame2, frame1, self.homography)
            return result

        return None

    def show_stitch(self, frame1, frame2):
        """
        Responsible for showing a stitch
        """
        result = self.stitch(frame1, frame2)
        if result is not None:
            cv2.imshow('Stitched output', result)
            cv2.waitKey()

    def reset(self):
        """
        Resets the homography of the stitcher to None for stitcher reuse.
        """
        self.homography = None

    def double_stitch(self, img1, img2, img3): # pylint: disable=unused-argument, no-self-use
        """
        TODO: Not implemented
        """
        raise Exception('Not implemented')

def compute_matches(frame1, frame2):
    """
    Computes the keypoint matches between the provided frames.
    """

    # Initialize the SURF detector
    surf = cv2.xfeatures2d.SURF_create()

    # Extracts the keypoints and descriptors via SURF
    keypoints1, descriptors1 = surf.detectAndCompute(frame1, None)
    keypoints2, descriptors2 = surf.detectAndCompute(frame2, None)

    # Initializes parameters for Flann-based matcher
    flann_index_kdtree = 0
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)

    # Initializes the Flann-based matcher object
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Computes matches using Flann matcher
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    return matches, keypoints1, keypoints2

def compute_homography(frame1, frame2):
    """
    Computes homography based on the provided frames.
    """
    min_match_count = 20
    matches, keypoints1, keypoints2 = compute_matches(frame1, frame2)

    # Store all the good matches based on Lowes ratio test
    good_matches = []
    for match1, match2 in matches:
        if match1.distance < 0.7 * match2.distance:
            good_matches.append(match1)

    if len(good_matches) > min_match_count:
        # TextFormatter.print_info("Found %d matches. We need at least %d matches."
        #                          % (len(good_matches), min_match_count))
        src_pts = np.float32([keypoints1[good_match.queryIdx].pt
                              for good_match in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[good_match.trainIdx].pt
                              for good_match in good_matches]).reshape(-1, 1, 2)

        homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return homography
    else:
        # TextFormatter.print_error("Images do not have enough matches to produce homography.")
        # TextFormatter.print_info("Found %d matches. We need at least %d matches."
        #                          % (len(good_matches), min_match_count))
        return False

def warp_images(img1, img2, homography):
    """
    Warps second image to plane of first image based on provided homography.
    """
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    point_list1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    temp_points = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)
    point_list2 = cv2.perspectiveTransform(temp_points, homography)
    combined_point_list = np.concatenate((point_list1, point_list2), axis=0)

    [x_min, y_min] = np.int32(combined_point_list.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(combined_point_list.max(axis=0).ravel() + 0.5)
    translation_dist = [-x_min, -y_min]
    homography_translation = np.array([[1, 0, translation_dist[0]],
                                       [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(img2, homography_translation.dot(homography), # pylint: disable=no-member
                                     (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1],
               translation_dist[0]:cols1+translation_dist[0]] = img1

    return output_img
