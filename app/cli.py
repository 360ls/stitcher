""" Responsible for demonstrating stitching and streaming functionality in the terminal. """
from __future__ import print_function
import argparse
from util.textformatter import TextFormatter

def main():
    """
    The main script for instantiating a CLI to demonstrate stitching and streaming functionality.
    """

    parsed_args = parse_args()
    if not parsed_args.interactive_mode:
        TextFormatter.print_heading("Choose an option to proceed:")
        Formatter.print_option(0, "Quit")
        Formatter.print_option(1, "Reconfigure Profile")
        Formatter.print_option(2, "Stitch from cameras")
        Formatter.print_option(3, "Stitch from 2 videos")
        Formatter.print_option(4, "Stitch from 4 videos")
        Formatter.print_option(5, "Stream stitched video")
        Formatter.print_option(6, "Stream validation")
        Formatter.print_option(7, "Stitch from 2 corrected videos")
        Formatter.print_option(8, "Stitch from 2 corrected cameras")
        scanner = Scanner()
        opt = scanner.read_int('Enter option number: ')
    else:
        opt = parsed_args.option_num



    return



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
