"""
Test core component Memory
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.core.memory import Memory, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus import Bus


class Memory_t(unittest.TestCase):
    """
    Test Core Memory constructor, inspect, modify, clocking, reset, and run
    functionality.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(1, 0)
        w = Bus(8, 10)
        r = Bus(1, 0)
        en = Bus(1, 0)
        raise NotImplementedError

    def test_on_rising_edge(self):
        """
        tests the memory's on_rising_edge function
        """
        raise NotImplementedError

    def test_on_falling_edge(self):
        """
        tests the memory's on_falling_edge function
        """
        raise NotImplementedError

    def test_on_reset(self):
        """
        tests the memory's on reset function
        """
        raise NotImplementedError

    def test_modify(self):
        """
        tests the memories modify function
        """
        raise NotImplementedError

    def test_run(self):
        """
        tests the memories run function
        """
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
