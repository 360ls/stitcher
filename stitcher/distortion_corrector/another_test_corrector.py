#!/usr/bin/python

# ./undistort 0_0000.jpg 1367.451167 1367.451167 0 0 -0.246065 0.193617 -0.002004 -0.002056

import sys
import cv2

def main(argv):
    if len(argv) < 10:
        print('Usage: %s input-file fx fy cx cy k1 k2 p1 p2 output-file' % argv[0])
        sys.exit(-1)

    src = argv[1]
    fx, fy, cx, cy, k1, k2, p1, p2, output = argv[2:]

    intrinsics = cv2.CreateMat(3, 3, cv2.cv2_64FC1)
    cv2.Zero(intrinsics)
    intrinsics[0, 0] = float(fx)
    intrinsics[1, 1] = float(fy)
    intrinsics[2, 2] = 1.0
    intrinsics[0, 2] = float(cx)
    intrinsics[1, 2] = float(cy)

    dist_coeffs = cv2.CreateMat(1, 4, cv2.cv2_64FC1)
    cv2.Zero(dist_coeffs)
    dist_coeffs[0, 0] = float(k1)
    dist_coeffs[0, 1] = float(k2)
    dist_coeffs[0, 2] = float(p1)
    dist_coeffs[0, 3] = float(p2)

    src = cv2.LoadImage(src)
    dst = cv2.CreateImage(cv2.GetSize(src), src.depth, src.nChannels)
    mapx = cv2.CreateImage(cv2.GetSize(src), cv2.IPL_DEPTH_32F, 1)
    mapy = cv2.CreateImage(cv2.GetSize(src), cv2.IPL_DEPTH_32F, 1)
    cv2.InitUndistortMap(intrinsics, dist_coeffs, mapx, mapy)
    cv2.Remap(src, dst, mapx, mapy, cv2.cv2_INTER_LINEAR + cv2.cv2_WARP_FILL_OUTLIERS,  cv2.ScalarAll(0))
    # cv2.Undistort2(src, dst, intrinsics, dist_coeffs)

    cv2.SaveImage(output, dst)


if __name__ == '__main__':
    main(sys.argv)