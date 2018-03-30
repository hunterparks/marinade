"""
Tests ARM component ALUFlagRegister
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.arm.alu_flag_register import ALUFlagRegister, Latch_Type, Logic_States
from simulator.components.core.constant import Constant
from simulator.components.core.bus import Bus


class ALUFlagRegister_t(unittest.TestCase):
    """
    Tests ALUFlagRegister's constructor and run functionality.

    Note that core Register tests base functionality for this component
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        cin = Bus(1)
        vin = Bus(1)
        nin = Bus(1)
        zin = Bus(1)

        rst = Bus(1)
        clk = Bus(1)
        en = Bus(1)

        cout = Bus(1)
        vout = Bus(1)
        nout = Bus(1)
        zout = Bus(1)

        # test bus configuration
        with self.assertRaises(TypeError):
            reg = ALUFlagRegister('cin', vin, nin, zin, rst, clk, en, cout, vout, nout, zout)
        with self.assertRaises(TypeError):
            c = Bus(2)
            reg = ALUFlagRegister(c, vin, nin, zin, rst, clk, en, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, 'vin', nin, zin, rst, clk, en, cout, vout, nout, zout)
        with self.assertRaises(TypeError):
            v = Bus(2)
            reg = ALUFlagRegister(cin, v, nin, zin, rst, clk, en, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, 'nin', zin, rst, clk, en, cout, vout, nout, zout)
        with self.assertRaises(TypeError):
            n = Bus(2)
            reg = ALUFlagRegister(cin, vin, n, zin, rst, clk, en, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, 'zin', rst, clk, en, cout, vout, nout, zout)
        with self.assertRaises(TypeError):
            z = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, z, rst, clk, en, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, 'rst', clk, en, cout, vout, nout, zout)
        with self.assertRaises(ValueError):
            r = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, r, clk, en, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, 'clk', en, cout, vout, nout, zout)
        with self.assertRaises(ValueError):
            c = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, c, en, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, 'en', cout, vout, nout, zout)
        with self.assertRaises(ValueError):
            e = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, e, cout, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, 'cout', vout, nout, zout)
        with self.assertRaises(TypeError):
            c = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, c, vout, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, 'vout', nout, zout)
        with self.assertRaises(TypeError):
            v = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, v, nout, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, 'nout', zout)
        with self.assertRaises(TypeError):
            n = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, n, zout)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, nout, 'zout')
        with self.assertRaises(TypeError):
            z = Bus(2)
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, nout, z)

        # test parameter configuration (only need to be concerned with default state)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, nout, zout, 255)

        with self.assertRaises(TypeError):
            reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, nout, zout, '255')


        # test valid construction
        reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, nout, zout,
                              0, Latch_Type.RISING_EDGE, Logic_States.ACTIVE_HIGH,
                              Logic_States.ACTIVE_HIGH)

    def test_run(self):
        "Verifies correct time based simulation"
        cin = Bus(1)
        vin = Bus(1)
        nin = Bus(1)
        zin = Bus(1)
        rst = Bus(1)
        clk = Bus(1)
        en = Bus(1, 1)
        cout = Bus(1)
        vout = Bus(1)
        nout = Bus(1)
        zout = Bus(1)

        reg = ALUFlagRegister(cin, vin, nin, zin, rst, clk, en, cout, vout, nout, zout)

        # store data in register and bring it back out, one bit at a time
        cin.write(1)
        vin.write(0)
        nin.write(0)
        zin.write(0)
        clk.write(0)
        reg.run()
        clk.write(1)
        reg.run()

        self.assertEqual(cout.read(), 1)
        self.assertEqual(vout.read(), 0)
        self.assertEqual(nout.read(), 0)
        self.assertEqual(zout.read(), 0)

        cin.write(0)
        vin.write(1)
        nin.write(0)
        zin.write(0)
        clk.write(0)
        reg.run()
        clk.write(1)
        reg.run()

        self.assertEqual(cout.read(), 0)
        self.assertEqual(vout.read(), 1)
        self.assertEqual(nout.read(), 0)
        self.assertEqual(zout.read(), 0)

        cin.write(0)
        vin.write(0)
        nin.write(1)
        zin.write(0)
        clk.write(0)
        reg.run()
        clk.write(1)
        reg.run()

        self.assertEqual(cout.read(), 0)
        self.assertEqual(vout.read(), 0)
        self.assertEqual(nout.read(), 1)
        self.assertEqual(zout.read(), 0)

        cin.write(0)
        vin.write(0)
        nin.write(0)
        zin.write(1)
        clk.write(0)
        reg.run()
        clk.write(1)
        reg.run()

        self.assertEqual(cout.read(), 0)
        self.assertEqual(vout.read(), 0)
        self.assertEqual(nout.read(), 0)
        self.assertEqual(zout.read(), 1)


if __name__ == '__main__':
    unittest.main()
