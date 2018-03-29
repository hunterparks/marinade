"""
Test abstract component ConfigurationParser
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.abstract.configuration_parser import ConfigurationParser


class ConfigurationParser_t(unittest.TestCase):
    """
    Tests ConfigurationParser abstract component for error on construction
    """

    def test_ConfigurationParser(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = ConfigurationParser()


if __name__ == '__main__':
    unittest.main()
