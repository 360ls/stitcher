"""
Creates Configuration object based on data in profile.yml config file.
"""

from __future__ import absolute_import, division, print_function

import os.path
import yaml

from .textformatter import TextFormatter

class Configuration(object):
    """
    The Configuration class creates a configuration instance from a profile yaml file.
    """

    def __init__(self, config_profile):
        """ The Configuration class constructor instantiates the Configuration class. """

        self.config_profile = config_profile
        self.check_config_file()

    def check_config_file(self):
        """ Checks for an existing yaml configuration profile. """

        if not os.path.isfile(self.config_profile):
            raise ValueError('The provided configuration profile does not exist.')

    def get(self):
        """
        Maps configuration from profile to object.
        """

        # Opens up configuration profile and gets configuration, then cleans up.
        with open(self.config_profile, 'r') as config_profile:
            configuration = yaml.load(config_profile)

        return configuration

    def print(self):
        """
        Displays contents of configuration profile.
        """
        TextFormatter.print_heading("Current Configuration")
        with open(self.config_profile, 'r') as config_profile:
            configuration = yaml.load(config_profile)
        for key in sorted(configuration.keys()):
            TextFormatter.print_pair(key, configuration[key])
