""" Responsible for demonstrating stitching and streaming functionality in the terminal. """
from __future__ import print_function
import argparse
from .util.textformatter import TextFormatter

def main():
    """
    The main script for instantiating a CLI to demonstrate stitching and streaming functionality.
    """

    parsed_args = parse_args()
    if not parsed_args.interactive_mode:
        TextFormatter.print_title("Welcome to the 360ls Stitching and Streaming CLI")
        TextFormatter.print_heading("Choose an option to proceed:")
        TextFormatter.print_option(1, "View Stitching and Correction Functionality")
        TextFormatter.print_option(2, "Run Utilities for Setup and Configuration")
        TextFormatter.print_option(0, "Quit")
    else:
        option = parsed_args.option_num

def stitching_and_streaming():
    """
    Provides interaction with application stitching and streaming functionality.
    """
    TextFormatter.print_title("View current stitching and streaming functionality below.")
    TextFormatter.print_heading("Choose an option to proceed:")
    TextFormatter.print_option(1, "Show Corrected Image - Single Image")
    TextFormatter.print_option(2, "Show Corrected Live Feed - Single Camera")
    TextFormatter.print_option(3, "Show Corrected Live Feed - Two Stiched Cameras")
    TextFormatter.print_option(4, "Show Corrected Live Feed - Four Stitched Cameras")
    TextFormatter.print_option(0, "Quit")

def parse_args():
    """
    Returns parsed arguments from command line.
    """

    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Facilitates interactive mode.")

    # Adds arguments to the parser for interactive mode and options.
    parser.add_argument('-n', action='store_false', default=True,
                        dest='interactive_mode',
                        help='Turns interactive mode on.')
    parser.add_argument('--option', action='store',
                        type=int,
                        dest='option_num',
                        help='Option number for selected stitching and streaming option.')
    return parser.parse_args()

if __name__ == "__main__":
    main()
