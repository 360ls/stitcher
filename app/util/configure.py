"""
Module responsible for configuration based on instructions in the profile.yml config file.
"""
from __future__ import absolute_import, division, print_function

from .configuration import Configuration
from .textformatter import TextFormatter


def main():
    """
    Responsible for loading and printing standard configuration.
    """
    get_configuration()

def get_configuration(config_profile="config/profile.yml"):
    """
    Loads profile.yml to get configuration parameters.
    """
    try:
        configuration = Configuration(config_profile)
        TextFormatter.print_info("Profile is valid and parsed properly.")
        return configuration.get()
    except ValueError:
        TextFormatter.print_error("Profile was parsed, but it was invalid.")

if __name__ == "__main__":
    main()
