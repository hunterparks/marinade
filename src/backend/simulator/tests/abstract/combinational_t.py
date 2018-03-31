"""
Test abstract component Combinational
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.abstract.combinational import Combinational


class Combinational_t(unittest.TestCase):
    """
    Tests Combinational abstract component for error on construction
    """

    def test_Combinational(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Combinational()


if __name__ == '__main__':
    unittest.main()
