"""
Test arm component RegisterFile_wo_PC
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.register_file_demo import RegisterFile, Latch_Type, Logic_States
from simulator.components.core.constant import Constant
from simulator.components.core.bus import Bus


class RegisterFile_Demo_t(unittest.TestCase):
    """
    Tests RegisterFile_wo_PC constructor for valid operation.
    Note that all other tests are covered by core RegisterFile
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        wa = Bus(4, 0)
        wd = Bus(32, 10)
        ra0 = Bus(4, 0)
        ra1 = Bus(4, 0)
        rd0 = Bus(32)
        rd1 = Bus(32)
        en = Bus(1, 0)

        # just prove that the constructor accepts data when filled, rest is
        # tested under the core component

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, wa, rd0, rd1)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, wa, rd0,
                           rd1, edge_type=Latch_Type.BOTH_EDGE)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, wa, rd0,
                           rd1, reset_type=Logic_States.ACTIVE_HIGH)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, wa, rd0,
                           rd1, enable_type=Logic_States.ACTIVE_LOW)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, wa, rd0, rd1,
                           Latch_Type.RISING_EDGE, Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_LOW)

    def test_from_dict(self):
        "Validates dictionary constructor"

        hooks = OrderedDict({
            "clock" : Bus(1),
            "reset" : Bus(1),
            "write_enable" : Bus(1),
            "write_data" : Bus(32),
            "a1" : Bus(4),
            "a2" : Bus(4),
            "a3" : Bus(4),
            "rd1" : Bus(32),
            "rd2" : Bus(32),
        })

        config = {
            "name" : "register_file_demo",
            "type" : "RegisterFileDemo",
            "clock" : "clock",
            "reset" : "reset",
            "write_enable" : "write_enable",
            "write_data" : "write_data",
            "a1" : "a1",
            "a2" : "a2",
            "a3" : "a3",
            "rd1" : "rd1",
            "rd2" : "rd2",
            "edge_type" : "falling_edge",
            "reset_type" : "active_high",
            "enable_type" : "active_low"
        }

        reg = RegisterFile.from_dict(config,hooks)


if __name__ == '__main__':
    unittest.main()
