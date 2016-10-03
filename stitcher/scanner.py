"""
Scanner module
"""

import os

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
            num_input = int(raw_input(prompt))
            print ""
            return num_input
        except ValueError:
            print "Please enter a number."

    @staticmethod
    def read_dir(prompt):
        """
        reads a directory from standard input
        """
        directory = raw_input(prompt)
        if os.path.isdir(directory):
            return directory
        else:
            raise ValueError
