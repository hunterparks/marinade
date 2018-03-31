"""
Tests core component LogicInput
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.core.logic_input import LogicInput


class LogicInput_t(unittest.TestCase):
    """
    Tests LogicInput's constructor, read, write, size, inspect, and generate
    functionality
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        with self.assertRaises(TypeError):
            l = LogicInput('8', 0)
        with self.assertRaises(TypeError):
            l = LogicInput(0, 0)
        with self.assertRaises(TypeError):
            l = LogicInput(1, '0')
        with self.assertRaises(TypeError):
            l = LogicInput(1, -1)
        with self.assertRaises(TypeError):
            l = LogicInput(1, 2)
        l = LogicInput(1, 1)
        self.assertTrue(l.size() == 1 and l.read() == 1)
        l = LogicInput(16)
        self.assertTrue(l.size() == 16 and l.read() == 0)

    def test_inspect(self):
        "Check inspect for valid data presentation"
        l = LogicInput(8, 255)
        ins = l.inspect()
        self.assertTrue(ins['type'] == 'logic')
        self.assertTrue(ins['size'] == 8)
        self.assertTrue(ins['state'] == 255)

    def test_generate(self):
        "Check generate handler for valid and invalid message"
        l = LogicInput(8, 0)

        m = None
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {}
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'state': '0'
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'state': -1
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'state': 256
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'state': 128
        }
        rm = l.generate(m)
        self.assertTrue('success' in rm and rm['success'])

        self.assertTrue(l.read() == 128)

    def test_read(self):
        "Valid data on read"
        l = LogicInput(8, 97)
        self.assertTrue(l.read() == 97)

    def test_write(self):
        "Exception expected on write"
        l = LogicInput(32, 2600000)

        with self.assertRaises(Exception):
            l.write(152)

    def test_size(self):
        "Valid bus size presented"
        l = LogicInput(16, 56)
        self.assertTrue(l.size() == 16)


if __name__ == '__main__':
    unittest.main()
