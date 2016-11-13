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
    num_cameras = parsed_args.num_cameras
    camera_index = parsed_args.camera_index

    if capture_type == "frame":
        if num_cameras == 1:
            capture_camera_frames("out/captured_frames", "jpg", 0)
        elif num_cameras == 2:
            capture_camera_frames("out/captured_frames", "jpg", 1, 2)
        elif num_cameras == 4:
            capture_camera_frames("out/captured_frames", "jpg", 1, 2, 3, 4)
    elif capture_type == "video":
        if num_cameras == 1:
            if camera_index is not 0:
                capture_single_video(camera_index, 5)
            else:
                capture_single_video(camera_index, 5, 12)
        else:
            TextFormatter.print_info("You chose to capture video for %s cameras." % num_cameras)
    else:
        TextFormatter.print_error("Please provide a proper capture argument.")

def capture_single_video(index=0, duration=5, fps=30, output_dir="out/captured_videos",
                         filetype="avi"):
    """
    Ramps up camera provided by index and captures video for provided capture_duration (in sec).
    """
    camera_feed = CameraFeed(index)
    camera_feed.ramp(fps)
    filepath = create_filepath(output_dir, filetype)

    writer = None
    (height, width) = (None, None)

    start_time = time.time()
    while time.time() < start_time + duration:
        frame = camera_feed.get_next(True, False)
        if writer is None:
            (height, width) = frame.shape[:2]
            writer = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*"MJPG"),
                                     fps, (width, height))
        writer.write(frame)

    writer.release()
    camera_feed.close()

    TextFormatter.print_info("Video was captured for %s seconds." % duration)

def capture_camera_frames(output_dir="out/captured_frames", filetype="jpg", *feed_indices):
    """
    Ramps up cameras provided by index and captures a single frame from each for testing.
    """

    # Creates CameraFeeds for the provided indices and adds them to a list.
    camera_feed_list = []
    frame_list = []

    for feed_index in feed_indices: # Makes sure that the xrange function is available
        camera_feed = CameraFeed(feed_index)
        camera_feed_list.append(camera_feed)

    # Ramps up the available cameras.
    for camera_feed in camera_feed_list:
        TextFormatter.print_info("Camera feed ramped and read.")
        camera_feed.ramp()
        if camera_feed.has_next():
            frame = camera_feed.get_next(True, False)
        camera_feed.close()
        frame_list.append(frame)

    frame_counter = 1
    for frame in frame_list:
        TextFormatter.print_info("Filepath created.")
        filepath = create_filepath(output_dir, filetype, "%s--" % frame_counter)
        print(filepath)
        cv2.imwrite(filepath, frame)
        frame_counter += 1

    TextFormatter.print_info("Frames were captured and saved.")

def create_filepath(output_folder, filetype, prefix=""):
    """
    Creates a filepath for output of captured data based on timestamp.
    """
    timestamp = datetime.datetime.now()
    filename = "{}.{}".format(timestamp.strftime("%Y-%m-%d-%H-%M-%S"), filetype)
    filename = "%s%s" % (prefix, filename)
    filepath = os.path.sep.join((output_folder, filename))
    return filepath


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
    parser.add_argument("--cameras", action="store", default=1,
                        type=int,
                        dest="num_cameras",
                        help="Number of cameras.")
    parser.add_argument("--index", action="store", default=0,
                        type=int,
                        dest="camera_index",
                        help="Index of camera.")
    return parser.parse_args()

if __name__ == "__main__":
    main()
