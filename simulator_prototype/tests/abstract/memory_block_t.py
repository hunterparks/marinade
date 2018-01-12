"""
Test abstract component MemoryBlock
"""

import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.memory_block import MemoryBlock



class MemoryBlock_t(unittest.TestCase):
    """
    Tests MemoryBlock abstract component for error on construction
    """

    def test_MemoryBlock(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = MemoryBlock()


if __name__ == '__main__':
    unittest.main()
