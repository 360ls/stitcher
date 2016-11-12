"""
Utility module responsible for capturing photos and videos for testing and manipulation.
"""
from __future__ import absolute_import, division, print_function
import argparse
import datetime
import time
import os
import cv2
from .textformatter import TextFormatter
from .feed import CameraFeed


def main():
    """
    Determines capture type based on parsed args and runs capture.
    """
    parsed_args = parse_args()
    capture_type = parsed_args.capture_type
    if capture_type == "frame":
        capture_frame()
    elif capture_type == "video":
        capture_video()
    else:
        TextFormatter.print_error("Please provide a proper capture argument.")

def capture_frame(feed_index=0):
    """
    Ramps up available camera and captures a single frame for testing.
    """
    camera_feed = CameraFeed(feed_index)
    camera_feed.ramp()
    frame = camera_feed.get_next()

    output_folder_path = "out/captured_frames/"
    timestamp = datetime.datetime.now()
    filename = "{}.jpg".format(timestamp.strftime("%Y-%m-%d-%H-%M-%S"))
    filepath = os.path.sep.join((output_folder_path, filename))

    cv2.imwrite(filepath, frame)
    TextFormatter.print_info("Frame was captured.")

    camera_feed.close()

def capture_video(feed_index=0, capture_duration=5, fps=30, filepath="out/"):
    """
    Ramps up available camera and captures video for provided capture_duration (in sec).
    """
    camera_feed = CameraFeed(feed_index)
    camera_feed.ramp(fps)
    start_time = time.time()

    output_folder_path = "out/captured_videos/"
    timestamp = datetime.datetime.now()
    filename = "{}.avi".format(timestamp.strftime("%Y-%m-%d-%H-%M-%S"))
    filepath = os.path.sep.join((output_folder_path, filename))

    writer = None
    (height, width) = (None, None)

    while time.time() < start_time + capture_duration:
        frame = camera_feed.get_next()
        if writer is None:
            (height, width) = frame.shape[:2]
            writer = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc('I', '4', '2', '0'),
                                     fps, (width, height))
        writer.write(frame)

    writer.release()

    camera_feed.close()

    TextFormatter.print_info("Video was captured for %s seconds." % capture_duration)

def capture_four_camera_frames():
    """
    Ramps up available cameras and captures a single frame from each for testing.
    """

    # Creates CameraFeeds for the provided indices and adds them to a list.
    camera_feed_list = []

    try:
        for feed_index in xrange(1, 4): # Makes sure that the xrange function is available
            camera_feed = CameraFeed(feed_index)
            camera_feed_list.append(camera_feed)
    except NameError:
        for feed_index in range(1, 4):
            camera_feed = CameraFeed(feed_index)
            camera_feed_list.append(camera_feed)

    # Ramps up the available cameras.
    for camera_feed in camera_feed_list:
        camera_feed.ramp()



    # success0 = cameraCapture0.grab()
    # success1 = cameraCapture1.grab()
    # if success0 and success1:
    #     frame0 = cameraCapture0.retrieve()
    #     frame1 = cameraCapture1.retrieve()



def parse_args():
    """
    Returns parsed arguments from command line input.
    """

    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Determines type of capture.")

    # Adds arguments to the parser for interactive mode and options.
    parser.add_argument("--type", action="store", default="frame",
                        type=str,
                        dest="capture_type",
                        help="Type of capture.")
    return parser.parse_args()

if __name__ == "__main__":
    main()
