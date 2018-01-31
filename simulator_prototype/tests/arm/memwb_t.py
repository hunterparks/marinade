"""
Tests arm state register memwb
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.memwb import Memwb
from components.core.bus import Bus
from components.abstract.sequential import Latch_Type, Logic_States

class Memwb_t(unittest.TestCase):
    "Unit tests for Memwb class"

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pcsrcw = Bus(2)
        regwrsw = Bus(2)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        invalidBusSize = Bus(7)
        invalidBusType = 'w'

        with self.assertRaises(ValueError):
            memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                            clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                            invalidBusSize)

        with self.assertRaises(TypeError):
            memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                            clk, pcsrcw, regwrsw, regwrw, regsrcw, invalidBusType, 
                            fw, rdw, ra3w)

        memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                        clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                        ra3w)


    def test_on_rising_edge(self):
        "Tests the on_rising_edge method"
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pcsrcw = Bus(2)
        regwrsw = Bus(2)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                        clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                        ra3w)
        regwrsm.write(2)
        regsrcm.write(1)
        wd3sm.write(1)
        self.assertNotEqual(regwrsm.read(), regwrsw.read())
        self.assertNotEqual(regsrcm.read(), regsrcw.read())
        self.assertNotEqual(wd3sm.read(), wd3sw.read())
        memwb.on_rising_edge()
        self.assertEqual(regwrsm.read(), regwrsw.read())
        self.assertEqual(regsrcm.read(), regsrcw.read())
        self.assertEqual(wd3sm.read(), wd3sw.read())


    def test_on_falling_edge(self):
        "Tests on_falling_edge method"
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pcsrcw = Bus(2)
        regwrsw = Bus(2)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                        clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                        ra3w, Latch_Type.FALLING_EDGE)
        pcsrcm.write(2)
        rdm.write(0x0A000002)
        ra3m.write(5)
        self.assertNotEqual(pcsrcm.read(), pcsrcw.read())
        self.assertNotEqual(rdm.read(), rdw.read())
        self.assertNotEqual(ra3m.read(), ra3w.read())
        memwb.on_falling_edge()
        self.assertEqual(pcsrcm.read(), pcsrcw.read())
        self.assertEqual(rdm.read(), rdw.read())
        self.assertEqual(ra3m.read(), ra3w.read())


    def test_inspect(self):
        "Tests inspect method"
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pcsrcw = Bus(2)
        regwrsw = Bus(2)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                        clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                        ra3w)
        wd3sm.write(1)
        fm.write(0xE2889001)
        self.assertEqual(memwb.inspect()['state'].get_state()['wd3sw'], 0)
        self.assertEqual(memwb.inspect()['state'].get_state()['fw'], 0)
        memwb.on_rising_edge()
        self.assertEqual(memwb.inspect()['state'].get_state()['wd3sw'], 1)
        self.assertEqual(memwb.inspect()['state'].get_state()['fw'], 0xE2889001)


    def test_modify(self):
        "Tests the modify method"
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pcsrcw = Bus(2)
        regwrsw = Bus(2)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                        clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                        ra3w)
        self.assertEqual(memwb.modify()['error'], 'memwb register cannot be modified')
        

    def test_run(self):
        "Tests the run method"
        "Tests the modify method"
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pcsrcw = Bus(2)
        regwrsw = Bus(2)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pcsrcm, regwrsm, regwrm, regsrcm, wd3sm, fm, rdm, ra3m,
                        clk, pcsrcw, regwrsw, regwrw, regsrcw, wd3sw, fw, rdw,
                        ra3w)
        pcsrcm.write(2)
        regwrsm.write(1)
        rdm.write(0xE3A0C004)
        memwb.run()
        self.assertNotEqual(pcsrcm.read(), pcsrcw.read())
        self.assertNotEqual(regwrsm.read(), regwrsw.read())
        self.assertNotEqual(rdm.read(), rdw.read())
        clk.write(1)
        memwb.run()
        self.assertEqual(pcsrcm.read(), pcsrcw.read())
        self.assertEqual(regwrsm.read(), regwrsw.read())
        self.assertEqual(rdm.read(), rdw.read())

        

if __name__ == '__main__':
    unittest.main()