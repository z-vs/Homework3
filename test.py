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

    def test_declare_integer_and_float_constants(self):
        self.config_parser.declare_constant('let max_retries = 5')
        self.config_parser.declare_constant('let pi = 3.14159')

        self.assertEqual(self.config_parser.constants['max_retries'], 5)
        self.assertEqual(self.config_parser.constants['pi'], 3.14159)

    def test_declare_string_constants(self):
        self.config_parser.declare_constant('let greeting = "Hello, World!"')
        self.config_parser.declare_constant('let language = "Python"')

        self.assertEqual(self.config_parser.constants['greeting'], "Hello, World!")
        self.assertEqual(self.config_parser.constants['language'], "Python")

    def test_declare_array_constants(self):
        self.config_parser.declare_constant('let languages = #("en", "es", "fr")')

        self.assertEqual(self.config_parser.constants['languages'], ['en', 'es', 'fr'])

    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            self.config_parser.declare_constant('let x = !!')

        with self.assertRaises(ValueError):
            self.config_parser.declare_constant('let y = 123abc')

    def test_handle_empty_config(self):
        self.assertEqual(self.config_parser.constants, {})

    def test_nested_arrays(self):
        self.config_parser.declare_constant('let nested_languages = #("en", #("fr", "de"))')
        self.assertEqual(self.config_parser.constants['nested_languages'], ['en', ['fr', 'de']])

    def test_declare_mixed_constants(self):
        config_lines = [
            'let max_retries = 3',
            'let is_active = true',
            'let greeting = "Hello"',
            'let languages = #("en", "fr", "de")'
        ]
        for line in config_lines:
            self.config_parser.declare_constant(line)

        self.assertEqual(self.config_parser.constants['max_retries'], 3)
        self.assertEqual(self.config_parser.constants['is_active'], True)
        self.assertEqual(self.config_parser.constants['greeting'], "Hello")
        self.assertEqual(self.config_parser.constants['languages'], ['en', 'fr', 'de'])

    def test_empty_array(self):
        self.config_parser.declare_constant('let empty_list = #()')
        self.assertEqual(self.config_parser.constants['empty_list'], [])

    def test_special_characters_in_string(self):
        self.config_parser.declare_constant('let file_path = "C:\\Program Files\\App"')
        self.assertEqual(self.config_parser.constants['file_path'], "C:\\Program Files\\App")


if __name__ == '__main__':
    unittest.main()
