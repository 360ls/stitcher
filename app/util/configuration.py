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

    def __init__(self, config_profile="config/profile.yml"):
        """ The Configuration class constructor instantiates the Configuration class. """

        self.config_file = config_profile
        self.check_config_file()

    def get_fields(self):
        """ Returns generator of instance key value pairs """
        for attr, value in self.__dict__.iteritems():
            if attr == "config_file":
                continue
            yield value

    def check_config_file(self):
        """ Checks for an existing yml configuration file. """

        if not os.path.isfile(self.config_file):
            raise ValueError('Configuration file does not exist.')

    def print_configuration(self):
        """
        Displays configuration file contents
        """

        with open(self.config_file, 'r') as config_file:
            config_dict = yaml.load(config_file)
        for key in sorted(config_dict.keys()):
            TextFormatter.print_pair(key, config_dict[key])
