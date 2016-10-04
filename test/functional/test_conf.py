import unittest
import yaml

from stitcher.configuration import Configuration

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        config = Configuration("test/fixtures/profile.yml")
        self.configuration = config

    def test_if_parsed_config_matches_profile(self):
        with open(self.configuration.config_file, 'r') as config_file:
            doc = yaml.load(config_file)

        for key in doc:
            attr = key.replace("-", "_")
            field = getattr(self.configuration, attr)
            self.assertEquals(doc[key], field.value)
