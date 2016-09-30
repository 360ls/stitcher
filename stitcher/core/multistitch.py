
"""
This module encapsulates the Multistitcher class to enable stitching of multiple images/frames.
"""
#!/usr/bin/python

import os
import sys
import cv2
import math
import numpy as np

from PIL import Image
from numpy import linalg

class Multistitcher:
    """ The Multistitcher class enables stitching of multiple images/frames. """
    def __init__(self, src_dir):
        """ The constructor for the Multistitcher class. """
        self.src_dir = src_dir
        self.cached_homographies = []

    def filter_matches(self, matches, ratio = 0.75):
        """ Filters nearest neighbor matches for computing stitch. """
        filtered_matches = []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                filtered_matches.append(m[0])
        return filtered_matches

    def imageDistance(self, matches):
        """ Computes sum of distances between nearest neighbor matches. """
        sumDistance = 0.0
        for match in matches:
            sumDistance += match.distance
        return sumDistance

    def findDimensions(self, image, homography):
        """ Gets the dimensions of the image based on the calculated homography. """
        base_p1 = np.ones(3, np.float32)
        base_p2 = np.ones(3, np.float32)
        base_p3 = np.ones(3, np.float32)
        base_p4 = np.ones(3, np.float32)

        (y, x) = image.shape[:2]

        base_p1[:2] = [0,0]
        base_p2[:2] = [x,0]
        base_p3[:2] = [0,y]
        base_p4[:2] = [x,y]

        max_x = None
        max_y = None
        min_x = None
        min_y = None

        for pt in [base_p1, base_p2, base_p3, base_p4]:
            hp = np.matrix(homography, np.float32) * np.matrix(pt, np.float32).T
            hp_arr = np.array(hp, np.float32)

            normal_pt = np.array([hp_arr[0]/hp_arr[2], hp_arr[1]/hp_arr[2]], np.float32)

            if ( max_x == None or normal_pt[0,0] > max_x ):
                max_x = normal_pt[0,0]

            if ( max_y == None or normal_pt[1,0] > max_y ):
                max_y = normal_pt[1,0]

            if ( min_x == None or normal_pt[0,0] < min_x ):
                min_x = normal_pt[0,0]

            if ( min_y == None or normal_pt[1,0] < min_y ):
                min_y = normal_pt[1,0]

        min_x = min(0, min_x)
        min_y = min(0, min_y)

        return (min_x, min_y, max_x, max_y)

    def stitchImages(self, key_frame_file, base_img_rgb, dir_list, output, round, img_type):
        """ Primary method for stitching the images together. """
        if ( len(dir_list) < 1 ):
            return base_img_rgb

        base_img = cv2.GaussianBlur(cv2.cvtColor(base_img_rgb,cv2.COLOR_BGR2GRAY), (5,5), 0)
        if (round < len(self.cached_homographies)):
            closestImage = self.cached_homographies[round]
        else:

            # Use the SURF feature detector
            detector = cv2.SURF()

            # Find key points in base image for motion estimation
            base_features, base_descs = detector.detectAndCompute(base_img, None)

            # Parameters for nearest-neighbor matching
            FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
            flann_params = dict(algorithm = FLANN_INDEX_KDTREE, 
                trees = 5)
            matcher = cv2.FlannBasedMatcher(flann_params, {})

            print "Iterating through next images..."

            closestImage = self.getNextImage(detector, matcher, base_descs, base_features, round, img_type)
        new_dir_list = filter(lambda x: x != closestImage['path'], dir_list)

        H = closestImage['h']
        H = H / H[2,2]
        H_inv = linalg.inv(H)

        if ( closestImage['inliers'] > 0.1 ): # and 

            (min_x, min_y, max_x, max_y) = self.findDimensions(closestImage['img'], H_inv)

            # Adjust max_x and max_y by base img size
            max_x = max(max_x, base_img.shape[1])
            max_y = max(max_y, base_img.shape[0])

            move_h = np.matrix(np.identity(3), np.float32)

            if ( min_x < 0 ):
                move_h[0,2] += -min_x
                max_x += -min_x

            if ( min_y < 0 ):
                move_h[1,2] += -min_y
                max_y += -min_y

            print "Homography: \n", H
            print "Inverse Homography: \n", H_inv
            print "Min Points: ", (min_x, min_y)

            mod_inv_h = move_h * H_inv

            img_w = int(math.ceil(max_x))
            img_h = int(math.ceil(max_y))

            print "New Dimensions: ", (img_w, img_h)

            # Warp the new image given the homography from the old image
            base_img_warp = cv2.warpPerspective(base_img_rgb, move_h, (img_w, img_h))
            print "Warped base image"


            next_img_warp = cv2.warpPerspective(closestImage['rgb'], mod_inv_h, (img_w, img_h))
            print "Warped next image"


            # Put the base image on an enlarged palette
            enlarged_base_img = np.zeros((img_h, img_w, 3), np.uint8)

            print "Enlarged Image Shape: ", enlarged_base_img.shape
            print "Base Image Shape: ", base_img_rgb.shape
            print "Base Image Warp Shape: ", base_img_warp.shape

            # Create a mask from the warped image for constructing masked composite
            (ret,data_map) = cv2.threshold(cv2.cvtColor(next_img_warp, cv2.COLOR_BGR2GRAY), 
                0, 255, cv2.THRESH_BINARY)

            enlarged_base_img = cv2.add(enlarged_base_img, base_img_warp, 
                mask=np.bitwise_not(data_map), 
                dtype=cv2.CV_8U)

            # Now add the warped image
            final_img = cv2.add(enlarged_base_img, next_img_warp, 
                dtype=cv2.CV_8U)


            # Crop off the black edges
            final_gray = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(final_gray, 1, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            print "Found %d contours..." % (len(contours))

            max_area = 0
            best_rect = (0,0,0,0)

            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)

                deltaHeight = h-y
                deltaWidth = w-x

                area = deltaHeight * deltaWidth

                if ( area > max_area and deltaHeight > 0 and deltaWidth > 0):
                    max_area = area
                    best_rect = (x,y,w,h)

            if ( max_area > 0 ):
                print "Maximum Contour: ", max_area
                print "Best Rectangle: ", best_rect

                final_img_crop = final_img[best_rect[1]:best_rect[1]+best_rect[3],
                        best_rect[0]:best_rect[0]+best_rect[2]]


                final_img = final_img_crop

            # Write out the current round
            final_filename = "%s/%d." % (output, round)
            final_filename = final_filename + img_type
            cv2.imwrite(final_filename, final_img)

            return self.stitchImages(key_frame_file, final_img, new_dir_list, output, round+1, img_type)

        else:

            return self.stitchImages(key_frame_file, base_img_rgb, new_dir_list, output, round+1, img_type)

    def getNextImage(self, detector, matcher, base_descs, base_features,  round, format):
            """ Pulls in the next image for processing. """

            next_img_path = "{2}/{0}.{1}".format(round+1, format, self.src_dir)
            print "Reading %s..." % next_img_path

            # Read in the next image...
            next_img_rgb = cv2.imread(next_img_path)
            next_img = cv2.GaussianBlur(cv2.cvtColor(next_img_rgb,cv2.COLOR_BGR2GRAY), (5,5), 0)

            print "\t Finding points..."

            # Find points in the next frame
            next_features, next_descs = detector.detectAndCompute(next_img, None)

            matches = matcher.knnMatch(next_descs, trainDescriptors=base_descs, k=2)

            print "\t Match Count: ", len(matches)

            matches_subset = self.filter_matches(matches)

            print "\t Filtered Match Count: ", len(matches_subset)

            distance = self.imageDistance(matches_subset)

            print "\t Distance from Key Image: ", distance

            averagePointDistance = distance/float(len(matches_subset))

            print "\t Average Distance: ", averagePointDistance

            kp1 = []
            kp2 = []

            for match in matches_subset:
                            kp1.append(base_features[match.trainIdx])
                            kp2.append(next_features[match.queryIdx])

            p1 = np.array([k.pt for k in kp1])
            p2 = np.array([k.pt for k in kp2])

            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
            print '%d / %d  inliers/matched' % (np.sum(status), len(status))

            inlierRatio = float(np.sum(status)) / float(len(status))

            closestImage = {}
            closestImage['h'] = H
            closestImage['inliers'] = inlierRatio
            closestImage['dist'] = averagePointDistance
            closestImage['path'] = next_img_path
            closestImage['rgb'] = next_img_rgb
            closestImage['img'] = next_img
            closestImage['feat'] = next_features
            closestImage['desc'] = next_descs
            closestImage['match'] = matches_subset

            if len(self.cached_homographies) <= round:
                self.cached_homographies.append(closestImage)

            print "Closest Image: ", closestImage['path']
            print "Closest Image Ratio: ", closestImage['inliers']
            return closestImage

    def resizeImages(self, dir_list, dir_name, width):
        """ Resizes images to cut down on computation time. """
        
        width = int(width)
        for i in range(len(dir_list)):
            print "Resizing image: ", dir_list[i]
            imTemp = Image.open(dir_list[i])
            wPercent = (width/float(imTemp.size[0]))
            height = int((float(imTemp.size[1]) * float(wPercent)))
            imTemp = imTemp.resize((width, height), Image.BILINEAR)
            imTemp.save(os.path.join(dir_name, dir_list[i]))
