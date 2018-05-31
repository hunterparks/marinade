"""
Tests core component Bus
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.core.bus import Bus


class Bus_t(unittest.TestCase):
    """
    Tests Bus component's read, write, size, constructor, and inspect
    functionality
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        with self.assertRaises(TypeError):
            b = Bus('0')
        with self.assertRaises(TypeError):
            b = Bus(0)
        with self.assertRaises(TypeError):
            b = Bus(1, -1)
        with self.assertRaises(TypeError):
            b = Bus(1, 2)
        with self.assertRaises(TypeError):
            b = Bus(1, '0')

        b = Bus(8, 255)
        self.assertTrue(b.read() == 255)
        self.assertTrue(b.size() == 8)

    def test_inspect(self):
        "Check inspect for valid data presentation"
        b = Bus(8, 255)
        ins = b.inspect()
        self.assertTrue(ins['type'] == 'logic')
        self.assertTrue(ins['size'] == 8)
        self.assertTrue(ins['state'] == 255)

    def test_read(self):
        "Valid data on read"
        b = Bus(32, 125536)
        self.assertTrue(b.read() == 125536)

    def test_write(self):
        "Valid update on write"
        b = Bus(16, 5)
        b.write(290)
        self.assertTrue(b.read() == 290)

    def test_size(self):
        "Valid bus size presented"
        b = Bus(8, 255)
        self.assertTrue(b.size() == 8)

    def test_from_dict(self):
        "Validates dictionary constructor"

        config = {
            "width" : 32,
            "value" : 7869
        }

        bus = Bus.from_dict(config,None) #Buses do not need hook reference


if __name__ == '__main__':
    unittest.main()
