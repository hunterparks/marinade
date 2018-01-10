

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.controller_single_cycle import ControllerSingleCycle
from components.core.bus import Bus

class ControllerSingleCycle_t(unittest.TestCase):

    def test_constructor(self):
        "tests 4 bad constructors - not all possible constructors tested"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcsrc = Bus(2)
        pcwr = Bus(1)
        regsa = Bus(1)
        regdst = Bus(2)
        regwrs = Bus(2)
        regwr = Bus(1)
        exts = Bus(2)
        alusrcb = Bus(1)
        alus = Bus(4)
        aluflagwr = Bus(1)
        memwr = Bus(1)
        regsrc = Bus(1)
        wd3s = Bus(1)
        # test case 1
        with self.assertRaises(ValueError):
            scc = ControllerSingleCycle(cond, funct, op, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                                        regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr,
                                        memwr, regsrc, wd3s)
        # test case 2
        with self.assertRaises(ValueError):
            scc = ControllerSingleCycle(cond, op, bit4, rd, funct, c, v, n, z, pcsrc, pcwr, regsa,
                                        regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr,
                                        memwr, regsrc, wd3s)
        # test case 3
        with self.assertRaises(ValueError):
            scc = ControllerSingleCycle(cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                                        regdst, regwr, regwrs, exts, alusrcb, aluflagwr, alus,
                                        memwr, regsrc, wd3s)
        # test case 4
        with self.assertRaises(ValueError):
            scc = ControllerSingleCycle(cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                                        regdst, regwr, regwrs, alusrcb, exts, alus, aluflagwr,
                                        memwr, regsrc, wd3s)

    def test_run(self):
        "tests the signle cycle processors run method"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcsrc = Bus(2)
        pcwr = Bus(1)
        regsa = Bus(1)
        regdst = Bus(2)
        regwrs = Bus(2)
        regwr = Bus(1)
        exts = Bus(2)
        alusrcb = Bus(1)
        alus = Bus(4)
        aluflagwr = Bus(1)
        memwr = Bus(1)
        regsrc = Bus(1)
        wd3s = Bus(1)
        # initialize single cycle controller
        scc = ControllerSingleCycle(cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                                    regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr,
                                    regsrc, wd3s)
        # pcsrc tests
        # test case 4 - occurs for banch instructions where condition is met
        op.write(2)
        cond.write(1)
        scc.run()
        self.assertEqual(pcsrc.read(), 0)
        # test case 5 - occurs when a data processing instruction modifies pc
        op.write(0)
        rd.write(15)
        scc.run()
        self.assertEqual(pcsrc.read(), 2)
        # test case 6 - for pc+4
        op.write(1)
        scc.run()
        self.assertEqual(pcsrc.read(), 1)
        # pcwr
        # test case 7 - always a 1 for the single cycle processor
        self.assertEqual(pcwr.read(), 1)
        # regsa
        # test case 8 - used to select Rn register (mul instruction)
        op.write(0)
        bit4.write(1)
        funct.write(1)
        scc.run()
        self.assertEqual(regsa.read(), 0)
        # test case 9 - used to select Rn register (data processing instuction)
        op.write(1)
        scc.run()
        self.assertEqual(regsa.read(), 1)
        # regdst
        # test case 10 - used to select Rd register (str instruction)
        op.write(1)
        funct.write(24)
        scc.run()
        self.assertEqual(regdst.read(), 2)
        # test case 11 - used to select Rm register (data processing instruction)
        op.write(0)
        bit4.write(1)
        funct.write(0)
        scc.run()
        self.assertEqual(regdst.read(), 0)
        # test case 12 - used to select Rm register (mul instruction)
        op.write(2)
        scc.run()
        self.assertEqual(regdst.read(), 1)
        # regwrs
        # test cast 13 - used to select lr instruction (bl instruction)
        op.write(2)
        funct.write(8)
        scc.run()
        self.assertEqual(regwrs.read(), 2)
        # test case 14 - used to select Rd register (data processing instruction)
        op.write(0)
        bit4.write(1)
        funct.write(0)
        scc.run()
        self.assertEqual(regwrs.read(), 0)
        # test case 15 - used to selcet Rd resister (mul instruction)
        op.write(1)
        scc.run()
        self.assertEqual(regwrs.read(), 1)
        # regwr
        # test case 16 - occurs when an instruction writes back to the regfile
        op.write(0)
        funct.write(53)
        scc.run()
        self.assertEqual(regwr.read(), 0)
        # test case 17 - occurs when an instruction writes back to the regfile
        op.write(1)
        funct.write(24)
        scc.run()
        self.assertEqual(regwr.read(), 0)
        # test case 18 - occurs when an instruction writes back to the regfile
        op.write(2)
        funct.write(0b111000)
        scc.run()
        self.assertEqual(regwr.read(), 0)
        # test case 19 - occurs when an instruction writes back to the regfile
        funct.write(1)
        scc.run()
        self.assertEqual(regwr.read(), 1)
        # exts
        # test case 20 - used for branch instruction
        op.write(2)
        scc.run()
        self.assertEqual(exts.read(), 2)
        # test case 21 - used for 12-bit immediate (ldr and str instructions)
        op.write(1)
        funct.write(25)
        scc.run()
        self.assertEqual(exts.read(), 1)
        # test case 22 - used for 8-bit immediate (data processing immediate)
        op.write(0)
        scc.run()
        self.assertEqual(exts.read(), 0)
        # alusrcb
        # test case 23 - occurs when source b requires the output to the rd2 register
        # (data processing instruction)
        op.write(0)
        funct.write(28)
        scc.run()
        self.assertEqual(alusrcb.read(), 1)
        # test case 24 - occurs when source b requires the output to the rd2 register
        # (data processing instruction)
        op.write(0)
        bit4.write(1)
        funct.write(1)
        scc.run()
        self.assertEqual(alusrcb.read(), 1)
        # test case 25 - occurs when source b requires an exdended immediate
        op.write(0)
        funct.write(63)
        scc.run()
        self.assertEqual(alusrcb.read(), 0)
        # test case 26 - occurs when source b requires an exdended immediate
        op.write(1)
        scc.run()
        self.assertEqual(alusrcb.read(), 0)
        # alus
        # test case 27 - + operation
        op.write(0)
        funct.write(8)
        scc.run()
        self.assertEqual(alus.read(), 0)
        # test case 28 - + operation
        op.write(1)
        funct.write(25)
        scc.run()
        self.assertEqual(alus.read(), 0)
        # test case 30 - - operation
        op.write(0)
        funct.write(21)
        scc.run()
        self.assertEqual(alus.read(), 1)
        # test case 31 - and operation
        op.write(0)
        funct.write(32)
        scc.run()
        self.assertEqual(alus.read(), 2)
        # test case 32 - or operation
        op.write(0)
        funct.write(25)
        scc.run()
        self.assertEqual(alus.read(), 3)
        # test case 33 - xor operation
        op.write(0)
        funct.write(35)
        scc.run()
        self.assertEqual(alus.read(), 4)
        # test case 34 - return B
        op.write(0)
        funct.write(26)
        scc.run()
        self.assertEqual(alus.read(), 6)
        # test case 35 - * operation
        op.write(0)
        funct.write(1)
        scc.run()
        self.assertEqual(alus.read(), 7)
        # test case 36 - return 1
        op.write(2)
        scc.run()
        self.assertEqual(alus.read(), 15)
        # aluflagwr
        # test case 37 - set c, v, n, z flags (cmp instructions or s bit set)
        op.write(0)
        funct.write(15)
        scc.run()
        self.assertEqual(aluflagwr.read(), 1)
        # test case 39 - flags will not be set
        op.write(0)
        funct.write(0)
        scc.run()
        self.assertEqual(aluflagwr.read(), 0)
        # test case 40 - flags will not be set
        op.write(1)
        scc.run()
        self.assertEqual(aluflagwr.read(), 0)
        # memwr
        # test case 41 - allows data to be written to data memory (str instructions)
        op.write(1)
        funct.write(24)
        scc.run()
        self.assertEqual(memwr.read(), 1)
        # test case 42 - cannot write to data memory
        op.write(0)
        scc.run()
        self.assertEqual(memwr.read(), 0)
        # regsrc
        # test case 43 - occurs when output of alu is feedback (ldr instructions)
        op.write(2)
        funct.write(25)
        scc.run()
        self.assertEqual(regsrc.read(), 0)
        # test case 44 - occurs when output of data memory is feedback
        op.write(0)
        scc.run()
        self.assertEqual(regsrc.read(), 1)
        # wd3s
        # test case 45 - occurs when a bl is run
        op.write(2)
        funct.write(24)
        scc.run()
        self.assertEqual(wd3s.read(), 1)
        # test case 46 - occurs for all non bl instructions
        op.write(0)
        scc.run()
        self.assertEqual(wd3s.read(), 0)

    def test_inspect(self):
        "tests the single cycle processors inspect method"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcsrc = Bus(2)
        pcwr = Bus(1)
        regsa = Bus(1)
        regdst = Bus(2)
        regwrs = Bus(2)
        regwr = Bus(1)
        exts = Bus(2)
        alusrcb = Bus(1)
        alus = Bus(4)
        aluflagwr = Bus(1)
        memwr = Bus(1)
        regsrc = Bus(1)
        wd3s = Bus(1)
        # initialize single cycle controller
        scc = ControllerSingleCycle(cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                                    regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr,
                                    regsrc, wd3s)
        ins = scc.inspect()
        self.assertTrue(ins['type'] == 'sc-controller')
        self.assertTrue(ins['state'] is None)

    def test_modify(self):
        "tests the single cycle processor inspect method"

        cond = Bus(4)
        op = Bus(2)
        funct = Bus(6)
        rd = Bus(4)
        bit4 = Bus(1)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcsrc = Bus(2)
        pcwr = Bus(1)
        regsa = Bus(1)
        regdst = Bus(2)
        regwrs = Bus(2)
        regwr = Bus(1)
        exts = Bus(2)
        alusrcb = Bus(1)
        alus = Bus(4)
        aluflagwr = Bus(1)
        memwr = Bus(1)
        regsrc = Bus(1)
        wd3s = Bus(1)
        # initialize single cycle controller
        scc = ControllerSingleCycle(cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                                    regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr,
                                    regsrc, wd3s)
        mod = scc.modify(None)
        self.assertTrue('error' in mod) #modify is not implemented for controller

        mod = scc.modify({'state' : 0})
        self.assertTrue('error' in mod) #modify is not implemented for controller

if __name__ == '__main__':
    unittest.main()
