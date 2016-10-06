"""
Scanner module
"""

import os
from .formatter import Formatter

class Scanner(object):
    """
    Scanner for reading user input
    """
    @staticmethod
    def read_int(prompt):
        """
        reads an integer from standard input
        """
        try:
            num_input = int(raw_input(Formatter.get_input_msg(prompt)))
            print ""
            return num_input
        except ValueError:
            print "Please enter a number."

    @staticmethod
    def read_dir(prompt):
        """
        reads a directory from standard input
        """
        directory = raw_input(Formatter.get_input_msg(prompt))
        if os.path.isdir(directory):
            return directory
        else:
            raise ValueError

    @staticmethod
    def read_string(prompt):
        """
        reads a string from standard input
        """
        string = raw_input(Formatter.get_input_msg(prompt))
        return string
