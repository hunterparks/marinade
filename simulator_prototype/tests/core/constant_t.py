"""
Tests core component Constant
"""

import unittest
import sys
sys.path.insert(0,'../../')
from components.core.constant import Constant



class Constant_t(unittest.TestCase):
    """
    Tests Constant component's constructor, inpsect, read, write and size
    functionality
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        with self.assertRaises(TypeError):
            l = Constant('8',0)
        with self.assertRaises(TypeError):
            l = Constant(0,0)
        with self.assertRaises(TypeError):
            l = Constant(1,'0')
        with self.assertRaises(TypeError):
            l = Constant(1,-1)
        with self.assertRaises(TypeError):
            l = Constant(1,2)
        with self.assertRaises(Exception):
            l = Constant(16)
        l = Constant(1,1)


    def test_inspect(self):
        "Check inspect for valid data presentation"
        l = Constant(8,255)
        ins = l.inspect()
        self.assertTrue(ins['type'] == 'logic')
        self.assertTrue(ins['size'] == 8)
        self.assertTrue(ins['state'] == 255)


    def test_read(self):
        "Valid data on read"
        l = Constant(8,97)
        self.assertTrue(l.read() == 97)


    def test_write(self):
        "Exception expected on write"
        l = Constant(32,2600000)

        with self.assertRaises(Exception):
            l.write(152)


    def test_size(self):
        "Valid bus size presented"
        l = Constant(16,56)
        self.assertTrue(l.size() == 16)


if __name__ == '__main__':
    unittest.main()
