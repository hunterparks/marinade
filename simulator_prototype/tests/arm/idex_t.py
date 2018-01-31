"""
Tests arm state register idex
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.idex import Idex
from components.core.bus import Bus
from components.abstract.sequential import Latch_Type, Logic_States

class Idex_t(unittest.TestCase):
    "Unit tests for idex class"

    def test_constructor(self):
        "Tests constructor with valid and invalid configurations"
        pcsrcd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        rd1d = Bus(32)
        rd2d = Bus(32)
        imm32d = Bus(32)
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3d = Bus(4)
        flush = Bus(1)
        clk = Bus(1)
        pcsrce = Bus(2)
        regwre = Bus(1)
        regwrse = Bus(2)
        alusrcbe = Bus(1)
        aluse = Bus(4)
        aluflagwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd1e = Bus(32)
        rd2e = Bus(32)
        imm32e = Bus(32)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)

        invalidBusSize = Bus(7)
        invalidBusType = 'w'

        with self.assertRaises(ValueError):
            idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                        memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                        ra3d, flush, clk, invalidBusSize, regwrse, regwre, alusrcbe, 
                        aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                        imm32e, ra1e, ra2e, ra3e)

        with self.assertRaises(TypeError):
            idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                        memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                        ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                        aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                        imm32e, ra1e, invalidBusType, ra3e)

        idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                    memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                    ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                    aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                    imm32e, ra1e, ra2e, ra3e)


    def test_on_rising_edge(self):
        "Tests on_rising_edge method"
        pcsrcd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        rd1d = Bus(32)
        rd2d = Bus(32)
        imm32d = Bus(32)
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3d = Bus(4)
        flush = Bus(1)
        clk = Bus(1)
        pcsrce = Bus(2)
        regwre = Bus(1)
        regwrse = Bus(2)
        alusrcbe = Bus(1)
        aluse = Bus(4)
        aluflagwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd1e = Bus(32)
        rd2e = Bus(32)
        imm32e = Bus(32)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)

        idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                    memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                    ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                    aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                    imm32e, ra1e, ra2e, ra3e)
        pcsrcd.write(3)
        self.assertNotEqual(pcsrcd.read(), pcsrce.read())
        idex.on_rising_edge()
        self.assertEqual(pcsrcd.read(), pcsrce.read())


    def test_on_falling_edge(self):
        "Tests on_falling edge method"
        pcsrcd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        rd1d = Bus(32)
        rd2d = Bus(32)
        imm32d = Bus(32)
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3d = Bus(4)
        flush = Bus(1)
        clk = Bus(1)
        pcsrce = Bus(2)
        regwre = Bus(1)
        regwrse = Bus(2)
        alusrcbe = Bus(1)
        aluse = Bus(4)
        aluflagwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd1e = Bus(32)
        rd2e = Bus(32)
        imm32e = Bus(32)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)

        idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                    memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                    ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                    aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                    imm32e, ra1e, ra2e, ra3e, Latch_Type.FALLING_EDGE,
                    Logic_States.ACTIVE_LOW)
        pcsrcd.write(3)
        flush.write(1)
        self.assertNotEqual(pcsrcd.read(), pcsrce.read())
        idex.on_falling_edge()
        self.assertEqual(pcsrcd.read(), pcsrce.read())


    def test_inspect(self):
        "Tests the inspect method"
        pcsrcd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        rd1d = Bus(32)
        rd2d = Bus(32)
        imm32d = Bus(32)
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3d = Bus(4)
        flush = Bus(1)
        clk = Bus(1)
        pcsrce = Bus(2)
        regwre = Bus(1)
        regwrse = Bus(2)
        alusrcbe = Bus(1)
        aluse = Bus(4)
        aluflagwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd1e = Bus(32)
        rd2e = Bus(32)
        imm32e = Bus(32)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)

        idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                    memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                    ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                    aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                    imm32e, ra1e, ra2e, ra3e)
        alusd.write(1)
        self.assertEqual(idex.inspect()['state'].get_state()['aluse'], 0)
        idex.on_rising_edge()
        self.assertEqual(idex.inspect()['state'].get_state()['aluse'], 1)


    def test_modify(self):
        "Tests the modify method"
        pcsrcd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        rd1d = Bus(32)
        rd2d = Bus(32)
        imm32d = Bus(32)
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3d = Bus(4)
        flush = Bus(1)
        clk = Bus(1)
        pcsrce = Bus(2)
        regwre = Bus(1)
        regwrse = Bus(2)
        alusrcbe = Bus(1)
        aluse = Bus(4)
        aluflagwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd1e = Bus(32)
        rd2e = Bus(32)
        imm32e = Bus(32)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)

        idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                    memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                    ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                    aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                    imm32e, ra1e, ra2e, ra3e)
        self.assertEqual(idex.modify()['error'], 'idex register cannot be modified')


    def test_run(self):
        "Tests the run method"
        pcsrcd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        rd1d = Bus(32)
        rd2d = Bus(32)
        imm32d = Bus(32)
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3d = Bus(4)
        flush = Bus(1)
        clk = Bus(1)
        pcsrce = Bus(2)
        regwre = Bus(1)
        regwrse = Bus(2)
        alusrcbe = Bus(1)
        aluse = Bus(4)
        aluflagwre = Bus(1)
        memwre = Bus(1)
        regsrce = Bus(1)
        wd3se = Bus(1)
        rd1e = Bus(32)
        rd2e = Bus(32)
        imm32e = Bus(32)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)

        idex = Idex(pcsrcd, regwrsd, regwrd, alusrcbd, alusd, aluflagwrd,
                    memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d,
                    ra3d, flush, clk, pcsrce, regwrse, regwre, alusrcbe, 
                    aluse, aluflagwre, memwre, regsrce, wd3se, rd1e, rd2e,
                    imm32e, ra1e, ra2e, ra3e)
        regwrsd.write(1)
        rd1d.write(0xE3A0A000)
        ra3d.write(12)
        idex.run()
        self.assertNotEqual(regwrsd.read(), regwrse.read())
        self.assertNotEqual(rd1d.read(), rd1e.read())
        self.assertNotEqual(ra3d.read(), ra3e.read())
        clk.write(1)
        idex.run()
        self.assertEqual(regwrsd.read(), regwrse.read())
        self.assertEqual(rd1d.read(), rd1e.read())
        self.assertEqual(ra3d.read(), ra3e.read())
        clk.write(0)
        idex.run()
        flush.write(1)
        clk.write(1)
        idex.run()
        self.assertNotEqual(regwrsd.read(), regwrse.read())
        self.assertNotEqual(rd1d.read(), rd1e.read())
        self.assertNotEqual(ra3d.read(), ra3e.read())



if __name__ == '__main__':
    unittest.main()