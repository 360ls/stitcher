"""
Module responsible for configuration based on instructions in the profile.yml config file.
"""
from __future__ import absolute_import, division, print_function

import sys

from .configuration import Configuration
from .textformatter import TextFormatter


def main():
    """
    Responsible for handling configuration call from the command line.
    """
    configuration = load_profile()
    configure_stitching(configuration)

def configure_stitching(configuration):
  """
  Responsible for core functionality of configuration from profile.yml.
  """
  pass

def load_profile():
    """
    Loads profile.yml to get configuration parameters.
    """
    try:
        config = Configuration()
        print("%s %s" % ("Profile is valid and parsed properly.", TextFormatter.get_check()))
        return config
    except:
        print("{0} {1}"
              .format("Profile parsed. Invalid configuration. Please reconfigure.",
                      TextFormatter.get_xmark()))
        sys.exit(-1)


if __name__ == "__main__":
  main()