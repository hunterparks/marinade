"""
Tests arm state register ifid
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.ifid import Ifid
from components.core.bus import Bus
from components.abstract.sequential import Latch_Type, Logic_States

class Ifid_t(unittest.TestCase):
    "Unit test for Ifid class"

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(32)

        invalidBusSize = Bus(7)
        notBusType = 'w'

        with self.assertRaises(ValueError):
            ifid = Ifid(instrf, invalidBusSize, flush, clk, instrd)

        with self.assertRaises(TypeError):
            ifid = Ifid(notBusType, stall, flush, clk, instrd)

        idif = Ifid(instrf, stall, flush, clk, instrd)


    def test_on_rising_edge(self):
        "Tests on_rising_edge method"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(32)

        ifid = Ifid(instrf, stall, flush, clk, instrd)
        instrf.write(0xE3A0800A)    # mov r8, #10
        self.assertNotEqual(instrf.read(), instrd.read())
        ifid.on_rising_edge()
        self.assertEqual(instrf.read(), instrd.read())


    def test_on_falling_edge(self):
        "Tests on_falling_edge method"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(32)

        ifid = Ifid(instrf, stall, flush, clk, instrd, 0,
                    Latch_Type.FALLING_EDGE, Logic_States.ACTIVE_LOW, None,
                    Logic_States.ACTIVE_HIGH)
        instrf.write(0xE3A0800A)    # mov r8, #10
        flush.write(1)
        self.assertNotEqual(instrf.read(), instrd.read())
        ifid.on_falling_edge()
        self.assertEqual(instrf.read(), instrd.read())


    def test_inspect(self):
        "Tests inspect method"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(32)

        ifid = Ifid(instrf, stall, flush, clk, instrd)
        self.assertEqual(ifid.inspect()['state'], 0)
        instrf.write(0xE0090998)    # mul r9, r8, r9
        ifid.on_rising_edge()
        self.assertEqual(ifid.inspect()['state'], 0xE0090998)


    def test_modify(self):
        "Tests modify method"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(32)

        ifid = Ifid(instrf, stall, flush, clk, instrd)
        self.assertEqual(ifid.modify()['error'], 'ifid register cannot be modified')


    def test_run(self):
        "Test run method"
        instrf = Bus(32)
        stall = Bus(1)
        flush = Bus(1)
        clk = Bus(1)
        instrd = Bus(32)

        ifid = Ifid(instrf, stall, flush, clk, instrd)
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
        


if __name__ == '__main__':
    unittest.main()