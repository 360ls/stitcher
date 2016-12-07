"""
Distortion corrector module for providing functionality to correct a distorted image.
"""
import numpy as np
import cv2

def correct_distortion(image):
    """
    This function corrects the distortion of a radially-distorted
    input image based on pre-determined, hard-coded distortion correction parameters.

    These are calibration parameters derived
    from the radial distortion correction calibration.
    For a new set of parameters, run the calibration in the calibrate folder
    and pull the parameters from the program result.

    RMS: 2.40806793018
    camera matrix:
     [[  6.11968871e+02   0.00000000e+00   1.15939403e+03]
     [  0.00000000e+00   6.03873075e+02   8.71465543e+02]
     [  0.00000000e+00   0.00000000e+00   1.00000000e+00]]
    distortion coefficients:  [-0.13851498  0.01500291 -0.00039581 -0.00014884 -0.00065915]
    [-0.13851498  0.01500291  0.          0.          0.        ]

    """
    # camera_matrix = np.array([[6.11968871e+02,
    #                            0, 1.15939403e+03],
    #                           [0, 6.03873075e+02, 8.71465543e+02], [0, 0, 1]])
    # distortion_coefficients = np.array([-0.13851498, 0.01500291, 0, 0, 0])

    camera_matrix = np.array([[857.48296979,
                               0, 968.06224829],
                              [0, 876.71824265, 556.37145899], [0, 0, 1]])
    distortion_coefficients = np.array([-2.57614020e-01, 8.77086999e-02, 0, 0, 0])

    # Correct the radial distortion
    corrected_image = cv2.undistort(image, camera_matrix, distortion_coefficients)

    return corrected_image
