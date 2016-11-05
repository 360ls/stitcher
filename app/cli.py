""" Responsible for demonstrating stitching and streaming functionality in the terminal. """
from __future__ import print_function
import argparse
import cv2

def main():
    """
    The main script for instantiating a CLI to demonstrate stitching and streaming functionality.
    """
    return



def parse_args():
    """
    Returns parsed arguments from command line.
    """
    # Opens up an argument parser.
    parser = argparse.ArgumentParser(description="Facilitates interactive mode.")

    # adds the 
    parser.add_argument('-n', action='store_true', default=False,
                        dest='interactive_mode',
                        help='Turns interactive mode off.')
    parser.add_argument('--option', action='store',
                        type=int,
                        dest='option_num',
                        help='Option number')
    return parser.parse_args()

if __name__ == "__main__":
    main()
