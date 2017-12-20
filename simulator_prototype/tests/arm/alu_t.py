import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.alu import Alu
from components.core.bus import Bus

class Alu_t(unittest.TestCase):

    def test_run(self):
        # initialize sizes of input and output busses
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
        # test case 1
        alus.write(0)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 2
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 3)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 3
        alus.write(2)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        # test case 4
        alus.write(3)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 5
        alus.write(4)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 6
        alus.write(5)
        test_alu.run()
        self.assertEqual(f.read(), 5)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 7
        alus.write(6)
        test_alu.run()
        self.assertEqual(f.read(), 2)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 8
        alus.write(7)
        test_alu.run()
        self.assertEqual(f.read(), 1)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        # test case 9
        '''
            Curt - A 'Value out of range for bus' error occurs here
            because of the sign extended number. Need to look
            further into this error
        '''
        a.write(1)
        b.write(2)
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFF)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)

if __name__ == '__main__':
    unittest.main()
