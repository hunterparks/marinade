import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.memory_block import MemoryBlock

class MemoryBlock_t(unittest.TestCase):

    def test_MemoryBlock(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = MemoryBlock()

if __name__ == '__main__':
    unittest.main()
