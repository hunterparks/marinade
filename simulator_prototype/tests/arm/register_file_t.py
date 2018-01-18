import unittest
import sys
sys.path.insert(0,'../../')
from components.arm.register_file_wo_pc import RegisterFile_wo_PC, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus import Bus

class RegisterFile_t(unittest.TestCase):

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1,0)
        rst = Bus(1,0)
        wa = Bus(4,0)
        wd = Bus(32,10)
        ra0 = Bus(4,0)
        ra1 = Bus(4,0)
        rd0 = Bus(32)
        rd1 = Bus(32)
        en = Bus(1,0)

        #just prove that the constructor accepts data when filled, rest is
        #tested under the core component

        reg = RegisterFile_wo_PC(clk,rst,en,wd,ra0,ra1,wa,rd0,rd1)

        reg = RegisterFile_wo_PC(clk,rst,en,wd,ra0,ra1,wa,rd0,rd1,edge_type = Latch_Type.BOTH_EDGE)

        reg = RegisterFile_wo_PC(clk,rst,en,wd,ra0,ra1,wa,rd0,rd1, reset_type = Logic_States.ACTIVE_HIGH)

        reg = RegisterFile_wo_PC(clk,rst,en,wd,ra0,ra1,wa,rd0,rd1, enable_type = Logic_States.ACTIVE_LOW)

        reg = RegisterFile_wo_PC(clk,rst,en,wd,ra0,ra1,wa,rd0,rd1,Latch_Type.RISING_EDGE,Logic_States.ACTIVE_HIGH,Logic_States.ACTIVE_LOW)

if __name__ == '__main__':
    unittest.main()
