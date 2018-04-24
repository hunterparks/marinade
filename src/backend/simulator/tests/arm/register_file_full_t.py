"""
Test arm component RegisterFile_wo_PC
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.arm.register_file_full import RegisterFile, Latch_Type, Logic_States
from simulator.components.core.constant import Constant
from simulator.components.core.bus import Bus


class RegisterFile_Full_t(unittest.TestCase):
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
        ra2 = Bus(4, 0)
        rd0 = Bus(32)
        rd1 = Bus(32)
        rd2 = Bus(32)
        en = Bus(1, 0)
        pc = Bus(32, 0)

        # just prove that the constructor accepts data when filled, rest is
        # tested under the core component

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, ra2, wa, rd0, rd1, rd2, pc)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, ra2, wa, rd0, rd1, rd2, pc,
                           edge_type=Latch_Type.BOTH_EDGE)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, ra2, wa, rd0, rd1, rd2, pc,
                           reset_type=Logic_States.ACTIVE_HIGH)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, ra2, wa, rd0, rd1, rd2, pc,
                           enable_type=Logic_States.ACTIVE_LOW)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, ra2, wa, rd0, rd1, rd2, pc,
                           Latch_Type.RISING_EDGE, Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_LOW)

    def test_run(self):
        "Prove that PC is routed from external signal to read"
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        wa = Bus(4, 0)
        wd = Bus(32, 10)
        ra0 = Bus(4, 0)
        ra1 = Bus(4, 0)
        ra2 = Bus(4, 0)
        rd0 = Bus(32)
        rd1 = Bus(32)
        rd2 = Bus(32)
        en = Bus(1, 0)
        pc = Bus(32, 0)

        reg = RegisterFile(clk, rst, en, wd, ra0, ra1, ra2, wa, rd0, rd1, rd2, pc)

        # set buses
        pc.write(255)
        ra0.write(15)
        ra1.write(15)
        ra2.write(1)

        #run and validate
        reg.run()
        self.assertEqual(rd0.read(), 255)
        self.assertEqual(rd1.read(), 255)
        self.assertNotEqual(rd2.read(), 255)

    def test_from_dict(self):
        "Validates dictionary constructor"
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
