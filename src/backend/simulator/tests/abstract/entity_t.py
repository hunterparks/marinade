"""
Test abstract component Entity
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.abstract.entity import Entity


class Entity_t(unittest.TestCase):
    """
    Test Entity abstract component for error on construction
    """

    def test_Entity(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Entity()


if __name__ == '__main__':
    unittest.main()
