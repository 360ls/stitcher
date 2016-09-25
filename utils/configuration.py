import yaml
import os.path

class Configuration:
    def __init__(self):
        self.config_file = "config/profile.yml"
        self.check_config_file()
        self.initialize()

    def check_config_file(self):
        if not os.path.isfile(self.config_file):
            raise ValueError('Configuration file does not exist.')

    def initialize(self):
        with open(self.config_file, 'r') as f:
            doc = yaml.load(f)
            self.left_index = doc["left-index"]
            self.right_index = doc["right-index"]
            self.source_dir = doc["source-dir"]
            self.dest_dir = doc["dest-dir"]
            self.keyframe = doc["key-frame"]
            self.width = doc["width"]
            self.format = doc["format"]
            self.left_video = doc["left-video"]
            self.right_video = doc["right-video"]
            self.video_dir = doc["video-dir"]
