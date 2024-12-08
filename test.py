import unittest
from config_parser import ConfigParser
import json


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.config_parser = ConfigParser()

    def test_declare_boolean_constants(self):
        self.config_parser.declare_constant('let is_active = true')
        self.config_parser.declare_constant('let is_enabled = false')

        self.assertEqual(self.config_parser.constants['is_active'], True)
        self.assertEqual(self.config_parser.constants['is_enabled'], False)
