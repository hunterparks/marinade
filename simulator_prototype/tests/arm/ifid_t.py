"""
Tests arm state register ifid
"""

import unittest
import sys
sys.path.insert(0, '/sto/Documents/SeniorDesign/marinade/simulator_prototype/')
from components.arm.ifid import Ifid
from components.core.bus import Bus

class Ifid_t(unittest.TestCase):

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(1)

        with self.assertRaises(ValueError):
            ifid = Ifid(stall, instrf, flush, clk, instrd)

        idif = Ifid(instrf, stall, flush, clk, instrd)

    