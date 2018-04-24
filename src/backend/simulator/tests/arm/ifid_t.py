"""
Tests the ifid.py module
Must be run in the marinade/src/backend/simulator/tests/arm
"""

import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.ifid import Ifid
from simulator.components.core.bus import Bus
from simulator.components.abstract.sequential import Latch_Type, Logic_States

class Ifid_t(unittest.TestCase):
    "Unit test for ifid.py module"

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        pc4f = Bus(32)
        pc8f = Bus(32)
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        pc4d = Bus(32)
        pc8d = Bus(32)
        instrd = Bus(32)

        invalidBusSize = Bus(7)
        notBusType = 'w'

        with self.assertRaises(ValueError):
            Ifid(pc4f, pc8f, invalidBusSize, stall, flush, clk, pc4d, pc8d,
                 instrd)

        with self.assertRaises(TypeError):
            Ifid(notBusType, pc8f, instrf, stall, flush, clk, pc4d, pc8d,
                 instrd)

        Ifid(pc4f, pc8f, instrf, stall, flush, clk, pc4d, pc8d, instrd)


    def test_on_rising_edge(self):
        "Tests on_rising_edge method"
        pc4f = Bus(32)
        pc8f = Bus(32)
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        pc4d = Bus(32)
        pc8d = Bus(32)
        instrd = Bus(32)

        ifid = Ifid(pc4f, pc8f, instrf, stall, flush, clk, pc8d, pc8d, instrd)
        instrf.write(0xE3A0800A)    # mov r8, #10
        self.assertNotEqual(instrf.read(), instrd.read())
        ifid.on_rising_edge()
        self.assertEqual(instrf.read(), instrd.read())


    def test_on_falling_edge(self):
        "Tests on_falling_edge method"
        pc4f = Bus(32)
        pc8f = Bus(32)
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        pc4d = Bus(32)
        pc8d = Bus(32)
        instrd = Bus(32)

        ifid = Ifid(pc4f, pc8f, instrf, stall, flush, clk, pc4d, pc8d, instrd,
                    0, Latch_Type.FALLING_EDGE, Logic_States.ACTIVE_LOW, None,
                    Logic_States.ACTIVE_HIGH)
        instrf.write(0xE3A0800A)    # mov r8, #10
        flush.write(1)
        self.assertNotEqual(instrf.read(), instrd.read())
        ifid.on_falling_edge()
        self.assertEqual(instrf.read(), instrd.read())


    def test_inspect(self):
        "Tests inspect method"
        pc4f = Bus(32)
        pc8f = Bus(32)
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        pc4d = Bus(32)
        pc8d = Bus(32)
        instrd = Bus(32)

        ifid = Ifid(pc4f, pc8f, instrf, stall, flush, clk, pc4d, pc8d, instrd)
        self.assertEqual(ifid.inspect()['state']['instrd'], 0)
        instrf.write(0xE0090998)    # mul r9, r8, r9
        ifid.on_rising_edge()
        self.assertEqual(ifid.inspect()['state']['instrd'], 0xE0090998)


    def test_modify(self):
        "Tests modify method"
        pc4f = Bus(32)
        pc8f = Bus(32)
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        pc4d = Bus(32)
        pc8d = Bus(32)
        instrd = Bus(32)

        ifid = Ifid(pc4f, pc8f, instrf, stall, flush, clk, pc4d, pc8d, instrd)
        self.assertEqual(ifid.modify()['error'], 'ifid register cannot be modified')


    def test_run(self):
        "Test run method"
        pc4f = Bus(32)
        pc8f = Bus(32)
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        pc4d = Bus(32)
        pc8d = Bus(32)
        instrd = Bus(32)

        ifid = Ifid(pc4f, pc8f, instrf, stall, flush, clk, pc4d, pc8d, instrd)
        instrf.write(0xE24AA020)    # sub r10, r10, #32
        ifid.run()
        self.assertNotEqual(instrf.read(), instrd.read())
        clk.write(1)
        ifid.run()
        self.assertEqual(instrf.read(), instrd.read())
        clk.write(0)
        ifid.run()
        clk.write(1)
        flush.write(1)
        ifid.run()
        self.assertNotEqual(instrf.read(), instrd.read())

    def test_from_dict(self):
        "Validates dictionary constructor"
        raise NotImplementedError



if __name__ == '__main__':
    unittest.main()
