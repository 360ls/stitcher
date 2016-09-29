"""
This module enapsulates the UnsortableList and UnsortableOrderedDict classes
to enable instantiation of unsorted ordered dictionaries, which are used 
to write key-value pairs in a desired order into a yaml format.
"""

import yaml

from collections import OrderedDict

class UnsortableList(list):
	""" The UnsortableList class. """
	
	def sort(self, *args, **kwargs):
		pass

class UnsortableOrderedDict(OrderedDict):
	""" The UnsortableOrderedDict class is responsible for creating an unsortable dictionary from an ordered dictionary. """

	def items(self, *args, **kwargs):
		return UnsortableList(OrderedDict.items(self, *args, **kwargs))

yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)
