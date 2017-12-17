import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.controller import Controller

class Controller_t(unittest.TestCase):

    def test_Controller(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Controller()

if __name__ == '__main__':
    unittest.main()
