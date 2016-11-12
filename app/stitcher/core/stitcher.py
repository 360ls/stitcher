
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
        """ Initializes homography matrix and opencv version """

        # determine if we are using OpenCV v3.X and initialize the
        # cached homography matrix
        self.isv3 = imutils.is_cv3()
        self.cached_homography = None

    def stitch(self, images, ratio=0.75, reproj_thresh=4.0):
        """ Primary method for stitching images together within the Stitcher class. """
        # unpack the images
        (image_b, image_a) = images

        # if the cached homography matrix is None, then we need to
        # apply keypoint matching to construct it
        if self.cached_homography is None:
            # detect keypoints and extract
            (kps_a, features_a) = self.detect_and_describe(image_a)
            (kps_b, features_b) = self.detect_and_describe(image_b)

            # match features between the two images
            match = self.match_keypoints(kps_a, kps_b,
                                         features_a, features_b, ratio, reproj_thresh)

            # if the match is None, then there aren't enough matched
            # keypoints to create a panorama
            if match is None:
                return None

            # cache the homography matrix
            self.cached_homography = match[1]

        # apply a perspective transform to stitch the images together
        # using the cached homography matrix
        result = cv2.warpPerspective(image_a, self.cached_homography,
                                     (image_a.shape[1] + image_b.shape[1], image_a.shape[0]))
        result[0:image_b.shape[0], 0:image_b.shape[1]] = image_b

        # return the stitched image
        return result

    def detect_and_describe(self, image):
        """ Detects keypoints from image and extracts features from the keypoints """

        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we are using OpenCV 3.X
        if self.isv3:
            # detect and extract features from the image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)

        # otherwise, we are using OpenCV 2.4.X
        else:
            # detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)

            # extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        kps = np.float32([kp.pt for kp in kps])

        # return a tuple of keypoints and features
        return (kps, features)

    # pylint: disable=too-many-arguments
    # pylint: disable=R0914
    @staticmethod
    def match_keypoints(kps_a, kps_b, features_a, features_b,
                        ratio, reproj_thresh):
        """ Computes keypoint matches and homography matrix based on those matches. """

        # compute the raw matches and initialize the list of actual
        # matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        raw_matches = matcher.knnMatch(features_a, features_b, 2)
        matches = []

        # loop over the raw matches
        for match in raw_matches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(match) == 2 and match[0].distance < match[1].distance * ratio:
                matches.append((match[0].trainIdx, match[0].queryIdx))

        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            pts_a = np.float32([kps_a[i] for (_, i) in matches])
            pts_b = np.float32([kps_b[i] for (i, _) in matches])

            # compute the homography between the two sets of points
            (homography, status) = cv2.findHomography(pts_a, pts_b, cv2.RANSAC,
                                                      reproj_thresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, homography, status)

        # otherwise, no homograpy could be computed
        return None
