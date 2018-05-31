"""
Test iBus, iBusRead, iBusWrite functionality
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.abstract.ibus import iBus, iBusRead, iBusWrite


class iBus_t(unittest.TestCase):
    """
    Tests iBus interface for error on construction
    """

    def test_iBus(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = iBus()


class iBusRead_t(unittest.TestCase):
    """
    Tests iBusRead interface for error on construction
    """

    def test_iBusRead(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = iBusRead()


class iBusWrite_t(unittest.TestCase):
    """
    Tests iBusWrite interface for error on construction
    """

    def test_iBusWrite(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = iBusWrite()


if __name__ == '__main__':
    unittest.main()
