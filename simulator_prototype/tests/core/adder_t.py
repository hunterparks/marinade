import unittest
import sys
sys.path.insert(0,'../../')
from components.core.adder import Adder
from components.core.constant import Constant
from components.core.bus import Bus

class Adder_t(unittest.TestCase):

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        cin = Constant(1,1)
        c1 = Constant(8,1)
        c2 = Constant(8,254)
        y0 = Bus(8)
        cout = Bus(1)

        with self.assertRaises(TypeError):
            a = Adder('0',c1,c2)
        with self.assertRaises(TypeError):
            a = Adder(-1,c1,c2)

        with self.assertRaises(TypeError):
            a = Adder(8,None,c2)
        with self.assertRaises(TypeError):
            a = Adder(8,c1,None)
        with self.assertRaises(ValueError):
            a = Adder(5,c1,c2)

        with self.assertRaises(TypeError):
            a = Adder(8,c1,c2,'0')
        with self.assertRaises(ValueError):
            y = Bus(5)
            a = Adder(8,c1,c2,y)

        with self.assertRaises(TypeError):
            a = Adder(8,c1,c2,y0,'0')
        with self.assertRaises(ValueError):
            c = Constant(8,5)
            a = Adder(8,c1,c2,y0,c)

        with self.assertRaises(TypeError):
            a = Adder(8,c1,c2,y0,cin,'0')
        with self.assertRaises(ValueError):
            c = Bus(8)
            a = Adder(8,c1,c2,y0,cin,c)

        a = Adder(8,c1,c2,y0,cin,cout)


    def test_run(self):
        "Prove correct combinational output given signals"
        cin = Constant(1,1)
        c1 = Constant(8,1)
        c2 = Constant(8,254)
        y0 = Bus(8)
        cout = Bus(1)

        a = Adder(8,c1,c2,y0,cin,cout)
        a.run()
        self.assertTrue(y0.read() == 0)
        self.assertTrue(cout.read() == 1)

        a.run(50)
        self.assertTrue(y0.read() == 0)
        self.assertTrue(cout.read() == 1)

if __name__ == '__main__':
    unittest.main()