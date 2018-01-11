"""
Tests core component Register
"""

import unittest
import sys
sys.path.insert(0,'../../')
from components.core.register import Register, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus import Bus



class Register_t(unittest.TestCase):
    """
    Tests Register's constructor, inspect, modify, clocking, reset, and run
    functionality.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(2,1)
        q_bus = Bus(2,0)
        en = Bus(1,0)

        with self.assertRaises(TypeError):
            r = Register('0',clk,rst,d_bus)
        with self.assertRaises(TypeError):
            r = Register(0,clk,rst,d_bus)

        with self.assertRaises(TypeError):
            r = Register(2,clk,rst,d_bus,q_bus,'0')
        with self.assertRaises(TypeError):
            r = Register(2,clk,rst,d_bus,q_bus,-1)
        with self.assertRaises(TypeError):
            r = Register(2,clk,rst,d_bus,q_bus,4)

        with self.assertRaises(TypeError):
            r = Register(2,'clk',rst,d_bus,q_bus)
        with self.assertRaises(ValueError):
            c = Bus(2)
            r = Register(2,c,rst,d_bus,q_bus)

        with self.assertRaises(TypeError):
            r = Register(2,clk,'rst',d_bus,q_bus)
        with self.assertRaises(ValueError):
            rs = Bus(2)
            r = Register(2,clk,rs,d_bus,q_bus)

        with self.assertRaises(TypeError):
            r = Register(2,clk,rst,'d_bus',q_bus)
        with self.assertRaises(ValueError):
            d = Bus(3)
            r = Register(2,clk,rst,d,q_bus)

        with self.assertRaises(TypeError):
            r = Register(2,clk,rst,d_bus,q_bus,enable = '0')
        with self.assertRaises(ValueError):
            e = Bus(3)
            r = Register(2,clk,rst,d,q_bus,enable = e)

        with self.assertRaises(TypeError):
            r = Register(2,clk,rst,d_bus,'q_bus')
        with self.assertRaises(ValueError):
            q = Bus(3)
            r = Register(2,clk,rst,d_bus,q)

        with self.assertRaises(ValueError):
            r = Register(2,clk,rst,d_bus,q_bus,edge_type = 5)

        with self.assertRaises(ValueError):
            r = Register(2,clk,rst,d_bus,q_bus,reset_type = 5)

        with self.assertRaises(ValueError):
            r = Register(2,clk,rst,d_bus,q_bus,enable_type = 5)

        reg = Register(2,clk,rst,d_bus,q_bus,0,Latch_Type.BOTH_EDGE,
                       Logic_States.ACTIVE_LOW,en,Logic_States.ACTIVE_LOW)


    def test_rising_edge(self):
        "Verifies rising edge capture behavior"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,10)
        q_bus = Bus(8,0)
        reg = Register(8,clk,rst,d_bus,q_bus,0,Latch_Type.RISING_EDGE,
                       Logic_States.ACTIVE_HIGH)

        reg.run()
        self.assertTrue(q_bus.read() == 0)

        d_bus.write(15)
        reg.on_rising_edge()
        reg.run()
        self.assertTrue(q_bus.read() == 15)

        d_bus.write(25)
        reg.on_falling_edge()
        reg.run()
        self.assertTrue(q_bus.read() == 15)


    def test_falling_edge(self):
        "Verifies falling edge capture behavior"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,10)
        q_bus = Bus(8,0)
        reg = Register(8,clk,rst,d_bus,q_bus,0,Latch_Type.FALLING_EDGE,
                       Logic_States.ACTIVE_HIGH)

        reg.run()
        self.assertTrue(q_bus.read() == 0)

        d_bus.write(15)
        reg.on_falling_edge()
        reg.run()
        self.assertTrue(q_bus.read() == 15)

        d_bus.write(25)
        reg.on_rising_edge()
        reg.run()
        self.assertTrue(q_bus.read() == 15)


    def test_both_edges(self):
        "Verifies both edge capture behavior"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,10)
        q_bus = Bus(8,0)
        reg = Register(8,clk,rst,d_bus,q_bus,0,Latch_Type.BOTH_EDGE,
                       Logic_States.ACTIVE_HIGH)

        reg.run()
        self.assertTrue(q_bus.read() == 0)

        d_bus.write(15)
        reg.on_falling_edge()
        reg.run()
        self.assertTrue(q_bus.read() == 15)

        d_bus.write(25)
        reg.on_rising_edge()
        reg.run()
        self.assertTrue(q_bus.read() == 25)


    def test_reset(self):
        "Verifies reset behavior of component"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,10)
        q_bus = Bus(8,0)
        reg = Register(8,clk,rst,d_bus,q_bus,0,Latch_Type.RISING_EDGE,
                       Logic_States.ACTIVE_HIGH)

        clk.write(0)
        reg.run()
        self.assertTrue(q_bus.read() == 0)

        clk.write(1)
        reg.run()
        self.assertTrue(q_bus.read() == 10)

        reg.on_reset()
        reg.run()
        self.assertTrue(q_bus.read() == 0)


    def test_inspect(self):
        "Verifies hook inspect for valid return"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,0)
        q_bus = Bus(8,0)
        reg = Register(8,clk,rst,d_bus,q_bus,1)

        ins = reg.inspect()
        self.assertTrue(ins['type'] == 'register')
        self.assertTrue(ins['size'] == 8)
        self.assertTrue(ins['state'] == 1)


    def test_modify(self):
        "Verifies internal hook modify function"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,0)
        q_bus = Bus(8,0)
        reg = Register(8,clk,rst,d_bus,q_bus,1)

        tm = None
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {}
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'state' : '0'
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'state' : -1
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'state' : 256
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'state' : 128
        }
        rm = reg.modify(tm)
        self.assertTrue('success' in rm and rm['success'])
        reg.run()
        self.assertTrue(q_bus.read() == 128)


    def test_run(self):
        "Verifies correct time based simulation"
        clk = Bus(1,0)
        rst = Bus(1,0)
        d_bus = Bus(8,10)
        q_bus = Bus(8,0)
        en = Bus(1,0)
        reg = Register(8,clk,rst,d_bus,q_bus,0,Latch_Type.RISING_EDGE,
                       Logic_States.ACTIVE_HIGH,en,Logic_States.ACTIVE_HIGH)

        en.write(0)
        clk.write(0)
        reg.run()
        self.assertTrue(q_bus.read() == 0)

        en.write(1)
        clk.write(0)
        reg.run()
        self.assertTrue(q_bus.read() == 0)

        en.write(0)
        clk.write(1)
        reg.run()
        self.assertTrue(q_bus.read() == 0)

        en.write(1)
        clk.write(1)
        reg.run()
        self.assertTrue(q_bus.read() == 0)

        clk.write(0)
        reg.run()
        self.assertTrue(q_bus.read() == 0)

        clk.write(1)
        reg.run()
        self.assertTrue(q_bus.read() == 10)

        d_bus.write(15)
        clk.write(0)
        reg.run()
        self.assertTrue(q_bus.read() == 10)

        rst.write(1)
        clk.write(1)
        reg.run()
        self.assertTrue(q_bus.read() == 0)


if __name__ == '__main__':
    unittest.main()
