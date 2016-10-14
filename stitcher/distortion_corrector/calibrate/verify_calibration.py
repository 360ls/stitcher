def verify_calibration(camera_matrix, distortion_coefficients):
	import numpy as np
	import cv2
	import imutils

	# copy parameters to arrays
	K = camera_matrix
	d = distortion_coefficients

	# read one of your images
	src = cv2.imread("inputs/104_0009.JPG")
	height, width = src.shape[:2]

	# undistort
	newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (width,height), 0) 
	newimg = cv2.undistort(src, K, d, None, newcamera)

	cv2.imshow("original", imutils.resize(src, width=720))
	cv2.imshow("corrected", imutils.resize(newimg, width=720))
	cv2.waitKey(0)
	cv2.destroyAllWindows()