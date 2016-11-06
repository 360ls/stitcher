"""
Module for reading user input from the command line.
"""

from __future__ import absolute_import, division, print_function
import os
from .textformatter import TextFormatter

class InputScanner(object):
    """
    Scanner reads user input from the command line.
    """
    @staticmethod
    def read_int(prompt):
        """
        Reads an integer from standard input.
        """
        try:
            num_input = int(raw_input(TextFormatter.get_input_msg(prompt)))
            TextFormatter.print_new_line()
            return num_input
        except ValueError:
            TextFormatter.print_error("Please retry and enter a valid number.")

    @staticmethod
    def read_dir(prompt):
        """
        reads a directory from standard input
        """
        directory = raw_input(TextFormatter.get_input_msg(prompt))
        if os.path.isdir(directory):
            return directory
        else:
            raise ValueError

    @staticmethod
    def read_string(prompt):
        """
        reads a string from standard input
        """
        string = raw_input(TextFormatter.get_input_msg(prompt))
        return string
