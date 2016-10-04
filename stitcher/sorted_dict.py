"""
This module enapsulates the UnsortableList and UnsortableOrderedDict classes
to enable instantiation of unsorted ordered dictionaries, which are used
to write key-value pairs in a desired order into a yaml format.
"""

from collections import OrderedDict
import yaml

class UnsortableList(list):
    """ The UnsortableList class. """
    def sort(self, *args, **kwargs):
        pass

class UnsortableOrderedDict(OrderedDict):
    """ Dictionary with Ordered Key/Value pairs """

    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))

yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)
