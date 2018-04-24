"""
Tests architecture's limit definitions
"""

import unittest
import sys
sys.path.insert(0, '../../')
import simulator.limits as limits

class Limits_t(unittest.TestCase):
    """
    Tests limit module for existence of all necessary constants
    """

    def test_limits_exists(self):
        "Prove that all limits exist and are properly defined"

        self.assertTrue(isinstance(limits.MAX_FREQUENCY, (int, float)))
        self.assertTrue(isinstance(limits.MIN_FREQUENCY, (int, float)))
        self.assertTrue(isinstance(limits.MAX_MEMORY_BLOCK, (int)))
        self.assertTrue(isinstance(limits.MIN_MEMORY_BLOCK, (int)))
        self.assertTrue(isinstance(limits.MAX_BYTES_IN_WORD, (int)))
        self.assertTrue(isinstance(limits.MIN_ADDRESS, (int)))
        self.assertTrue(isinstance(limits.MAX_ADDRESS, (int)))

if __name__ == '__main__':
    unittest.main()
