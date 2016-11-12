"""
Module for demonstrating stitch of two images using a Flann-based keypoint matcher
and homography-driven image warp.
"""

import cv2
import numpy as np
import imutils

def main():
    """
    Responsible for 
    """
    img1 = cv2.imread("app/storage/earth1.jpg")
    img2 = cv2.imread("app/storage/earth2.jpg")
    img1 = imutils.resize(img1, 400)
    img2 = imutils.resize(img2, 400)

    cv2.imshow('Image 1', img1)
    cv2.imshow('Image 2', img2)

    homography = compute_homography(img1, img2)

    if homography is not False:
        result = warpImages(img2, img1, homography)
        cv2.imshow('Stitched output', result)
        cv2.waitKey()


def compute_homography(frame1, frame2):
    """ Computes the homography based on the provided frames. """

    # Initialize the SIFT detector
    min_match_count = 60
    sift = cv2.xfeatures2d.SIFT_create()

    # Extract the keypoints and descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(frame1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(frame2, None)

    # Initialize parameters for Flann based matcher
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    # Initialize the Flann based matcher object
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Compute the matches
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Store all the good matches as per Lowe's ratio test
    good_matches = []
    for m1,m2 in matches:
        if m1.distance < 0.7*m2.distance:
            good_matches.append(m1)

    if len(good_matches) > min_match_count:
        src_pts = np.float32([keypoints1[good_match.queryIdx].pt for good_match in good_matches]).reshape(-1,1,2)
        dst_pts = np.float32([keypoints2[good_match.trainIdx].pt for good_match in good_matches]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return M
    else:
        print "We don't have enough number of matches between the two images."
        print "Found only %d matches. We need at least %d matches." % (len(good_matches), min_match_count)
        return False


# Warp img2 to img1 using the homography matrix H
def warpImages(img1, img2, H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0,0], [0,rows1], [cols1,rows1], [cols1,0]]).reshape(-1,1,2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)
    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)
    list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
    translation_dist = [-x_min,-y_min]
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0,0,1]])

    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1
    
    return output_img

if __name__=='__main__':
    main()
