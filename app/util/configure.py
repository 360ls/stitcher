"""
Module responsible for configuration based on instructions in the profile.yml config file.
"""
from __future__ import absolute_import, division, print_function

from .configuration import Configuration
from .textformatter import TextFormatter


def main():
    """
    Responsible for handling configuration call from the command line.
    """
    configure_stitching()

def configure_stitching():
    """
    Responsible for core functionality of configuration from profile.yml.
    """
    configuration = load_profile()

def load_profile():
    """
    Loads profile.yml to get configuration parameters.
    """
    try:
        configuration = Configuration()
        TextFormatter.print_info("Profile is valid and parsed properly.")
        return configuration
    except:
        TextFormatter.print_error("Profile was parsed, but it was invalid.")

if __name__ == "__main__":
    main()
