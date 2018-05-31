"""
Tests arm component Alu
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.alu_full import Alu
from simulator.components.core.bus import Bus


class Alu_t(unittest.TestCase):
    """
    Tests Alu's constructor and run functionality
    """

    def test_constructor(self):
        """
        tests 2 bad constructors - not all possible constructors tested
        """

        a = Bus(31)
        b = Bus(32)
        ar = Bus(32)
        alus = Bus(4)
        shift = Bus(5)
        cin = Bus(1)
        shiftOp = Bus(2)
        shiftCtrl = Bus(2)
        accEn = Bus(1)
        f = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)

        # test case 1
        with self.assertRaises(ValueError):
            test_alu = Alu(a, b, ar, alus, shift, cin, shiftOp, shiftCtrl, accEn, f, c, v, n, z)
        # test case 2
        with self.assertRaises(ValueError):
            test_alu = Alu(Bus(32), Bus(32), ar, alus, shift, cin, shiftOp, shiftCtrl, accEn, c, f, v, n, z)

    def test_run(self):
        """
        test's the alu's run function
        """

        a = Bus(32)
        b = Bus(32)
        ar = Bus(32)
        alus = Bus(4)
        shift = Bus(5)
        cin = Bus(1)
        shiftOp = Bus(2)
        shiftCtrl = Bus(2)
        accEn = Bus(1)
        f = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)

        # initialize alu
        test_alu = Alu(a, b, ar, alus, shift, cin, shiftOp, shiftCtrl, accEn, f, c, v, n, z)

        #test shifter left logical constant
        a.write(0)
        b.write(0xAA)
        alus.write(6)
        shift.write(1)
        shiftOp.write(0)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0x154)

        #test shifter right logical constant
        a.write(0)
        b.write(0xAA)
        alus.write(6)
        shift.write(1)
        shiftOp.write(1)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0x55)

        a.write(0)
        b.write(0xFFFFFFF0)
        alus.write(6)
        shift.write(1)
        shiftOp.write(1)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0x7FFFFFF8)

        #test shifter right arithmetic constant
        a.write(0)
        b.write(0xF0)
        alus.write(6)
        shift.write(1)
        shiftOp.write(2)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0x78)

        a.write(0)
        b.write(0xFFFFFFF0)
        alus.write(6)
        shift.write(1)
        shiftOp.write(2)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0xFFFFFFF8)

        #test shifter right roll constant
        a.write(0)
        b.write(0xF)
        alus.write(6)
        shift.write(4)
        shiftOp.write(3)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0xF0000000)

        a.write(0)
        b.write(4)
        alus.write(6)
        shift.write(3)
        shiftOp.write(3)
        shiftCtrl.write(1)
        test_alu.run()
        self.assertEqual(f.read(),0x80000000)


        #test shifter left logical register
        a.write(0)
        b.write(0xAA)
        ar.write(0xF01)
        alus.write(6)
        shift.write(0xF)
        shiftOp.write(0)
        shiftCtrl.write(3)
        test_alu.run()
        self.assertEqual(f.read(),0x154)

        #test shifter right logical register
        a.write(0)
        b.write(0xAA)
        ar.write(0xF01)
        alus.write(6)
        shift.write(0xF)
        shiftOp.write(1)
        shiftCtrl.write(3)
        test_alu.run()
        self.assertEqual(f.read(),0x55)

        a.write(0)
        b.write(0xFFFFFFF0)
        ar.write(0xF01)
        alus.write(6)
        shift.write(0xF)
        shiftOp.write(1)
        shiftCtrl.write(3)
        test_alu.run()
        self.assertEqual(f.read(),0x7FFFFFF8)

        #test shifter right arithmetic register
        a.write(0)
        b.write(0xF0)
        ar.write(0xF01)
        alus.write(6)
        shift.write(0xF)
        shiftOp.write(2)
        shiftCtrl.write(3)
        test_alu.run()
        self.assertEqual(f.read(),0x78)

        a.write(0)
        b.write(0xFFFFFFF0)
        ar.write(0xF01)
        alus.write(6)
        shift.write(0xF)
        shiftOp.write(2)
        shiftCtrl.write(3)
        test_alu.run()
        self.assertEqual(f.read(),0xFFFFFFF8)

        #test shifter right roll register
        a.write(0)
        b.write(0xF)
        ar.write(0xF04)
        alus.write(6)
        shift.write(0xF)
        shiftOp.write(3)
        shiftCtrl.write(3)
        test_alu.run()
        self.assertEqual(f.read(),0xF0000000)



        #disable shifter for rest of test
        shiftCtrl.write(0)

        #test alus add
        a.write(5)
        b.write(2)
        alus.write(0)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(0x80000000)
        b.write(0x80000000)
        alus.write(0)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 1)

        #test alus subtract
        a.write(5)
        b.write(2)
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 3)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(1)
        b.write(2)
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFF)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 0)

        a.write(0x7FFFFFFF)
        b.write(0xFFFFFFFF)
        alus.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 0x80000000)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 1)

        #test alus and
        a.write(5)
        b.write(2)
        alus.write(2)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus or
        a.write(5)
        b.write(2)
        alus.write(3)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus xor
        a.write(5)
        b.write(2)
        alus.write(4)
        test_alu.run()
        self.assertEqual(f.read(), 7)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus pass a
        a.write(5)
        b.write(2)
        alus.write(5)
        test_alu.run()
        self.assertEqual(f.read(), 5)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus pass b
        a.write(5)
        b.write(2)
        alus.write(6)
        test_alu.run()
        self.assertEqual(f.read(), 2)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus multiply
        a.write(5)
        b.write(2)
        alus.write(7)
        test_alu.run()
        self.assertEqual(f.read(), 10)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(268435456)
        b.write(9)
        alus.write(7)
        test_alu.run()
        self.assertEqual(f.read(), 2415919104)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 1)

        #test alus add with carry
        a.write(5)
        b.write(2)
        cin.write(1)
        alus.write(8)
        test_alu.run()
        self.assertEqual(f.read(), 8)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(0x80000000)
        b.write(0x7FFFFFFF)
        cin.write(1)
        alus.write(8)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 0)

        #test alus subtract with carry
        a.write(5)
        b.write(2)
        cin.write(0)
        alus.write(9)
        test_alu.run()
        self.assertEqual(f.read(), 2)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(2)
        b.write(2)
        cin.write(0)
        alus.write(9)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFF)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 0)

        #test alus reverse subtract
        a.write(2)
        b.write(5)
        alus.write(10)
        test_alu.run()
        self.assertEqual(f.read(), 3)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(2)
        b.write(1)
        alus.write(10)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFF)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 0)

        #test alus reverse subtract with carry
        a.write(2)
        b.write(5)
        cin.write(0)
        alus.write(11)
        test_alu.run()
        self.assertEqual(f.read(), 2)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(2)
        b.write(2)
        cin.write(0)
        alus.write(11)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFF)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 1)
        self.assertEqual(v.read(), 0)

        #test alus and not
        a.write(2)
        b.write(5)
        alus.write(12)
        test_alu.run()
        self.assertEqual(f.read(), 2)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test not
        a.write(2)
        b.write(1)
        alus.write(13)
        test_alu.run()
        self.assertEqual(f.read(), 0xFFFFFFFE)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus generate 0
        a.write(5)
        b.write(2)
        alus.write(14)
        test_alu.run()
        self.assertEqual(f.read(), 0)
        self.assertEqual(z.read(), 1)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        #test alus generate 1
        a.write(5)
        b.write(2)
        alus.write(15)
        test_alu.run()
        self.assertEqual(f.read(), 1)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        # test MLA behavior using accumulate
        a.write(5)
        b.write(5)
        ar.write(45)
        alus.write(7)
        accEn.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 70)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 0)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 0)

        a.write(0x3FFFFFFF)
        b.write(2)
        ar.write(2)
        alus.write(7)
        accEn.write(1)
        test_alu.run()
        self.assertEqual(f.read(), 0x80000000)
        self.assertEqual(z.read(), 0)
        self.assertEqual(n.read(), 1)
        self.assertEqual(c.read(), 0)
        self.assertEqual(v.read(), 1)

    def test_from_dict(self):
        "Validates dictionary constructor"

        hooks = OrderedDict({
            "a" : Bus(32),
            "b" : Bus(32),
            "ar" : Bus(32),
            "alus" : Bus(4),
            "sh" : Bus(5),
            "cin" : Bus(1),
            "shop" : Bus(2),
            "shctrl" : Bus(2),
            "accen" : Bus(1),
            "f" : Bus(32),
            "c" : Bus(1),
            "v" : Bus(1),
            "n" : Bus(1),
            "z" : Bus(1)
        })

        config = {
            "input_a" : "a",
            "input_b" : "b",
            "input_ar" : "ar",
            "alus" : "alus",
            "shift" : "sh",
            "input_c" : "cin",
            "shift_op" : "shop",
            "shift_ctrl" : "shctrl",
            "acc_enable" : "accen",
            "output_f" : "f",
            "output_c" : "c",
            "output_v" : "v",
            "output_n" : "n",
            "output_z" : "z"
        }

        alu = Alu.from_dict(config,hooks)


if __name__ == '__main__':
    unittest.main()
