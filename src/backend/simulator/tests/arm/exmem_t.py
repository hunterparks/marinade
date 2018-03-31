"""
Tests arm state register exmem
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.arm.exmem import Exmem
from simulator.components.core.bus import Bus
from simulator.components.abstract.sequential import Latch_Type, Logic_States

class Exmem_t(unittest.TestCase):
    "Unit tests for exmem class"

    def test_constructor(self):
        "Tests constructor with valid and invalid configuration"
        pcsrce = Bus(2)
        regwrse = Bus(2)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
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
            exmem = Exmem(pcsrce, regwrse, regwre, memwre, invalidBusSize, wd3se, rd2e,
                            fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                            regsrcm, wd3sm, fm, rd2m, ra3m)

        with self.assertRaises(TypeError):
            exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                            fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                            regsrcm, wd3sm, invalidBusType, rd2m, ra3m)

        exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                        fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                        regsrcm, wd3sm, fm, rd2m, ra3m)


    def test_on_rising_edge(self):
        "Tests on_rising_edge method"
        pcsrce = Bus(2)
        regwrse = Bus(2)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                        fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                        regsrcm, wd3sm, fm, rd2m, ra3m)
        memwre.write(1)
        self.assertNotEqual(memwre.read(), memwrm.read())
        exmem.on_rising_edge()
        self.assertEqual(memwre.read(), memwrm.read())


    def test_on_falling_edge(self):
        "Tests on_falling_edge method"
        pcsrce = Bus(2)
        regwrse = Bus(2)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                        fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                        regsrcm, wd3sm, fm, rd2m, ra3m,
                        Latch_Type.FALLING_EDGE)
        memwre.write(1)
        self.assertNotEqual(memwre.read(), memwrm.read())
        exmem.on_falling_edge()
        self.assertEqual(memwre.read(), memwrm.read())


    def test_inspect(self):
        "Tests inspect method"
        pcsrce = Bus(2)
        regwrse = Bus(2)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                        fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                        regsrcm, wd3sm, fm, rd2m, ra3m)
        pcsrce.write(1)
        regwrse.write(1)
        fe.write(0xEAFFFFFD)
        self.assertEqual(exmem.inspect()['state'].get_state()['pcsrcm'], 0)
        self.assertEqual(exmem.inspect()['state'].get_state()['regwrsm'], 0)
        self.assertEqual(exmem.inspect()['state'].get_state()['fm'], 0)
        exmem.on_rising_edge()
        self.assertEqual(exmem.inspect()['state'].get_state()['pcsrcm'], 1)
        self.assertEqual(exmem.inspect()['state'].get_state()['regwrsm'], 1)
        self.assertEqual(exmem.inspect()['state'].get_state()['fm'], 0xEAFFFFFD)


    def test_modify(self):
        "Tests modify method"
        pcsrce = Bus(2)
        regwrse = Bus(2)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                        fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                        regsrcm, wd3sm, fm, rd2m, ra3m)
        self.assertEqual(exmem.modify()['error'], 'exmem register cannot be modified')


    def test_run(self):
        "Tests the run method"
        pcsrce = Bus(2)
        regwrse = Bus(2)
        regwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd2e = Bus(32)
        fe = Bus(32)
        ra3e = Bus(4)
        clk = Bus(1)
        pcsrcm = Bus(2)
        regwrsm = Bus(2)
        regwrm = Bus(1)
        memwrm = Bus(1)
        regsrcm = Bus(1)
        wd3sm = Bus(1)
        fm = Bus(32)
        rd2m = Bus(32)
        ra3m = Bus(4)

        exmem = Exmem(pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e,
                        fe, ra3e, clk, pcsrcm, regwrsm, regwrm, memwrm,
                        regsrcm, wd3sm, fm, rd2m, ra3m)
        rd2e.write(0xE24AA020)
        ra3e.write(4)
        exmem.run()
        self.assertNotEqual(rd2e.read(), rd2m.read())
        self.assertNotEqual(ra3e.read(), ra3m.read())
        clk.write(1)
        exmem.run()
        self.assertEqual(rd2e.read(), rd2m.read())
        self.assertEqual(ra3e.read(), ra3m.read())



if __name__ == '__main__':
    unittest.main()
