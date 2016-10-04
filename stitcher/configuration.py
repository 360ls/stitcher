"""
Creates Configuration object based on profile.yml
"""

import os.path
import sys
import yaml

class Field(object):
    """
    Object representation for a configuration field
    """
    def __init__(self, key, value):
        self.value = value
        self.key = key

    def get_value(self):
        """
        Returns field value
        """
        return self.value

    def update(self, value):
        """
        Updates field value
        """
        self.value = value

class DirectoryField(Field):
    """
    String Field
    """
    def update(self, value):
        print value
        if not os.path.isdir(value):
            raise ValueError
        else:
            self.value = value

class NumField(Field):
    """
    Number Field
    """
    def update(self, value):
        if not isinstance(value, int):
            raise ValueError
        else:
            self.value = value

class FileField(Field):
    """
    File Field
    """
    def update(self, value):
        if not os.path.isfile(value):
            raise ValueError
        else:
            self.value = value

class Configuration(object):
    """ The Configuration class enables configuration instances to be created. """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, configFile="config/profile.yml"):
        """ The Configuration class constructor instantiates the Configuration class. """

        self.config_file = configFile
        self.check_config_file()
        self.initialize()

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

    def initialize(self):
        """ Parses profile.yml to initialize configuration values """
        try:
            with open(self.config_file, 'r') as config_file:
                doc = yaml.load(config_file)
            self.left_index = self.get_num_field("left-index", doc)
            self.right_index = self.get_num_field("right-index", doc)
            self.left_video = self.get_file_field("left-video", doc)
            self.right_video = self.get_file_field("right-video", doc)
            self.video_dir = self.get_directory_field("video-dir", doc)
            self.port = self.get_num_field("port", doc)
        except ValueError:
            print ValueError.message
            raise Exception
        except KeyError:
            print KeyError.message
            raise Exception

    @staticmethod
    def get_num_field(key, doc):
        """returns a numeric field"""
        if key not in doc:
            print "field {0} is not defined".format(key)
            raise KeyError
        try:
            val = int(doc[key])
            return NumField(key, val)
        except ValueError:
            print "{0} is not an integer value".format(doc[key])
            raise ValueError

    @staticmethod
    def get_file_field(key, doc):
        """returns a file field"""
        if key not in doc:
            print "field {0} is not defined".format(key)
            raise KeyError
        elif not os.path.isfile(doc[key]):
            print "file {0} not found".format(doc[key])
            raise ValueError
        else:
            return FileField(key, doc[key])

    @staticmethod
    def get_directory_field(key, doc):
        """returns a directory field"""
        if key not in doc:
            raise KeyError("field {0} is not defined".format(key))
        elif not os.path.isdir(doc[key]):
            raise ValueError("directory {0} not found".format(doc[key]))
        else:
            return DirectoryField(key, doc[key])

    def get_field(self, key, doc):
        """ Checks to make sure valid keys are in the profile.yml configuration file. """

        if key in doc:
            return doc[key]
        else:
            print "\"{0}\" is not a valid key in {1}.".format(key, self.config_file)
            print "Run configure.py again or define key in {0}".format(self.config_file)
            sys.exit(1)

    def print_configuration(self):
        """
        Displays configuration file contents
        """

        with open(self.config_file, 'r') as config_file:
            print config_file.read()

    def get_value(self, field):
        """
        Returns the value of a field
        """
        return getattr(self, field.replace("-", "_"))

    def set(self, key, val):
        """
        Modifies a configuration field with specifed value
        """
        with open(self.config_file) as config_file:
            config_dict = yaml.load(config_file)

        field = self.get_value(key)
        field.update(val)
        config_dict[key.replace("_", "-")] = val

        with open(self.config_file, 'w') as config_file:
            yaml.dump(config_dict, config_file, default_flow_style=False)
