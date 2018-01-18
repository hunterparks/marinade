"""
Tests core component Mux
"""

import unittest
import sys
sys.path.insert(0,'../../')
from components.core.mux import Mux
from components.core.constant import Constant
from components.core.bus import Bus



class Mux_t(unittest.TestCase):
    """
    Tests Mux component's constructor and run functionality
    Additionally, checks bound conditions.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        c0 = Constant(8,150)
        c1 = Constant(8,5)
        c2 = Constant(8,255)
        s = Bus(2,0)
        y = Bus(8,1)

        with self.assertRaises(TypeError):
            m = Mux('0',[c0,c1,c2],s,y)
        with self.assertRaises(TypeError):
            m = Mux(0,[c0,c1,c2],s,y)

        with self.assertRaises(TypeError):
            m = Mux(8,None,s,y)
        with self.assertRaises(TypeError):
            m = Mux(8,[],s,y)
        with self.assertRaises(TypeError):
            m = Mux(8,[None],s,y)
        with self.assertRaises(TypeError):
            m = Mux(8,['0','1','2'],s,y)
        with self.assertRaises(TypeError):
            c = Constant(1,0)
            m = Mux(8,[c1,c0,c],s,y)

        with self.assertRaises(TypeError):
            m = Mux(8,[c1,c0],None,y)
        with self.assertRaises(ValueError):
            s0 = Bus(8,0)
            m = Mux(8,[c1,c0],s0,y)
        with self.assertRaises(ValueError):
            m = Mux(8,[c1,c0],s,y)

        with self.assertRaises(TypeError):
            m = Mux(8,[c1,c0,c2],s,'0')
        with self.assertRaises(ValueError):
            y0 = Bus(2)
            m = Mux(8,[c1,c0,c2],s,y0)

        m = Mux(8,[c0,c1,c2],s,y)
        m = Mux(8,[c0,c1,c2],s)


    def test_run(self):
        "Prove correct combinational output given signals"
        c0 = Constant(8,150)
        c1 = Constant(8,5)
        c2 = Constant(8,255)
        s = Bus(2,0)
        y = Bus(8,1)

        m = Mux(8,[c0,c1,c2],s,y)
        m.run()
        self.assertTrue(y.read() == c0.read())

        s.write(1)
        m.run()
        self.assertTrue(y.read() == c1.read())

        s.write(2)
        m.run()
        self.assertTrue(y.read() == c2.read())

        s.write(3)
        m.run()
        self.assertTrue(y.read() == 0)

        s.write(0)
        m = Mux(8,[c0,c1,c2],s)
        m.run()


    def test_out_of_bounds(self):
        "Test for valid control signal that extends past defined"
        c0 = Constant(8,150)
        c1 = Constant(8,5)
        c2 = Constant(8,255)
        s = Bus(2,0)
        y = Bus(8,1)

        m = Mux(8,[c0,c1,c2],s,y)
        s.write(3)
        m.run()

        self.assertTrue(y.read() == 0) # prove valid overflow


    def test_large_mux(self):
        "Test mux for large size to validate scaling algorithm"
        c0 = Constant(8,150)
        c1 = Constant(8,5)
        c2 = Constant(8,255)
        c3 = Constant(8,150)
        c4 = Constant(8,5)
        c5 = Constant(8,255)
        c6 = Constant(8,150)
        c7 = Constant(8,5)
        s = Bus(3,0)
        y = Bus(8,1)
        m = Mux(8,[c0,c1,c2,c3,c4,c5,c6],s,y)

        c8 = Constant(8,255)
        s = Bus(4,0)
        m = Mux(8,[c0,c1,c2,c3,c4,c5,c6,c7,c8],s,y)


if __name__ == '__main__':
    unittest.main()
