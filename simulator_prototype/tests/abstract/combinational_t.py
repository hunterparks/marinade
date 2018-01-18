import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.combinational import Combinational

class Combinational_t(unittest.TestCase):

    def test_Combinational(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Combinational()

if __name__ == '__main__':
    unittest.main()
