"""
Tests the hazard controller
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.hazard import HazardController
from components.core.bus import Bus

class HazardController_t(unittest.TestCase):
    "Unit tests for hazard controller"

    def test_contructor(self):
        "Tests constructor with valid and invalid configuration"
        pass


    def test_generate_fwda(self):
        pass

    
    def test_generate_fwdb(self):
        pass


    def test_generate_fwds(self):
        pass


    def test_generate_stalld(self):
        pass


    def test_generate_flushd(self):
        pass

    
    def test_run(self):
        pass


    def test_inspect(self):
        pass


    def test_modify(self):
        pass



if __name__ == '__main__':
    unittest.main()