from app.stitcher.core.stitcher import Stitcher
import cv2

def main():
    test_stitcher()

def test_stitcher():
    img1 = cv2.imread("app/storage/stitch_tester/yard1.jpg")
    img2 = cv2.imread("app/storage/stitch_tester/yard2.jpg")
    stitcher = Stitcher()

    cv2.imshow(stitcher.stitch([img1, img2]))
    cv2.waitKey()

if __name__ == "__main__":
    main()



