"""
This function corrects the distortion on a single frame. For more information on what the individual coefficients do, go to the following link: http://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html
"""

import numpy as np
import cv2

src = cv2.imread("../../data/distortion/distorted.png")
width = src.shape[1]
height = src.shape[0]

distortionCoefficients = np.zeros((4,1),np.float64)

k1 = -1.0e-5;
k2 = 0.0;
p1 = 0.0;
p2 = 0.0;

distortionCoefficients[0,0] = k1;
distortionCoefficients[1,0] = k2;
distortionCoefficients[2,0] = p1;
distortionCoefficients[3,0] = p2;

# assume unit matrix for camera
cam = np.eye(3,dtype=np.float32)

# define center x value
cam[0,2] = width/2.0

# define center y value
cam[1,2] = height/2.0

# define focal length x value
cam[0,0] = 10.

# define focal length y value
cam[1,1] = 10.

# here the undistortion will be computed
dst = cv2.undistort(src,cam,distortionCoefficients)

cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()