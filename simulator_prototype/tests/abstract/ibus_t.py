import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.ibus import iBus, iBusRead, iBusWrite

class iBus_t(unittest.TestCase):

    def test_iBus(self):
        try:
            testBus = iBus()
        except:
            self.assertTrue(True)

class iBusRead_t(unittest.TestCase):

    def test_iBusRead(self):
        try:
            testBus = iBusRead()
        except:
            self.assertTrue(True)

class iBusWrite_t(unittest.TestCase):

    def test_iBusWrite(self):
        try:
            testBus = iBusWrite()
        except:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
