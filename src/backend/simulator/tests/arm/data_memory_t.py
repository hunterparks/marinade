"""
Tests arm component DataMemory
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.arm.data_memory import DataMemory, Latch_Type, Logic_States
from simulator.components.core.bus import Bus


class DataMemory_t(unittest.TestCase):
    """
    Tests DataMemory's constructor and run functionality. Note that this
    object's parent test will test the internal memory attributes
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        ad = Bus(32, 0)
        wd = Bus(32, 0)
        we = Bus(1, 0)
        rst = Bus(1, 0)
        clk = Bus(1, 0)
        rd = Bus(32, 0)
        am = Bus(2,0)

        # test invalid configurations
        with self.assertRaises(ValueError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, -1, 0x81, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, 0, 0x81, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, '0', 0x81, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, 4, '-1', Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, 4, -1, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, 4, 0, 'Latch_Type.FALLING_EDGE',
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, 4, 0, Latch_Type.FALLING_EDGE,
                             [Logic_States.ACTIVE_HIGH], Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, am, 4, 0, Latch_Type.FALLING_EDGE,
                             [Logic_States.ACTIVE_HIGH], None)

        # test invalid buses
        with self.assertRaises(TypeError):
            mem = DataMemory('a', wd, we, rst, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            a = Bus(3)
            mem = DataMemory(a, wd, we, rst, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, 'wd', we, rst, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            w = Bus(31)
            mem = DataMemory(ad, w, we, rst, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, 'we', rst, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            w = Bus(2)
            mem = DataMemory(ad, wd, w, rst, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, 'rst', clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            r = Bus(2)
            mem = DataMemory(ad, wd, we, r, clk, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, rst, 'clk', rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            c = Bus(2)
            mem = DataMemory(ad, wd, we, rst, c, rd, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, rst, clk, 'rd', am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            r = Bus(33)
            mem = DataMemory(ad, wd, we, rst, clk, r, am, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = DataMemory(ad, wd, we, rst, clk, rd, 'am', 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            a = Bus(1)
            mem = DataMemory(ad, wd, we, rst, clk, rd, a, 64, 0, Latch_Type.FALLING_EDGE,
                             Logic_States.ACTIVE_HIGH, Logic_States.ACTIVE_HIGH)

        # valid construction
        mem = DataMemory(ad, wd, we, rst, clk, rd, am, 16, 0x81,
                         Latch_Type.FALLING_EDGE, Logic_States.ACTIVE_HIGH,
                         Logic_States.ACTIVE_HIGH)

    def test_run(self):
        """
        tests the memory's run function
        """
        ad = Bus(32, 0)
        wd = Bus(32, 0)
        we = Bus(1, 0)
        rst = Bus(1, 0)
        clk = Bus(1, 0)
        rd = Bus(32, 0)

        mem = DataMemory(ad, wd, we, rst, clk, rd, default_size=16, default_value=0x81)

        # write to memory cells
        we.write(1)
        for i in range(0, 4):
            ad.write(4 * i)
            wd.write(i * 25)
            clk.write(0)
            mem.run()
            clk.write(1)
            mem.run()
            clk.write(0)
            mem.run()

        # insect memory contents
        msg = mem.inspect()
        self.assertTrue(len(msg['state'].keys()) == 16)

        # read from memory cells
        we.write(0)
        for i in range(0, 4):
            ad.write(4 * i)
            mem.run()
            self.assertEqual(rd.read(), i * 25)

        # check reset behavior
        rst.write(1)
        mem.run()
        rst.write(0)
        for i in range(0, 4):
            ad.write(4 * i)
            mem.run()
            self.assertEqual(rd.read(), 0x81818181)


if __name__ == '__main__':
    unittest.main()
