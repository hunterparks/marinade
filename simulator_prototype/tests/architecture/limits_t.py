"""
Tests architecture's limit definitions
"""

import unittest
import sys
sys.path.insert(0, '../../')
import limits



class Limits_t(unittest.TestCase):
    """
    Tests limit module for existence of all necessary constants
    """

    def test_limits_exists(self):
        "Prove that all limits exist and are properly defined"

        self.assertTrue(isinstance(limits.MAX_FREQUENCY,(int,float)))
        self.assertTrue(isinstance(limits.MIN_FREQUENCY,(int,float)))


if __name__ == '__main__':
    unittest.main()
