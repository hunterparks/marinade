"""
Component testing suite imports all tests written for abstract, core, and
arm. Note that simulation and architecture are not incorporated in this test.
"""

import unittest
import sys
sys.path.insert(0,'../')

from tests.abstract import *
from tests.core import *
from tests.arm import *



if __name__ == '__main__':
    "Run all tests imported from subdirectories"
    unittest.main()
