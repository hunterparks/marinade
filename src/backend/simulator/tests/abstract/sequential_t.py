"""
Test emuarations Latch_Type and Logic_States
Test abstract component Sequential
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.abstract.sequential import Latch_Type, Logic_States, Sequential


class Latch_Type_t(unittest.TestCase):
    """
    Tests Latch_Type for valid enumerated values and correct identification
    """

    def test_enums(self):
        "prove enum values are valid"
        self.assertTrue(Latch_Type.valid(Latch_Type.RISING_EDGE))
        self.assertTrue(Latch_Type.valid(Latch_Type.FALLING_EDGE))
        self.assertTrue(Latch_Type.valid(Latch_Type.BOTH_EDGE))
        self.assertFalse(Latch_Type.valid(3))
        self.assertFalse(Latch_Type.valid(-1))

    def test_fromString(self):
        self.assertEqual(Latch_Type.fromString("rising_edge"),Latch_Type.RISING_EDGE)
        self.assertEqual(Latch_Type.fromString("falling_edge"),Latch_Type.FALLING_EDGE)
        self.assertEqual(Latch_Type.fromString("both_edge"),Latch_Type.BOTH_EDGE)
        self.assertEqual(Latch_Type.fromString("test"),None)

class Logic_States_t(unittest.TestCase):
    """
    Tests Logic_States for valid enumerated values and correct identification
    """

    def test_enums(self):
        "prove enum values are valid"
        self.assertTrue(Logic_States.valid(Logic_States.ACTIVE_LOW))
        self.assertTrue(Logic_States.valid(Logic_States.ACTIVE_HIGH))
        self.assertFalse(Logic_States.valid(2))
        self.assertFalse(Logic_States.valid(-1))

    def test_fromString(self):
        self.assertEqual(Logic_States.fromString("active_low"),Logic_States.ACTIVE_LOW)
        self.assertEqual(Logic_States.fromString("active_high"),Logic_States.ACTIVE_HIGH)
        self.assertEqual(Logic_States.fromString("test"),None)

class Sequential_t(unittest.TestCase):
    """
    Tests Sequential abstract component for error on construction
    """

    def test_Sequential(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Sequential()


if __name__ == '__main__':
    unittest.main()
