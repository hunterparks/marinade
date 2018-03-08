"""
Test arm component ControllerSingleCycle
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.controller_single_cycle_full import ControllerSingleCycle
from components.core.bus import Bus


class ControllerSingleCycle_t(unittest.TestCase):
    """
    Test ControllerSingleCycle's constructor, run and hook functionality
    """

    def test_constructor(self):
        "tests 4 bad constructors - not all possible constructors tested"
        raise NotImplementedError

    def test_run(self):
        "tests the signle cycle processors run method"
        raise NotImplementedError

    def test_inspect(self):
        "tests the single cycle processors inspect method"
        raise NotImplementedError

    def test_modify(self):
        "tests the single cycle processor modify method"
        raise NotImplementedError

    def test_clear(self):
        "tests the single cycle processor clear method"
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
