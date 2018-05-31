"""
Tests core component BusSubset
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.core.bus_subset import BusSubset
from simulator.components.core.constant import Constant
from simulator.components.core.bus import Bus


class BusSubset_t(unittest.TestCase):
    """
    Tests BusSubset component's constructor and run functionality
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        c0 = Constant(16, 0xAAAA)
        b0 = Bus(4)
        b1 = Bus(8)
        b2 = Bus(2)
        b3 = Bus(2)

        with self.assertRaises(TypeError):
            bj = BusSubset(None, None, None)
        with self.assertRaises(TypeError):
            bj = BusSubset('0', None, None)
        with self.assertRaises(TypeError):
            bj = BusSubset(c0, None, None)
        with self.assertRaises(TypeError):
            bj = BusSubset(c0, [], [])
        with self.assertRaises(ValueError):
            bj = BusSubset(c0, ['0'], [(0, 1)])
        with self.assertRaises(TypeError):
            bj = BusSubset(c0, [b0], [])
        with self.assertRaises(TypeError):
            bj = BusSubset(c0, [b0], ['0'])
        with self.assertRaises(TypeError):
            bj = BusSubset(c0, [b0], [('0', '1')])
        with self.assertRaises(ValueError):
            bj = BusSubset(c0, [b0], [(1, 0)])
        with self.assertRaises(ValueError):
            bj = BusSubset(c0, [b0], [(0, 1)])
        with self.assertRaises(ValueError):
            bj = BusSubset(c0, [b0], [(0, 8)])

        bs = BusSubset(c0, [b0, b1, b2, b3], [(0, 4), (4, 12), (12, 14), (14, 16)])

    def test_run(self):
        "Prove correct combinational output given signals"
        c0 = Constant(16, 0xAAAA)
        b0 = Bus(4)
        b1 = Bus(8)
        b2 = Bus(2)
        b3 = Bus(2)
        b4 = Bus(1)

        bs = BusSubset(c0, [b0, b1, b2, b3, b4], [(0, 4), (4, 12), (12, 14), (14, 16), (3, 4)])
        bs.run()
        self.assertTrue(b0.read() == 0x0A)
        self.assertTrue(b1.read() == 0xAA)
        self.assertTrue(b2.read() == 0x02)
        self.assertTrue(b3.read() == 0x02)
        self.assertTrue(b4.read() == 1)

    def test_from_dict(self):
        "Validates dictionary constructor"
        hooks = OrderedDict({
            "i1" : Constant(8,0x0F),
            "o1" : Bus(4),
            "o2" : Bus(4)
        })

        config = {
            "input" : "i1",
            "outputs" : ["o1","o2"],
            "bounds" : [[0,4],[4,8]]
        }

        subset = BusSubset.from_dict(config,hooks)
        subset.run()
        self.assertEqual(hooks["o1"].read(),0xF)
        self.assertEqual(hooks["o2"].read(),0x0)


if __name__ == '__main__':
    unittest.main()
