"""
Tests core component Clock
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.core.clock import Clock
import limits


class Clock_t(unittest.TestCase):
    """
    Tests Clock component's constructor, read, write, generate, inspect, size
    and run functionality.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        with self.assertRaises(TypeError):
            l = Clock('8')
        with self.assertRaises(ValueError):
            l = Clock(-1)
        with self.assertRaises(ValueError):
            l = Clock(limits.MIN_FREQUENCY - 1)
        with self.assertRaises(ValueError):
            l = Clock(limits.MAX_FREQUENCY + 1)

        valid_f = (limits.MAX_FREQUENCY - limits.MIN_FREQUENCY) / 2
        with self.assertRaises(TypeError):
            l = Clock(valid_f, '8')
        with self.assertRaises(TypeError):
            l = Clock(valid_f, -1)
        with self.assertRaises(TypeError):
            l = Clock(valid_f, 2)

        l = Clock(limits.MIN_FREQUENCY, 1)
        self.assertTrue(l.size() == 1 and l.read() == 1 and l.frequency() == limits.MIN_FREQUENCY)
        l = Clock(limits.MAX_FREQUENCY)
        self.assertTrue(l.size() == 1 and l.read() == 0 and l.frequency() == limits.MAX_FREQUENCY)

    def test_inspect(self):
        "Check inspect for valid data presentation"
        l = Clock(10)
        ins = l.inspect()
        self.assertTrue(ins['type'] == 'clock')
        self.assertTrue(ins['size'] == 1)
        self.assertTrue(ins['state'] == 0)
        self.assertTrue(ins['frequency'] == 10)

    def test_generate(self):
        "Check generate handler for valid and invalid message"
        l = Clock(50)

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
            'state': 2
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'state': 1
        }
        rm = l.generate(m)
        self.assertTrue('success' in rm and rm['success'])

        self.assertTrue(l.read() == 1)

        m = {
            'frequency': limits.MAX_FREQUENCY + 1
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'frequency': limits.MIN_FREQUENCY - 1
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'frequency': '0'
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'frequency': '0',
            'state': '0'
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)

        m = {
            'frequency': 10,
            'state': '0'
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)
        self.assertFalse(l.frequency() == 10)
        self.assertTrue(l.read() == 1)

        m = {
            'frequency': '10',
            'state': 0
        }
        rm = l.generate(m)
        self.assertTrue('error' in rm)
        self.assertFalse(l.frequency() == 10)
        self.assertTrue(l.read() == 1)

        m = {
            'frequency': 10,
            'state': 0
        }
        rm = l.generate(m)
        self.assertTrue('success' in rm and rm['success'])
        self.assertTrue(l.frequency() == 10)
        self.assertTrue(l.read() == 0)

    def test_read(self):
        "Valid data on read"
        l = Clock(10)
        self.assertTrue(l.read() == 0)

    def test_write(self):
        "Exception expected on write"
        l = Clock(100)

        with self.assertRaises(Exception):
            l.write(1)

    def test_size(self):
        "Valid bus size presented"
        l = Clock(50)
        self.assertTrue(l.size() == 1)

    def test_run(self):
        "Verifies correct time based simulation"
        c = Clock(1, 0)  # 1Hz

        c.run(0)
        self.assertTrue(c.read() == 0)

        c.run(0.25)
        self.assertTrue(c.read() == 0)

        c.run(0.50)
        self.assertTrue(c.read() == 1)

        c.run(0.75)
        self.assertTrue(c.read() == 1)

        c.run(1.00)
        self.assertTrue(c.read() == 0)

        c.run(1.50)
        self.assertTrue(c.read() == 1)

        c.run(2)
        self.assertTrue(c.read() == 0)


if __name__ == '__main__':
    unittest.main()
