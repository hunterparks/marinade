"""
Test core component Memory
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.core.memory import Memory, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus import Bus
import limits


class Memory_t(unittest.TestCase):
    """
    Test Core Memory constructor, inspect, modify, clocking, reset, and run
    functionality.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(8, 0)
        w = Bus(16, 0)
        r = Bus(16, 0)
        en = Bus(1, 0)

        # Test configuration parameters
        with self.assertRaises(TypeError):
            mem = Memory(17.1, 2, 0, a, w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            mem = Memory(limits.MAX_MEMORY_BLOCK + 1, 2, 0, a, w, en, rst, clk, r)

        with self.assertRaises(TypeError):
            mem = Memory(256, 'v', 0, a, w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, limits.MAX_BYTES_IN_WORD + 1, 0, a, w, en, rst, clk, r)

        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r, default_value='cake')

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r, default_value=2**(8 * 2))

        with self.assertRaises(TypeError):
            mem = Memory(256, 2, [], a, w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, limits.MAX_ADDRESS + 1, a, w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, limits.MAX_ADDRESS + 1 - 256, a, w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r, edge_type=None)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r, reset_type='cats')

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r, writeEnable_type=[])

        # Test bus parameters
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, 'a', w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            a = Bus(7)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r)

        a = Bus(8)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, 'w', en, rst, clk, r)

        with self.assertRaises(ValueError):
            w = Bus(17)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r)

        w = Bus(16)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, 'en', rst, clk, r)

        with self.assertRaises(ValueError):
            en = Bus(2)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r)

        en = Bus(1)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, 'rst', clk, r)

        with self.assertRaises(ValueError):
            rst = Bus(2)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r)

        rst = Bus(1)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, 'clk', r)

        with self.assertRaises(ValueError):
            clk = Bus(2)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r)

        clk = Bus(1)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, 'r')

        with self.assertRaises(ValueError):
            r = Bus(15)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, r)

        r = Bus(16)

        # Construct a valid object
        mem = Memory(256, 2, 0, a, w, en, rst, clk, r, 0, Latch_Type.FALLING_EDGE,
                     Logic_States.ACTIVE_LOW, Logic_States.ACTIVE_LOW)

    def test_on_rising_edge(self):
        """
        tests the memory's on_rising_edge function
        """
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(10, 0)
        w = Bus(32, 10)
        r = Bus(32, 0)
        en = Bus(1, 1)

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, r,
                     default_value=55, edge_type=Latch_Type.FALLING_EDGE)
        mem.on_rising_edge()
        self.assertTrue(0 not in mem.inspect()['state'])

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, r,
                     default_value=55, edge_type=Latch_Type.RISING_EDGE)
        mem.on_rising_edge()
        self.assertTrue(0 in mem.inspect()['state'])
        self.assertEqual(mem.inspect()['state'][3], 10)

    def test_on_falling_edge(self):
        """
        tests the memory's on_falling_edge function
        """
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(10, 0)
        w = Bus(32, 10)
        r = Bus(32, 0)
        en = Bus(1, 1)

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, r,
                     default_value=55, edge_type=Latch_Type.RISING_EDGE)
        mem.on_falling_edge()
        self.assertTrue(0 not in mem.inspect()['state'])

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, r,
                     default_value=55, edge_type=Latch_Type.FALLING_EDGE)
        mem.on_falling_edge()
        self.assertTrue(0 in mem.inspect()['state'])
        self.assertEqual(mem.inspect()['state'][3], 10)

    def test_on_reset(self):
        """
        tests the memory's on reset function
        """
        a = Bus(10)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)

        mem = Memory(1024, 4, 0, a, wd, memwr, reset, clock, rd)

        a.write(0x0)
        wd.write(1)
        mem.on_falling_edge()
        a.write(0xC)
        wd.write(1)
        mem.on_falling_edge()

        msg = mem.inspect()
        self.assertTrue(len(msg['state'].keys()) == 8)
        mem.on_reset()
        msg = mem.inspect()
        self.assertTrue(len(msg['state'].keys()) == 0)

    def test_inspect(self):
        """
        Tests the memory's insect function
        """
        a = Bus(10)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)

        mem = Memory(1024, 1, 4, a, wd, memwr, reset, clock, rd)
        msg = mem.inspect()
        self.assertTrue(msg['type'] == 'Memory')
        self.assertTrue(msg['size'] == 1024)
        self.assertTrue(len(msg['state'].keys()) == 0)

        a.write(0x4)
        wd.write(1)
        mem.on_falling_edge()
        a.write(0xC)
        wd.write(201)
        mem.on_falling_edge()

        msg = mem.inspect()
        self.assertTrue(msg['type'] == 'Memory')
        self.assertTrue(msg['size'] == 1024)
        self.assertTrue(len(msg['state'].keys()) == 2)
        self.assertTrue(msg['state'][0x4] == 1)
        self.assertTrue(msg['state'][0xC] == 201)

    def test_modify(self):
        """
        tests the memory's modify function
        """
        a = Bus(1)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)

        mem = Memory(2, 1, 0, a, wd, memwr, reset, clock, rd)

        tm = None
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {}
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': '0',
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': -1,
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 2,
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': '[]'
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 1,
            'data': [12, 15]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [12, 15, 25]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [256]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [256, 256]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [255, 255]
        }
        rm = mem.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start': 0,
            'data': [15]
        }
        rm = mem.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start': 1,
            'data': [25]
        }
        rm = mem.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start': 0,
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

    def test_run(self):
        """
        tests the memory's run function
        """
        a = Bus(2)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)

        mem = Memory(3, 1, 0, a, wd, memwr, reset, clock, rd, default_value=37)

        # write to each memory address
        memwr.write(1)
        for i in range(0, 4):
            a.write(i)
            wd.write(i * 25)
            clock.write(0)
            mem.run()
            clock.write(1)
            mem.run()
            clock.write(0)
            mem.run()

        # read from each valid memory address
        memwr.write(0)
        for i in range(0, 3):
            a.write(i)
            mem.run()
            self.assertTrue(rd.read() == i * 25)

        # read from invalid memory address
        a.write(3)
        mem.run()
        self.assertTrue(rd.read() == 37)


if __name__ == '__main__':
    unittest.main()
