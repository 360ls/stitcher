"""
This module encapsulates the Stitcher class to enable stitching of images/frames.
"""

# import the necessary packages
import numpy as np
import imutils
import cv2

class Stitcher:
    def __init__(self):
        """ Constructor for the Stitcher class. Initializes cached homography matrix and checks version of OpenCV. """

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
            (kpsA, features_a) = self.detectAndDescribe(image_a)
            (kpsB, features_b) = self.detectAndDescribe(image_b)

            # match features between the two images
            M = self.matchKeypoints(kpsA, kpsB,
                    features_a, features_b, ratio, reproj_thresh)

            # if the match is None, then there aren't enough matched
            # keypoints to create a panorama
            if M is None:
                return None

            # cache the homography matrix
            self.cached_homography = M[1]

        # apply a perspective transform to stitch the images together
        # using the cached homography matrix
        result = cv2.warpPerspective(image_a, self.cached_homography,
                                     (image_a.shape[1] + image_b.shape[1], image_a.shape[0]))
        result[0:image_b.shape[0], 0:image_b.shape[1]] = image_b

        # return the stitched image
        return result

    def detectAndDescribe(self, image):
        """ Detects keypoints in the image and extracts features from the image based on those keypoints. """

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

    def matchKeypoints(self, kpsA, kpsB, features_a, features_b, 
                       ratio, reproj_thresh):
        """ Computes keypoint matches and homography matrix based on those matches. """

        # compute the raw matches and initialize the list of actual
        # matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(features_a, features_b, 2)
        matches = []

        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                             reproj_thresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, H, status)

        # otherwise, no homograpy could be computed
        return None