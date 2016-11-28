"""
Provides functionality for listing the files of a set directory.
"""
from __future__ import absolute_import, division, print_function
import os

def main():
    """ Lists the directory tree structure of the directory in from the python file was run. """
    list_files(os.getcwd())

def list_files(root_directory):
    """ Lists the directory tree structure, beginning from the root directory. """
    # _directories has a leading _ because it is an intentionally unused variable
    for root, _directories, files in os.walk(root_directory):
        level = root.replace(root_directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for individual_file in files:
            print('{}{}'.format(subindent, individual_file))

if __name__ == "__main__":
    main()
