import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.core.reset import Reset


class Reset_t(unittest.TestCase):

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        with self.assertRaises(TypeError):
            l = Reset('8')
        with self.assertRaises(TypeError):
            l = Reset(-1)
        with self.assertRaises(TypeError):
            l = Reset(2)
        l = Reset(1)
        self.assertTrue(l.size() == 1 and l.read() == 1)
        l = Reset()
        self.assertTrue(l.size() == 1 and l.read() == 0)

    def test_inspect(self):
        "Check inspect for valid data presentation"
        l = Reset(1)
        ins = l.inspect()
        self.assertTrue(ins['type'] == 'reset')
        self.assertTrue(ins['size'] == 1)
        self.assertTrue(ins['state'] == 1)

    def test_generate(self):
        "Check generate handler for valid and invalid message"
        l = Reset()

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
            'reset': False
        }
        rm = l.generate(m)
        self.assertTrue('success' in rm and rm['success'])
        self.assertTrue(l.read() == 0)

        m = {
            'reset': True
        }
        rm = l.generate(m)
        self.assertTrue('success' in rm and rm['success'])
        self.assertTrue(l.read() == 1)

    def test_read(self):
        "Valid data on read"
        l = Reset()
        self.assertTrue(l.read() == 0)

    def test_write(self):
        "Exception expected on write"
        l = Reset()

        with self.assertRaises(Exception):
            l.write(1)

    def test_size(self):
        "Valid bus size presented"
        l = Reset()
        self.assertTrue(l.size() == 1)


if __name__ == '__main__':
    unittest.main()
