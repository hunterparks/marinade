"""
Test core component RegisterFile
"""

import unittest
import sys
sys.path.insert(0,'../../')
from components.core.register_file import RegisterFile, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus import Bus

class RegisterFile_t(unittest.TestCase):
    """
    Test RegisterFile's constructor, inspect, modify, clocking, reset, and run
    functionality.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(1,0)
        wd = Bus(8,10)
        ra = Bus(1,0)
        rd = Bus(8)
        en = Bus(1,0)

        with self.assertRaises(TypeError):
            rgf = RegisterFile('5',8,clk,rst,wa,wd,[ra],[rd],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(0,8,clk,rst,wa,wd,[ra],[rd],en)

        with self.assertRaises(TypeError):
            rgf = RegisterFile(1,'0',clk,rst,wa,wd,[ra],[rd],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(1,0,clk,rst,wa,wd,[ra],[rd],en)

        with self.assertRaises(ValueError):
            rgf = RegisterFile(1,8,clk,rst,wa,wd,[ra],[rd],en,edge_type = 5)
        with self.assertRaises(ValueError):
            rgf = RegisterFile(1,8,clk,rst,wa,wd,[ra],[rd],en,reset_type = 5)
        with self.assertRaises(ValueError):
            rgf = RegisterFile(1,8,clk,rst,wa,wd,[ra],[rd],en,enable_type = 5)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(1,8,clk,rst,wa,wd,[ra],[rd],en,default_state = '5')

        with self.assertRaises(TypeError):
            rgf = RegisterFile(1,8,'clk',rst,wa,wd,[ra],[rd],en)
        with self.assertRaises(TypeError):
            c = Bus(2,1)
            rgf = RegisterFile(1,8,c,rst,wa,wd,[ra],[rd],en)

        with self.assertRaises(TypeError):
            rgf = RegisterFile(1,8,clk,'rst',wa,wd,[ra],[rd],en)
        with self.assertRaises(TypeError):
            r = Bus(2,1)
            rgf = RegisterFile(1,8,clk,r,wa,wd,[ra],[rd],en)

        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,'wa',wd,[ra],[rd],en)
        with self.assertRaises(TypeError):
            w = Bus(4,1)
            rgf = RegisterFile(2,8,clk,rst,w,wd,[ra],[rd],en)

        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,'wd',[ra],[rd],en)
        with self.assertRaises(TypeError):
            w = Bus(4,1)
            rgf = RegisterFile(2,8,clk,rst,wa,w,[ra],[rd],en)

        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,'[ra]',[rd],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],'[rd]',en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,ra,[rd],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],rd,en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[],[],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[],[rd],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,['0'],['0'],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],['0'],en)
        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,['0'],[rd],en)
        with self.assertRaises(TypeError):
            a = Bus(2)
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[a],[rd],en)
        with self.assertRaises(TypeError):
            d = Bus(9)
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[d],en)

        with self.assertRaises(TypeError):
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],'0')
        with self.assertRaises(TypeError):
            e = Bus(2)
            rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],e)

        rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],en)


    def test_inspect(self):
        "Verifies hook inspect for valid return"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(1,0)
        wd = Bus(8,10)
        ra = Bus(1,0)
        rd = Bus(8)
        en = Bus(1,0)

        rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],en)

        rm = rgf.inspect()
        self.assertTrue(rm['type'] == 'register')
        self.assertTrue(rm['length'] == 2)
        self.assertTrue(rm['size'] == 8)
        self.assertTrue(len(rm['state']) == 2)
        self.assertTrue(rm['state'][0] == 0)
        self.assertTrue(rm['state'][1] == 0)


    def test_modify(self):
        "Verifies internal hook modify function"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(1,0)
        wd = Bus(8,10)
        ra = Bus(1,0)
        rd = Bus(8)
        en = Bus(1,0)

        reg = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],en)

        tm = None
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {}
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : '0',
            'data' : []
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : -1,
            'data' : []
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 2,
            'data' : []
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 0,
            'data' : '[]'
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 1,
            'data' : [12,15]
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 0,
            'data' : [12,15,25]
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 0,
            'data' : [256]
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 0,
            'data' : [256,256]
        }
        rm = reg.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start' : 0,
            'data' : [255,255]
        }
        rm = reg.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start' : 0,
            'data' : [15]
        }
        rm = reg.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start' : 1,
            'data' : [25]
        }
        rm = reg.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start' : 0,
            'data' : []
        }
        rm = reg.modify(tm)
        self.assertTrue('success' in rm)


    def test_on_rising_edge(self):
        "Verifies rising edge capture behavior"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(1,0)
        wd = Bus(8,10)
        ra = Bus(1,0)
        rd = Bus(8)
        en = Bus(1,0)

        rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],en, edge_type = Latch_Type.RISING_EDGE)

        # prove that on_rising_edge does not fail on call
        # no further testing is necessary as it is non-functional
        rgf.on_rising_edge()


    def test_on_falling_edge(self):
        "Verifies falling edge capture behavior"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(1,0)
        wd = Bus(8,10)
        ra = Bus(1,0)
        rd = Bus(8)
        en = Bus(1,0)

        rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],en, edge_type = Latch_Type.FALLING_EDGE)

        # prove that on_falling_edge does not fail on call
        # no further testing is necessary as it is non-functional
        rgf.on_falling_edge()


    def test_on_reset(self):
        "Verifies reset behavior of component"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(1,0)
        wd = Bus(8,10)
        ra = Bus(1,0)
        rd = Bus(8)
        en = Bus(1,0)

        rgf = RegisterFile(2,8,clk,rst,wa,wd,[ra],[rd],en, default_state = 55)

        #setup registers to have data
        clk.write(0)
        en.write(1)
        wa.write(0)
        wd.write(25)
        ra.write(0)
        rgf.run()
        self.assertTrue(rd.read() == 55)

        clk.write(1)
        en.write(1)
        wa.write(0)
        wd.write(25)
        ra.write(0)
        rgf.run()
        self.assertTrue(rd.read() == 25)

        clk.write(0)
        en.write(1)
        wa.write(1)
        wd.write(25)
        ra.write(1)
        rgf.run()
        self.assertTrue(rd.read() == 55)

        clk.write(1)
        en.write(1)
        wa.write(1)
        wd.write(25)
        ra.write(1)
        rgf.run()
        self.assertTrue(rd.read() == 25)

        # cause reset event
        rgf.on_reset()

        #verify default state
        en.write(0)
        ra.write(0)
        rgf.run()
        self.assertTrue(rd.read() == 55)
        ra.write(1)
        rgf.run()
        self.assertTrue(rd.read() == 55)


    def test_run(self):
        "Verifies correct time based simulation"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(4,0)
        wd = Bus(8,10)
        ra0 = Bus(4,0)
        ra1 = Bus(4,0)
        rd0 = Bus(8)
        rd1 = Bus(8)
        en = Bus(1,0)

        rgf = RegisterFile(16,8,clk,rst,wa,wd,[ra0,ra1],[rd0,rd1],en)

        #write to each register
        en.write(1)

        for i in range(16):
            wa.write(i)
            wd.write(i+1)
            clk.write(0)
            rgf.run()
            clk.write(1)
            rgf.run()
            clk.write(0)
            rgf.run()

        #read from each register seperate
        for i in range(8):
            ra0.write(i)
            ra1.write(i+8)
            rgf.run()
            self.assertTrue(rd0.read() == i + 1)
            self.assertTrue(rd1.read() == i + 9)

        #read same location to verify data
        for i in range(16):
            ra0.write(i)
            ra1.write(i)
            rgf.run()
            self.assertTrue(rd0.read() == rd1.read())


if __name__ == '__main__':
    unittest.main()
