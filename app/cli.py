""" Responsible for demonstrating stitching and streaming functionality in the terminal. """
from __future__ import absolute_import, division, print_function
import argparse
import sys
from .util.textformatter import TextFormatter
from .util.inputscanner import InputScanner
from .util.validatefeeds import view_valid_camera_feeds

def main():
    """
    The main script for instantiating a CLI to demonstrate stitching and streaming functionality.
    """
    parsed_args = parse_args()
    if parsed_args.interactive_mode:
        TextFormatter.print_title("Welcome to the 360ls Stitching and Streaming CLI")
        TextFormatter.print_heading("Choose an option to proceed:")
        TextFormatter.print_option(1, "View Stitching and Correction Functionality")
        TextFormatter.print_option(2, "Run Utilities for Setup and Configuration")
        TextFormatter.print_option(0, "Quit")

        scanner = InputScanner()
        selected_option = scanner.read_int('Enter option number: ')
    else:
        # If not in interactive mode, takes option number from input and passes to stitching cli
        stitching_and_streaming(parsed_args.option_num)

    # Responds to user-provided option selection
    if selected_option == 1:
        stitching_and_streaming()
    elif selected_option == 2:
        utilities()
    elif selected_option == 0:
        exit_python()
    else:
        TextFormatter.print_error("Please retry and enter a valid number.")
        main()

def stitching_and_streaming(non_interactive_selected_option=None):
    """
    Provides interaction with application stitching and streaming functionality.
    """
    if non_interactive_selected_option is None:
        TextFormatter.print_title("View current stitching and streaming functionality below.")
        TextFormatter.print_heading("Choose an option to proceed:")
        TextFormatter.print_option(1, "Show Corrected Image - Single Image")
        TextFormatter.print_option(2, "Show Corrected Live Feed - Single Camera")
        TextFormatter.print_option(3, "Show Corrected Live Feed - Two Stiched Cameras")
        TextFormatter.print_option(4, "Show Corrected Live Feed - Four Stitched Cameras")
        TextFormatter.print_option(0, "Quit")

        scanner = InputScanner()
        selected_option = scanner.read_int('Enter option number: ')
    else:
        selected_option = non_interactive_selected_option

    # Responds to user-provided option selection
    if selected_option == 1:
        pass
    elif selected_option == 2:
        pass
    elif selected_option == 3:
        pass
    elif selected_option == 4:
        pass
    elif selected_option == 0:
        exit_python()
    else:
        TextFormatter.print_error("Please retry and enter a valid number.")
        stitching_and_streaming()

def utilities():
    """
    Provides interaction with utilities for demonstrating and testing stitching
    and streaming functionality.
    """
    TextFormatter.print_title("Use one of the useful utility functions below.")
    TextFormatter.print_heading("Choose an option to proceed:")
    TextFormatter.print_option(1, "Calibrate Camera - Single Camera")
    TextFormatter.print_option(2, "Check Camera Feeds - All Available Cameras")
    TextFormatter.print_option(3, "Capture Video - Two Cameras")
    TextFormatter.print_option(4, "Capture Video - Four Cameras")
    TextFormatter.print_option(5, "Take Photos - Two Cameras")
    TextFormatter.print_option(6, "Take Photos - Four Cameras")
    TextFormatter.print_option(0, "Quit")

    scanner = InputScanner()
    selected_option = scanner.read_int('Enter option number: ')

    # Responds to user-provided option selection
    if selected_option == 1:
        TextFormatter.print_title("Calibrate Camera - Single Camera")

    elif selected_option == 2:
        TextFormatter.print_title("Check Camera Views - All Available Cameras")
        view_valid_camera_feeds()
    elif selected_option == 3:
        TextFormatter.print_title("Capture Video - Two Cameras")
    elif selected_option == 4:
        TextFormatter.print_title("Capture Video - Four Cameras")
    elif selected_option == 5:
        TextFormatter.print_title("Take Photos - Two Cameras")
    elif selected_option == 6:
        TextFormatter.print_title("Take Photos - Four Cameras")
    elif selected_option == 0:
        exit_python()
    else:
        TextFormatter.print_error("Please retry and enter a valid number.")
        utilities()

def parse_args():
    """
    Returns parsed arguments from command line.
    """

    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Facilitates interactive mode.")

    # Adds arguments to the parser for interactive mode and options.
    parser.add_argument('-n', action='store_true', default=False,
                        dest='interactive_mode',
                        help='Turns interactive mode on.')
    parser.add_argument('--option', action='store',
                        type=int,
                        dest='option_num',
                        help='Option number for selected stitching and streaming option.')
    return parser.parse_args()

def exit_python():
    """
    Simple helper function for exiting Python
    """
    TextFormatter.print_info("You have chosen to exit the application! Have a great day!\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
