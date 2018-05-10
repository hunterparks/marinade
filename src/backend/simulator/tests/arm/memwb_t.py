"""
Tests the memwb.py module
Must be run in the marinade/src/backend/simulator/tests/arm
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.memwb import Memwb
from simulator.components.core.bus import Bus
from simulator.components.abstract.sequential import Latch_Type, Logic_States

class Memwb_t(unittest.TestCase):
    "Unit tests for Memwb class"

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        pc4m = Bus(32)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pc4w = Bus(32)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        invalidBusSize = Bus(7)
        invalidBusType = 'w'

        with self.assertRaises(ValueError):
            Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                  regwrw, regsrcw, wd3sw, fw, rdw, invalidBusSize)

        with self.assertRaises(TypeError):
            Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                  regwrw, regsrcw, invalidBusType, fw, rdw, ra3w)

        Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w, regwrw,
              regsrcw, wd3sw, fw, rdw, ra3w)


    def test_on_rising_edge(self):
        "Tests the on_rising_edge method"
        pc4m = Bus(32)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pc4w = Bus(32)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                      regwrw, regsrcw, wd3sw, fw, rdw, ra3w)
        regsrcm.write(1)
        wd3sm.write(1)
        self.assertNotEqual(regsrcm.read(), regsrcw.read())
        self.assertNotEqual(wd3sm.read(), wd3sw.read())
        memwb.on_rising_edge()
        self.assertEqual(regsrcm.read(), regsrcw.read())
        self.assertEqual(wd3sm.read(), wd3sw.read())


    def test_on_falling_edge(self):
        "Tests on_falling_edge method"
        pc4m = Bus(32)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pc4w = Bus(32)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                      regwrw, regsrcw, wd3sw, fw, rdw, ra3w,
                      Latch_Type.FALLING_EDGE)
        pc4m.write(4)
        rdm.write(0x0A000002)
        ra3m.write(5)
        self.assertNotEqual(pc4m.read(), pc4w.read())
        self.assertNotEqual(rdm.read(), rdw.read())
        self.assertNotEqual(ra3m.read(), ra3w.read())
        memwb.on_falling_edge()
        self.assertEqual(pc4m.read(), pc4w.read())
        self.assertEqual(rdm.read(), rdw.read())
        self.assertEqual(ra3m.read(), ra3w.read())


    def test_inspect(self):
        "Tests inspect method"
        pc4m = Bus(32)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pc4w = Bus(32)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                      regwrw, regsrcw, wd3sw, fw, rdw, ra3w)
        wd3sm.write(1)
        fm.write(0xE2889001)
        self.assertEqual(memwb.inspect()['state']['wd3sw'], 0)
        self.assertEqual(memwb.inspect()['state']['fw'], 0)
        memwb.on_rising_edge()
        self.assertEqual(memwb.inspect()['state']['wd3sw'], 1)
        self.assertEqual(memwb.inspect()['state']['fw'], 0xE2889001)


    def test_modify(self):
        "Tests the modify method"
        pc4m = Bus(32)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pc4w = Bus(32)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                      regwrw, regsrcw, wd3sw, fw, rdw, ra3w)
        self.assertEqual(memwb.modify()['error'], 'memwb register cannot be modified')


    def test_run(self):
        "Tests the run method"
        pc4m = Bus(32)
        regwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rdm = Bus(32)
        ra3m = Bus(4)
        clk = Bus(1)
        pc4w = Bus(32)
        regwrw = Bus(1)
        regsrcw = Bus(1)
        wd3sw = Bus(1)
        fw = Bus(32)
        rdw = Bus(32)
        ra3w = Bus(4)

        memwb = Memwb(pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                      regwrw, regsrcw, wd3sw, fw, rdw, ra3w)
        pc4m.write(16)
        wd3sm.write(1)
        rdm.write(0xE3A0C004)
        memwb.run()
        self.assertNotEqual(pc4m.read(), pc4w.read())
        self.assertNotEqual(wd3sm.read(), wd3sw.read())
        self.assertNotEqual(rdm.read(), rdw.read())
        clk.write(1)
        memwb.run()
        self.assertEqual(pc4m.read(), pc4w.read())
        self.assertEqual(wd3sm.read(), wd3sw.read())
        self.assertEqual(rdm.read(), rdw.read())

    def test_from_dict(self):
        "Validates dictionary constructor"

        hooks = OrderedDict({
            "pc4m" : Bus(32),
            "regwrm" : Bus(1),
            "regsrcm" : Bus(1),
            "wd3sm" : Bus(1),
            "fm" : Bus(32),
            "rdm" : Bus(32),
            "ra3m" : Bus(4),
            "clk" : Bus(1),
            "pc4w" : Bus(32),
            "regwrw" : Bus(1),
            "regsrcw" : Bus(1),
            "wd3sw" : Bus(1),
            "fw" : Bus(32),
            "rdw" : Bus(32),
            "ra3w" : Bus(4),
            "enable" : Bus(1)
        })

        config = {
            "pc4m" : "pc4m",
            "regwrm" : "regwrm",
            "regsrcm" : "regsrcm",
            "wd3sm" : "wd3sm",
            "fm" : "fm",
            "rdm" : "rdm",
            "ra3m" : "ra3m",
            "clk" : "clk",
            "pc4w" : "pc4w",
            "regwrw" : "regwrw",
            "regsrcw" : "regsrcw",
            "wd3sw" : "wd3sw",
            "fw" : "fw",
            "rdw" : "rdw",
            "ra3w" : "ra3w",
            "enable" : "enable",
            "edge_type" : "both_edge",
            "enable_type" : "active_low"
        }

        reg = Memwb.from_dict(config,hooks)



if __name__ == '__main__':
    unittest.main()
