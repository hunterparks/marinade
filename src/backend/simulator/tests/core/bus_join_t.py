"""
Tests core component BusJoin
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.core.bus_join import BusJoin
from simulator.components.core.constant import Constant
from simulator.components.core.bus import Bus


class BusJoin_t(unittest.TestCase):
    """
    Tests BusJoin component's constructor and run functionality
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        c1 = Constant(1, 1)
        c2 = Constant(2, 0)
        c3 = Constant(3, 7)
        b = Bus(6)

        with self.assertRaises(TypeError):
            bj = BusJoin(None, None)
        with self.assertRaises(TypeError):
            bj = BusJoin(None, b)
        with self.assertRaises(TypeError):
            bj = BusJoin([], b)
        with self.assertRaises(TypeError):
            bj = BusJoin([c1, c2], None)
        with self.assertRaises(ValueError):
            bj = BusJoin([c1, c2], b)

        bj = BusJoin([c1, c2, c3], b)

    def test_run(self):
        "Prove correct combinational output given signals"
        c1 = Constant(1, 1)
        c2 = Constant(2, 0)
        c3 = Constant(3, 7)
        b = Bus(6)

        bj = BusJoin([c1, c2, c3], b)
        bj.run()
        self.assertTrue(b.read() == 0x39)


if __name__ == '__main__':
    unittest.main()
