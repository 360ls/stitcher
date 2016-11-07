"""
Utility module responsible for capturing photos and videos for testing and manipulation.
"""
from __future__ import absolute_import, division, print_function
import argparse

def parse_args():
    """
    Returns parsed arguments from command line input.
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