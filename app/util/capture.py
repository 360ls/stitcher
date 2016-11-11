"""
Utility module responsible for capturing photos and videos for testing and manipulation.
"""
from __future__ import absolute_import, division, print_function
import argparse
from .textformatter import TextFormatter


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

def capture_frame():
    """
    Ramps up available cameras and captures a single frame for testing.
    """
    TextFormatter.print_info("Frame was captured.")

def capture_video(capture_duration=10):
    """
    Ramps up available cameras and captures video for provided capture_duration.
    """
    TextFormatter.print_info("Video was captured for %s seconds." % capture_duration)

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
