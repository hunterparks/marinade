"""
Tests the controller_pipeline.py module
Must be run in the marinade/src/backend/simulator/tests/arm
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.controller_pipeline import ControllerPipeline
from simulator.components.core.bus import Bus


class ControllerSingleCycle_t(unittest.TestCase):
    """
    Unit test for controller_pipeline.py module
    """

    def test_constructor(self):
        "Tests 4 bad constructors - not all possible constructors tested"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        stalld = Bus(1)
        pcsrcd = Bus(2)
        pcwrd = Bus(1)
        regsad = Bus(1)
        regdstd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        extsd = Bus(2)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)

        # test case 1
        with self.assertRaises(ValueError):
            ControllerPipeline(cond, funct, op, rd, bit4, c, v, n, z, stalld,
                               pcsrcd, pcwrd, regsad, regdstd, regwrsd, regwrd,
                               extsd, alusrcbd, alusd, aluflagwrd, memwrd,
                               regsrcd, wd3sd)
        # test case 2
        with self.assertRaises(ValueError):
            ControllerPipeline(cond, op, bit4, rd, funct, c, v, n, z, stalld,
                               pcsrcd, pcwrd, regsad, regdstd, regwrsd, regwrd,
                               extsd, alusrcbd, alusd, aluflagwrd, memwrd,
                               regsrcd, wd3sd)
        # test case 3
        with self.assertRaises(ValueError):
            ControllerPipeline(cond, op, funct, rd, bit4, c, v, n, z, stalld,
                               pcsrcd, pcwrd, regsad, regdstd, regwrd, regwrsd,
                               extsd, alusrcbd, aluflagwrd, alusd, memwrd,
                               regsrcd, wd3sd)
        # test case 4
        with self.assertRaises(ValueError):
            ControllerPipeline(cond, op, funct, rd, bit4, c, v, n, z, stalld,
                               pcsrcd, pcwrd, regsad, regdstd, regwrd, regwrsd,
                               alusrcbd, extsd, alusd, aluflagwrd, memwrd,
                               regsrcd, wd3sd)


    def test_run(self):
        "Tests the pipeline processors run method"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        stalld = Bus(1)
        pcsrcd = Bus(2)
        pcwrd = Bus(1)
        regsad = Bus(1)
        regdstd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        extsd = Bus(2)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)
        # initialize single cycle controller
        pp = ControllerPipeline(cond, op, funct, rd, bit4, c, v, n, z, stalld,
                                pcsrcd, pcwrd, regsad, regdstd, regwrsd,
                                regwrd, extsd, alusrcbd, alusd, aluflagwrd,
                                memwrd, regsrcd, wd3sd)
        # pcsrcd tests
        # test case 4 - occurs for banch instructions where condition is met
        op.write(2)
        cond.write(1)
        pp.run()
        self.assertEqual(pcsrcd.read(), 0)
        # test case 5 - occurs when a data processing instruction modifies pc
        op.write(0)
        rd.write(15)
        pp.run()
        self.assertEqual(pcsrcd.read(), 2)
        # test case 6 - for pc+4
        op.write(1)
        pp.run()
        self.assertEqual(pcsrcd.read(), 1)
        # pcwrd
        # test case 7 - always write
        self.assertEqual(pcwrd.read(), 1)
        # regsad
        # test case 8 - used to select Rn register (mul instruction)
        op.write(0)
        bit4.write(1)
        funct.write(1)
        pp.run()
        self.assertEqual(regsad.read(), 0)
        # test case 9 - used to select Rn register (data processing instuction)
        op.write(1)
        pp.run()
        self.assertEqual(regsad.read(), 1)
        # regdstd
        # test case 10 - used to select Rd register (str instruction)
        op.write(1)
        funct.write(24)
        pp.run()
        self.assertEqual(regdstd.read(), 2)
        # test case 11 - used to select Rm register (data processing instruction)
        op.write(0)
        bit4.write(1)
        funct.write(0)
        pp.run()
        self.assertEqual(regdstd.read(), 0)
        # test case 12 - used to select Rm register (mul instruction)
        op.write(2)
        pp.run()
        self.assertEqual(regdstd.read(), 1)
        # regwrsd
        # test cast 13 - used to select lr instruction (bl instruction)
        op.write(2)
        funct.write(16)
        pp.run()
        self.assertEqual(regwrsd.read(), 2)
        # test case 14 - used to select Rd register (data processing instruction)
        op.write(0)
        bit4.write(1)
        funct.write(0)
        pp.run()
        self.assertEqual(regwrsd.read(), 0)
        # test case 15 - used to selcet Rd resister (mul instruction)
        op.write(1)
        pp.run()
        self.assertEqual(regwrsd.read(), 1)
        # regwrd
        # test case 16 - occurs when an instruction writes back to the regfile
        op.write(0)
        funct.write(53)
        pp.run()
        self.assertEqual(regwrd.read(), 0)
        # test case 17 - occurs when an instruction writes back to the regfile
        op.write(1)
        funct.write(24)
        pp.run()
        self.assertEqual(regwrd.read(), 0)
        # test case 18 - occurs when an instruction writes back to the regfile
        op.write(2)
        funct.write(0b101100)
        pp.run()
        self.assertEqual(regwrd.read(), 0)
        # test case 19 - occurs when an instruction writes back to the regfile
        funct.write(0b010000)
        pp.run()
        self.assertEqual(regwrd.read(), 1)
        # extsd
        # test case 20 - used for branch instruction
        op.write(2)
        pp.run()
        self.assertEqual(extsd.read(), 2)
        # test case 21 - used for 12-bit immediate (ldr and str instructions)
        op.write(1)
        funct.write(25)
        pp.run()
        self.assertEqual(extsd.read(), 1)
        # test case 22 - used for 8-bit immediate (data processing immediate)
        op.write(0)
        pp.run()
        self.assertEqual(extsd.read(), 0)
        # alusrcbd
        # test case 23 - occurs when source b requires the output to the rd2 register
        # (data processing instruction)
        op.write(0)
        funct.write(28)
        pp.run()
        self.assertEqual(alusrcbd.read(), 1)
        # test case 24 - occurs when source b requires the output to the rd2 register
        # (data processing instruction)
        op.write(0)
        bit4.write(1)
        funct.write(1)
        pp.run()
        self.assertEqual(alusrcbd.read(), 1)
        # test case 25 - occurs when source b requires an exdended immediate
        op.write(0)
        funct.write(63)
        pp.run()
        self.assertEqual(alusrcbd.read(), 0)
        # test case 26 - occurs when source b requires an exdended immediate
        op.write(1)
        pp.run()
        self.assertEqual(alusrcbd.read(), 0)
        # alusd
        # test case 27 - + operation
        op.write(0)
        funct.write(8)
        pp.run()
        self.assertEqual(alusd.read(), 0)
        # test case 28 - + operation
        op.write(1)
        funct.write(25)
        pp.run()
        self.assertEqual(alusd.read(), 0)
        # test case 29 - - operation
        op.write(0)
        funct.write(21)
        pp.run()
        self.assertEqual(alusd.read(), 1)
        # test case 30 - and operation
        op.write(0)
        funct.write(32)
        pp.run()
        self.assertEqual(alusd.read(), 2)
        # test case 31 - or operation
        op.write(0)
        funct.write(25)
        pp.run()
        self.assertEqual(alusd.read(), 3)
        # test case 32 - xor operation
        op.write(0)
        funct.write(35)
        pp.run()
        self.assertEqual(alusd.read(), 4)
        # test case 33 - return B
        op.write(0)
        funct.write(26)
        pp.run()
        self.assertEqual(alusd.read(), 6)
        # test case 34 - * operation
        op.write(0)
        funct.write(1)
        pp.run()
        self.assertEqual(alusd.read(), 7)
        # test case 35 - return 1
        op.write(2)
        pp.run()
        self.assertEqual(alusd.read(), 15)
        # aluflagwrd
        # test case 36 - set c, v, n, z flags (cmp instructions or s bit set)
        op.write(0)
        funct.write(15)
        pp.run()
        self.assertEqual(aluflagwrd.read(), 1)
        # test case 37 - flags will not be set
        op.write(0)
        funct.write(0)
        pp.run()
        self.assertEqual(aluflagwrd.read(), 0)
        # test case 38 - flags will not be set
        op.write(1)
        pp.run()
        self.assertEqual(aluflagwrd.read(), 0)
        # memwrd
        # test case 39 - allows data to be written to data memory (str instructions)
        op.write(1)
        funct.write(24)
        pp.run()
        self.assertEqual(memwrd.read(), 1)
        # test case 40 - cannot write to data memory
        op.write(0)
        pp.run()
        self.assertEqual(memwrd.read(), 0)
        # regsrcd
        # test case 41 - occurs when output of alu is feedback (ldr instructions)
        op.write(1)
        funct.write(25)
        pp.run()
        self.assertEqual(regsrcd.read(), 0)
        # test case 42 - occurs when output of data memory is feedback
        op.write(0)
        pp.run()
        self.assertEqual(regsrcd.read(), 1)
        # wd3sd
        # test case 43 - occurs when a bl is run
        op.write(2)
        funct.write(24)
        pp.run()
        self.assertEqual(wd3sd.read(), 1)
        # test case 44 - occurs for all non bl instructions
        op.write(0)
        pp.run()
        self.assertEqual(wd3sd.read(), 0)


    def test_inspect(self):
        "Tests the single cycle processors inspect method"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        stalld = Bus(1)
        pcsrcd = Bus(2)
        pcwrd = Bus(1)
        regsad = Bus(1)
        regdstd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        extsd = Bus(2)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)

        # initialize single cycle controller
        pp = ControllerPipeline(cond, op, funct, rd, bit4, c, v, n, z, stalld, pcsrcd, pcwrd,
                                    regsad, regdstd, regwrsd, regwrd, extsd, alusrcbd, alusd,
                                    aluflagwrd, memwrd, regsrcd, wd3sd)
        ins = pp.inspect()
        self.assertTrue(ins['type'] == 'pipeline-controller')
        self.assertTrue(ins['state'] is None)


    def test_modify(self):
        "Tests the single cycle processor inspect method"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        stalld = Bus(1)
        pcsrcd = Bus(2)
        pcwrd = Bus(1)
        regsad = Bus(1)
        regdstd = Bus(2)
        regwrsd = Bus(2)
        regwrd = Bus(1)
        extsd = Bus(2)
        alusrcbd = Bus(1)
        alusd = Bus(4)
        aluflagwrd = Bus(1)
        memwrd = Bus(1)
        regsrcd = Bus(1)
        wd3sd = Bus(1)

        # initialize single cycle controller
        pp = ControllerPipeline(cond, op, funct, rd, bit4, c, v, n, z, stalld, pcsrcd, pcwrd,
                                    regsad, regdstd, regwrsd, regwrd, extsd, alusrcbd, alusd,
                                    aluflagwrd, memwrd, regsrcd, wd3sd)

        mod = pp.modify(None)
        # modify is not implemented for controller
        self.assertTrue('error' in mod)

        mod = pp.modify({'state': 0})
        # modify is not implemented for controller
        self.assertTrue('error' in mod)

    def test_from_dict(self):
        "Validates dictionary constructor"

        hooks = OrderedDict({
            "cond" : Bus(4),
            "op" : Bus(2),
            "funct" : Bus(6),
            "rd" : Bus(4),
            "bit4" : Bus(1),
            "c" : Bus(1),
            "v" : Bus(1),
            "n" : Bus(1),
            "z" : Bus(1),
            "stallf" : Bus(1),
            "pcsrcd" : Bus(2),
            "pcwrd" : Bus(1),
            "regsad" : Bus(1),
            "regdstd" : Bus(2),
            "regwrsd" : Bus(2),
            "regwrd" : Bus(1),
            "extsd" : Bus(2),
            "alusrcbd" : Bus(1),
            "alusd" : Bus(4),
            "aluflagwrd" : Bus(1),
            "memwrd" : Bus(1),
            "regsrcd" : Bus(1),
            "wd3sd" : Bus(1)
        })

        config = {
            "name" : "controller_pipeline",
            "type" : "ControllerPipeline",
            "cond" : "cond",
            "op" : "op",
            "funct" : "funct",
            "rd" : "rd",
            "bit4" : "bit4",
            "c" : "c",
            "v" : "v",
            "n" : "n",
            "z" : "z",
            "stallf" : "stallf",
            "pcsrcd" : "pcsrcd",
            "pcwrd" : "pcwrd",
            "regsad" : "regsad",
            "regdstd" : "regdstd",
            "regwrsd" : "regwrsd",
            "regwrd" : "regwrd",
            "extsd" : "extsd",
            "alusrcbd" : "alusrcbd",
            "alusd" : "alusd",
            "aluflagwrd" : "aluflagwrd",
            "memwrd" : "memwrd",
            "regsrcd" : "regsrcd",
            "wd3sd" : "wd3sd"
        }

        ctrl = ControllerPipeline.from_dict(config,hooks)

if __name__ == '__main__':
    unittest.main()
