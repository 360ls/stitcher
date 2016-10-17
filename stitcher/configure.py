"""
Creates configuration profile from user input
"""

from __future__ import absolute_import
import yaml
from .scanner import Scanner
from .sorted_dict import UnsortableOrderedDict

CONFIG_DIR = "config"

def main():
    """ Calls the main parse method. """
    parse()

def parse():
    """ Parses user input to pass to the configuration profile. """
    scanner = Scanner()
    left_index = scanner.read_int('Enter index of left camera: ')
    right_index = scanner.read_int('Enter index of right camera: ')
    video_dir = raw_input('Enter path to video source directory: ')
    left_video = raw_input('Enter path to left video: ')
    right_video = raw_input('Enter path to right video: ')
    port = scanner.read_int('Enter socket port number')
    resolution = scanner.read_int('Enter target resolution: ')
    first_index = scanner.read_int('Enter first camera index: ')
    second_index = scanner.read_int('Enter second camera index: ')
    third_index = scanner.read_int('Enter third camera index: ')
    fourth_index = scanner.read_int('Enter fourth camera index: ')

    settings = UnsortableOrderedDict([
        ('left-index', left_index),
        ('right-index', right_index),
        ('video-dir', video_dir),
        ('left-video', left_video),
        ('right-video', right_video),
        ('port', port),
        ('resolution', resolution),
        ('first-index', first_index),
        ('second-index', second_index),
        ('third-index', third_index),
        ('fourth-index', fourth_index)
    ])

    with open(CONFIG_DIR + '/profile.yml', 'w') as config_file:
        yaml.dump(settings, config_file, default_flow_style=False)

if __name__ == "__main__":
    main()
