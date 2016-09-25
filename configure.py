import yaml
import utils.scanner as scanner
from utils.sorted_dict import UnsortableOrderedDict

config_dir = "config"

def main():
    parse()

def parse():
    left_index = scanner.read_int('Enter index of left camera: ')
    right_index = scanner.read_int('Enter index of right camer: ')

    source_dir = raw_input('Enter full path to image source directory: ')
    dest_dir = raw_input('Enter full path to image output directory: ')
    key_frame = raw_input('Enter full path to key frame image: ')
    left_video = raw_input('Enter path to left video: ')
    right_video = raw_input('Enter path to right video: ')

    try:
        width = int(raw_input('Enter image width: '))
    except ValueError:
        print "Please enter a number."

    format = raw_input('Enter image format: ')

    settings = UnsortableOrderedDict([
        ('left-index', left_index),
        ('right-index', right_index),
        ('source-dir', source_dir),
        ('dest-dir', dest_dir),
        ('key-frame', key_frame),
        ('width', width),
        ('format', format),
        ('left-video', left_video),
        ('right-video', right_video)
    ])

    with open(config_dir + '/profile.yml', 'w') as file:
        yaml.dump(settings, file, default_flow_style=False)

if __name__ == "__main__":
    main()
