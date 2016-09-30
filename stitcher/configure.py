"""
This module is responsible for taking in user input from the terminal and turning it into a configuration profile.
"""

import yaml
import utils.scanner as scanner
from utils.sorted_dict import UnsortableOrderedDict

CONFIG_DIR = "config"

def main():
    """ Calls the main parse method. """
    parse()

def parse():
    """ Parses user input to pass to the configuration profile. """
    left_index = scanner.read_int('Enter index of left camera: ')
    right_index = scanner.read_int('Enter index of right camer: ')

    source_dir = raw_input('Enter full path to image source directory: ')
    dest_dir = raw_input('Enter full path to image output directory: ')
    key_frame = raw_input('Enter full path to key frame image: ')
    video_dir = raw_input('Enter path to video source directory: ')
    left_video = raw_input('Enter path to left video: ')
    right_video = raw_input('Enter path to right video: ')

    port = scanner.read_int('Enter socket port number')

    try:
        width = int(raw_input('Enter image width: '))
    except ValueError:
        print "Please enter a number."

    img_format = raw_input('Enter image format: ')

    settings = UnsortableOrderedDict([
        ('left-index', left_index),
        ('right-index', right_index),
        ('source-dir', source_dir),
        ('dest-dir', dest_dir),
        ('key-frame', key_frame),
        ('width', width),
        ('format', img_format),
        ('video-dir', video_dir),
        ('left-video', left_video),
        ('right-video', right_video),
        ('port', port)
    ])

    with open(CONFIG_DIR + '/profile.yml', 'w') as config_file:
        yaml.dump(settings, config_file, default_flow_style=False)

if __name__ == "__main__":
    """ Ensures that script only runs when called explicitly. """
    main()
