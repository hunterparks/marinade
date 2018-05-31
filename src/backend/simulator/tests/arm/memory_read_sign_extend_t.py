"""
Tests arm component MemoryReadSignExtender
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.memory_read_sign_extend import MemoryReadSignExtender
from simulator.components.core.bus import Bus

class MemoryReadSignExtender_t(unittest.TestCase):
    """
    Tests MemoryReadSignExtender's constructor and run functionality
    """

    def test_constructor(self):
        """
        Tests constructors
        """
        x = Bus(32)
        s = Bus(2)
        y = Bus(32)

        # invalid construction
        with self.assertRaises(TypeError):
            mrse = MemoryReadSignExtender('x',s,y)

        with self.assertRaises(ValueError):
            a = Bus(31)
            mrse = MemoryReadSignExtender(a,s,y)

        with self.assertRaises(TypeError):
            mrse = MemoryReadSignExtender(x,'s',y)

        with self.assertRaises(ValueError):
            a = Bus(3)
            mrse = MemoryReadSignExtender(x,a,y)

        with self.assertRaises(TypeError):
            mrse = MemoryReadSignExtender(x,s,'y')

        with self.assertRaises(ValueError):
            a = Bus(33)
            mrse = MemoryReadSignExtender(x,s,a)

        #valid construction
        mrse = MemoryReadSignExtender(x,s,y)

    def test_run(self):
        """
        Test combinational run behavior
        """
        x = Bus(32)
        s = Bus(2)
        y = Bus(32)
        mrse = MemoryReadSignExtender(x,s,y)

        # disabled extend (pass through)
        x.write(0xFF)
        s.write(0)
        mrse.run()
        self.assertEqual(y.read(),0xFF)

        # disabled extend (pass through)
        x.write(0xF2C8FF)
        s.write(2)
        mrse.run()
        self.assertEqual(y.read(),0xF2C8FF)

        # enable extend byte
        x.write(0x2CAE)
        s.write(1)
        mrse.run()
        self.assertEqual(y.read(),0xFFFFFFAE)

        x.write(0x2C5E)
        s.write(1)
        mrse.run()
        self.assertEqual(y.read(),0x5E)

        #enable extend half-word
        x.write(0x34ACAE)
        s.write(3)
        mrse.run()
        self.assertEqual(y.read(),0xFFFFACAE)

        x.write(0xF2C5E)
        s.write(3)
        mrse.run()
        self.assertEqual(y.read(),0x2C5E)

    def test_from_dict(self):
        "Validates dictionary constructor"

        hooks = OrderedDict({
            "i" : Bus(32),
            "c" : Bus(2),
            "o" : Bus(32)
        })

        config = {
            "input" : "i",
            "ctrl" : "c",
            "output" : "o"
        }

        ext = MemoryReadSignExtender.from_dict(config,hooks)


if __name__ == '__main__':
    unittest.main()
