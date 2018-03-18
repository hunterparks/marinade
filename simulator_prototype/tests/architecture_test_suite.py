"""
Architecture test suite aggregates and runs all tests in architecture
subdirectory.
"""

import unittest
import sys
sys.path.insert(0, '../')

from tests.architecture import *


if __name__ == '__main__':
    "Run all tests imported from subdirectories"
    unittest.main()
