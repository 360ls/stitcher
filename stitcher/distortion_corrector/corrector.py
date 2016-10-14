import numpy as np
import cv2
import imutils

def correct_distortion(image):
	"""
	This function corrects the distortion of a radially-distorted input image based on pre-determined, hard-coded distortion correction parameters.
	"""
	
	"""
	These are calibration parameters derived from the radial distortion correction calibration. For a new set of parameters, run the calibration in the calibrate folder and pull the parameters from the program result.
	"""
	camera_matrix = np.array([[5.37986935e+02, 0, 1.14161919e+03], [0, 5.37766809e+02, 8.73291935e+02], [0, 0, 1]])
	distortion_coefficients = np.array([-0.11199349, 0.0096919, 0, 0, 0])

	# Read in the image for correction
	src = cv2.imread(image)
	height, width = src.shape[:2]

	# Correct the radial distortion
	new_camera, roi = cv2.getOptimalNewCameraMatrix(K, d, (width,height), 0) 
	corrected_image = cv2.undistort(src, K, d, None, new_camera)

	return corrected_image