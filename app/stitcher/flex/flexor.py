""" Module for handling response to invalid incoming camera feed. """

from __future__ import absolute_import, division, print_function

import cv2
import numpy as np

from app.util.feed import VideoFeed
from app.util.textformatter import TextFormatter

def main():
    """
    Runs an example of checking the main color of a video feed.
    """
    video = VideoFeed("app/storage/flex/naiveflex.mp4")
    if video.is_valid():
        while video.has_next():
            frame = video.get_next(True, False)
            average_frame_color = get_average_color(frame)
            zero_array = np.array([0, 0, 0])

            if np.array_equal(average_frame_color, zero_array):
                TextFormatter.print_error("Invalid frame.")
            else:
                # TextFormatter.print_info(get_average_color(frame))
                TextFormatter.print_info("Valid frame.")

            title = "Flex Video Feed"
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        TextFormatter.print_info("Cleaning up video feed.")
        video.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

def get_average_color(frame):
    """ Returns the average color of the provided frame. """

    # Computes average color for each row in frame.
    average_row_colors = np.average(frame, axis=0)

    # Computes the average of the average row colors
    average_frame_color_raw = np.average(average_row_colors, axis=0)

    # Converts average frame color to uint8 form for true color match
    average_frame_color = np.uint8(average_frame_color_raw)

    return average_frame_color

if __name__ == "__main__":
    main()
