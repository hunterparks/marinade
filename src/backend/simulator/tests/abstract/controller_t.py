"""
Test abstract component Controller
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.abstract.controller import Controller


class Controller_t(unittest.TestCase):
    """
    Tests Controller abstract component for error on construction
    """

    def test_Controller(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Controller()


if __name__ == '__main__':
    unittest.main()
