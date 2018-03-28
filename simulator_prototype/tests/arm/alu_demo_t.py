"""
Tests arm component Alu
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.alu_demo import Alu
from components.core.bus import Bus


class Alu_t(unittest.TestCase):
    """
    Tests Alu's constructor and run functionality
    """

    def test_constructor(self):
        """
        tests 2 bad constructors - not all possible constructors tested
        """

        a = Bus(31)
        b = Bus(32)
        alus = Bus(4)
        f = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        # test case 1
        with self.assertRaises(ValueError):
            test_alu = Alu(a, b, alus, f, c, v, n, z)
        # test case 2
        with self.assertRaises(ValueError):
            test_alu = Alu(a, b, alus, c, f, v, n, z)

    def test_run(self):
        """
        test's the alu's run function
        """

        a = Bus(32)
        b = Bus(32)
        alus = Bus(4)
        f = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        # initialize alu
        test_alu = Alu(a, b, alus, f, c, v, n, z)
        # initialize inputs with values
        a.write(5)
        b.write(2)
        # test case 3
        alus.write(0)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 4
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 3)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 5
        alus.write(2)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 6
        alus.write(3)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 7
        alus.write(4)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 8
        alus.write(5)
        test_alu.run()
        self.assertEqual(f.read(), 5)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 9
        alus.write(6)
        test_alu.run()
        self.assertEqual(f.read(), 2)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 10
        alus.write(7)
        test_alu.run()
        self.assertEqual(f.read(), 10)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 11
        alus.write(8)
        test_alu.run()
        self.assertEqual(f.read(), 1)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 12
        a.write(1)
        b.write(2)
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFF)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)
        # test case 13
        a.write(0x80000000)
        b.write(0x80000000)
        alus.write(0)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 1)
        # test case 14
        a.write(0x7FFFFFFF)
        b.write(0xFFFFFFFF)
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 0x80000000)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 1)
        # test case 15
        a.write(268435456)
        b.write(9)
        alus.write(7)
        test_alu.run()
        self.assertEqual(f.read(), 2415919104)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 1)


if __name__ == '__main__':
    unittest.main()
