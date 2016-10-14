import numpy as np
import cv2
import imutils

def verify_calibration(camera_matrix, distortion_coefficients):
	"""
	Verifies calibration of a test image based on an incoming camera_matrix and a set of distortion_coefficients pre-determined during calibration. 
	"""

	K = camera_matrix
	d = distortion_coefficients

	# Read in the image for correction
	src = cv2.imread("inputs/104_0009.JPG")
	height, width = src.shape[:2]

	# Correct the radial distortion
	newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (width,height), 0) 
	newimg = cv2.undistort(src, K, d, None, newcamera)

	# Display a comparison between the original image and the corrected image
	cv2.imshow("original", imutils.resize(src, width=720))
	cv2.imshow("corrected", imutils.resize(newimg, width=720))
	cv2.waitKey(0)
	cv2.destroyAllWindows()