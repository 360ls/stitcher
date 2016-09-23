import yaml

class Configuration:
    def __init__(self):
        with open("config/profile.yml", 'r') as f:
            doc = yaml.load(f)
            self.left_index = doc["left-index"]
            self.right_index = doc["right-index"]
            self.source_dir = doc["source-dir"]
            self.dest_dir = doc["dest-dir"]
            self.keyframe = doc["key-frame"]
            self.width = doc["width"]
            self.format = doc["format"]
