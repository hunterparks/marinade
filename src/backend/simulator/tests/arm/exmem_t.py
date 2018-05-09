"""
Tests the exmem.py module
Must be run in the marinade/src/backend/simulator/tests/arm
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.exmem import Exmem
from simulator.components.core.bus import Bus
from simulator.components.abstract.sequential import Latch_Type, Logic_States

class Exmem_t(unittest.TestCase):
    "Unit tests for exmem.py module"

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        pc4e = Bus(32)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pc4m = Bus(32)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        invalidBusSize = Bus(7)
        invalidBusType = 'w'

        with self.assertRaises(ValueError):
            Exmem(pc4e, regwre, memwre, invalidBusSize, wd3se, rd2e, fe, ra3e,
                  clk, pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m)

        with self.assertRaises(TypeError):
            Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                  pc4m, regwrm, memwrm, regsrcm, wd3sm, invalidBusType, rd2m,
                  ra3m)

        Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
              pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m)


    def test_on_rising_edge(self):
        "Tests on_rising_edge method"
        pc4e = Bus(32)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pc4m = Bus(32)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                      pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m)
        memwre.write(1)
        self.assertNotEqual(memwre.read(), memwrm.read())
        exmem.on_rising_edge()
        self.assertEqual(memwre.read(), memwrm.read())


    def test_on_falling_edge(self):
        "Tests on_falling_edge method"
        pc4e = Bus(32)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pc4m = Bus(32)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                      pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m,
                      Latch_Type.FALLING_EDGE)
        memwre.write(1)
        self.assertNotEqual(memwre.read(), memwrm.read())
        exmem.on_falling_edge()
        self.assertEqual(memwre.read(), memwrm.read())


    def test_inspect(self):
        "Tests inspect method"
        pc4e = Bus(32)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pc4m = Bus(32)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                      pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m)
        pc4e.write(24)
        regwre.write(1)
        fe.write(0xEAFFFFFD)
        self.assertEqual(exmem.inspect()['state']['pc4m'], 0)
        self.assertEqual(exmem.inspect()['state']['regwrm'], 0)
        self.assertEqual(exmem.inspect()['state']['fm'], 0)
        exmem.on_rising_edge()
        self.assertEqual(exmem.inspect()['state']['pc4m'], 24)
        self.assertEqual(exmem.inspect()['state']['regwrm'], 1)
        self.assertEqual(exmem.inspect()['state']['fm'], 0xEAFFFFFD)


    def test_modify(self):
        "Tests modify method"
        pc4e = Bus(32)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pc4m = Bus(32)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                      pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m)
        self.assertEqual(exmem.modify()['error'], 'exmem register cannot be modified')


    def test_run(self):
        "Tests the run method"
        pc4e = Bus(32)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pc4m = Bus(32)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pc4e, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                      pc4m, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m)
        rd2e.write(0xE24AA020)
        ra3e.write(4)
        exmem.run()
        self.assertNotEqual(rd2e.read(), rd2m.read())
        self.assertNotEqual(ra3e.read(), ra3m.read())
        clk.write(1)
        exmem.run()
        self.assertEqual(rd2e.read(), rd2m.read())
        self.assertEqual(ra3e.read(), ra3m.read())

    def test_from_dict(self):
        "Validates dictionary constructor"

        hooks = OrderedDict({
            "pc4e" : Bus(32),
            "regwre" : Bus(1),
            "memwre" : Bus(1),
            "regsrce" : Bus(1),
            "wd3se" : Bus(1),
            "rd2e" : Bus(32),
            "fe" : Bus(32),
            "ra3e" : Bus(4),
            "clk" : Bus(1),
            "pc4m" : Bus(32),
            "regwrm" : Bus(1),
            "memwrm" : Bus(1),
            "regsrcm" : Bus(1),
            "wd3sm" : Bus(1),
            "fm" : Bus(32),
            "rd2m" : Bus(32),
            "ra3m" : Bus(4),
            "en" : Bus(1)
        })

        config = {
            "name" : "exmem",
            "type" : "Exmem",
            "pc4e" : "pc4e",
            "regwre" : "regwre",
            "memwre" : "memwre",
            "regsrce" : "regsrce",
            "wd3se" : "wd3se",
            "rd2e" : "rd2e",
            "fe" : "fe",
            "ra3e" : "ra3e",
            "clk" : "clk",
            "pc4m" : "pc4m",
            "regwrm" : "regwrm",
            "memwrm" : "memwrm",
            "regsrcm" : "regsrcm",
            "wd3sm" : "wd3sm",
            "fm" : "fm",
            "rd2m" : "rd2m",
            "ra3m" : "ra3m",
            "enable" : "en",
            "edge_type" : "rising_edge",
            "enable_type" : "active_low"
        }

        reg = Exmem.from_dict(config,hooks)


if __name__ == '__main__':
    unittest.main()
