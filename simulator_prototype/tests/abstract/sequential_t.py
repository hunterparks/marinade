import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.sequential import Latch_Type, Logic_States, Sequential

class Latch_Type_t(unittest.TestCase):

    def test_enums(self):
        "prove enum values are valid"
        self.assertTrue(Latch_Type.valid(Latch_Type.RISING_EDGE))
        self.assertTrue(Latch_Type.valid(Latch_Type.FALLING_EDGE))
        self.assertTrue(Latch_Type.valid(Latch_Type.BOTH_EDGE))
        self.assertFalse(Latch_Type.valid(3))
        self.assertFalse(Latch_Type.valid(-1))
        pass

class Logic_States_t(unittest.TestCase):

    def test_enums(self):
        "prove enum values are valid"
        self.assertTrue(Logic_States.valid(Logic_States.ACTIVE_LOW))
        self.assertTrue(Logic_States.valid(Logic_States.ACTIVE_HIGH))
        self.assertFalse(Logic_States.valid(2))
        self.assertFalse(Logic_States.valid(-1))

class Sequential_t(unittest.TestCase):

    def test_Sequential(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Sequential()

if __name__ == '__main__':
    unittest.main()
