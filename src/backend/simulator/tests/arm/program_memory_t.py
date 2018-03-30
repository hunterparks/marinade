"""
Tests arm component ProgramMemory
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.arm.program_memory import ProgramMemory, Latch_Type, Logic_States
from simulator.components.core.bus import Bus


class ProgramMemory_t(unittest.TestCase):
    """
    Tests ProgramMemory's constructor and run functionality. Note that this
    object's parent test will test the internal memory attributes
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        ad = Bus(32, 0)
        rst = Bus(1, 0)
        rd = Bus(32, 0)

        # test invalid configurations
        with self.assertRaises(ValueError):
            mem = ProgramMemory(ad, rst, rd, -1, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = ProgramMemory(ad, rst, rd, 0, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = ProgramMemory(ad, rst, rd, '0', 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = ProgramMemory(ad, rst, rd, 4, '0x81', Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            mem = ProgramMemory(ad, rst, rd, 4, -1, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            mem = ProgramMemory(ad, rst, rd, 4, 0x81, 'Logic_States.ACTIVE_HIGH')

        # test invalid buses
        with self.assertRaises(TypeError):
            mem = ProgramMemory('ad', rst, rd, 64, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            a = Bus(3)
            mem = ProgramMemory(a, rst, rd, 64, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = ProgramMemory(ad, 'rst', rd, 64, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            r = Bus(2)
            mem = ProgramMemory(ad, r, rd, 64, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(TypeError):
            mem = ProgramMemory(ad, rst, 'rd', 64, 0x81, Logic_States.ACTIVE_HIGH)

        with self.assertRaises(ValueError):
            r = Bus(33)
            mem = ProgramMemory(ad, rst, r, 64, 0x81, Logic_States.ACTIVE_HIGH)

        # valid construction
        mem = ProgramMemory(ad, rst, rd, 64, 0x81, Logic_States.ACTIVE_HIGH)

    def test_run(self):
        """
        tests the memory's run function
        """
        ad = Bus(32, 0)
        rst = Bus(1, 0)
        rd = Bus(32, 0)

        mem = ProgramMemory(ad, rst, rd, default_size=32)

        # "flash" data to program memory
        data = []
        for i in range(0, 32):
            data.append(i + 1)
        msg = mem.modify({'start': 0, 'data': data})

        # read from memory validating "programming"
        for i in range(0, 8):
            ad.write(i * 4)
            mem.run()
            word = 0
            for j in range(0, 4):
                word |= data[i * 4 + j] << (32 - ((j + 1) * 8))
            self.assertEqual(rd.read(), word)

        # test clear message proving empty
        mem.clear()
        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()),0)


if __name__ == '__main__':
    unittest.main()
