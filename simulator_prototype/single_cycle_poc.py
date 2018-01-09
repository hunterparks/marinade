import time

from components.core.bus import Bus
from components.core.clock import Clock
from components.core.reset import Reset
from components.core.logic_input import LogicInput
from components.abstract.sequential import Latch_Type, Logic_States

from components.core.register import Register
from components.core.adder import Adder
from components.arm.register_file import RegisterFile
from components.core.mux import Mux
from components.arm.alu import Alu
from components.core.bus_subset import BusSubset
from components.core.bus_join import BusJoin
from components.core.constant import Constant
from components.arm.memory import Memory
from components.arm.extender import Extender
from components.arm.controller_single_cycle import ControllerSingleCycle

from collections import OrderedDict
from architecture import Architecture

def program_single_cycle_architecture(arch):
    program_msg = {
        'modify' : {
            'name' : 'progmem',
            'parameters' : {
                'start' : 0,
                'data' : [
                    0xE3A0800A,
                    0xE2889001,
                    0xE0090998,
                    0xE3A0A000,
                    0xE24AA020,
                    0xE019A00A,
                    0x0A000002,
                    0xE3A0B001,
                    0xE3A0C004,
                    0xE58CB000,
                    0xE59C6000,
                    0xEAFFFFFD
                ]
            }
        }
    }
    res = arch.hook(program_msg)
    print("Programming:")
    print(program_msg)
    print(res)
    print('\n\n\n')


def generate_single_cycle_architecture():
    #define system resources
    clk = Clock(10,0)
    rst = Reset(0)
    hooks = OrderedDict([('clk',clk),('rst',rst)])

    #define input hooks and constants
    hooks.update({'const8' : Constant(32,8)})
    hooks.update({'const4' : Constant(32,4)})
    hooks.update({'const14' : Constant(4,14)})
    hooks.update({'pmd' : LogicInput(32,0)})
    hooks.update({'pmwr' : LogicInput(1,0)})

    # define buses
    hooks.update({'pc' : Bus(32,0)})
    hooks.update({'pc8' : Bus(32,0)})
    hooks.update({'pc4' : Bus(32,0)})
    hooks.update({'instr' : Bus(32,0)})
    hooks.update({'instr_23_0' : Bus(24,0)})
    hooks.update({'instr_19_16' : Bus(4,0)})
    hooks.update({'instr_3_0' : Bus(4,0)})
    hooks.update({'instr_15_12' : Bus(4,0)})
    hooks.update({'instr_11_8' : Bus(4,0)})
    hooks.update({'instr_31_28' : Bus(4,0)})
    hooks.update({'instr_27_26' : Bus(2,0)})
    hooks.update({'instr_25_20' : Bus(6,0)})
    hooks.update({'instr_4_4' : Bus(1,0)})
    hooks.update({'imm32' : Bus(32,0)})
    hooks.update({'ra1' : Bus(4,0)})
    hooks.update({'ra2' : Bus(4,0)})
    hooks.update({'ra3' : Bus(4,0)})
    hooks.update({'rwd' : Bus(32,0)})
    hooks.update({'rd1' : Bus(32,0)})
    hooks.update({'rd2' : Bus(32,0)})
    hooks.update({'alub' : Bus(32,0)})
    hooks.update({'branch' : Bus(32,0)})
    hooks.update({'aluf' : Bus(32,0)})
    hooks.update({'aluc' : Bus(1,0)})
    hooks.update({'aluv' : Bus(1,0)})
    hooks.update({'alun' : Bus(1,0)})
    hooks.update({'aluz' : Bus(1,0)})
    hooks.update({'aluflag' : Bus(4,0)})
    hooks.update({'flag' : Bus(4,0)})
    hooks.update({'c' : Bus(1,0)})
    hooks.update({'v' : Bus(1,0)})
    hooks.update({'n' : Bus(1,0)})
    hooks.update({'z' : Bus(1,0)})
    hooks.update({'memrd' : Bus(32,0)})
    hooks.update({'wdb' : Bus(32,0)})
    hooks.update({'pcwb' : Bus(32,0)})

    #control signals
    hooks.update({'pcwr' : Bus(1,0)})
    hooks.update({'regsa' : Bus(1,0)})
    hooks.update({'regdst' : Bus(2,0)})
    hooks.update({'regwrs' : Bus(2,0)})
    hooks.update({'wdbs' : Bus(1,0)})
    hooks.update({'regwr' : Bus(1,0)})
    hooks.update({'exts' : Bus(2,0)})
    hooks.update({'alu8rcb' : Bus(1,0)})
    hooks.update({'alus' : Bus(4,0)})
    hooks.update({'aluflagwr' : Bus(1,0)})
    hooks.update({'memwr' : Bus(1,0)})
    hooks.update({'regsrc' : Bus(1,0)})
    hooks.update({'pcsrc' : Bus(2,0)})

    # generate components
    entities = OrderedDict([('clk',clk)])
    entities.update({'pc_reg' : Register(32,hooks['clk'],hooks['rst'],hooks['pcwb'],hooks['pc'],0, enable = hooks['pcwr'],edge_type = Latch_Type.FALLING_EDGE)})
    entities.update({'add8' : Adder(32,hooks['pc'],hooks['const8'],hooks['pc8'])})
    entities.update({'add4' : Adder(32,hooks['pc'],hooks['const4'],hooks['pc4'])})
    entities.update({'progmem' : Memory(hooks['pc'],hooks['pmd'],hooks['pmwr'],hooks['clk'],hooks['rst'],hooks['instr'])})

    entities.update({'instr_subset' : BusSubset(hooks['instr'],
                    [hooks['instr_23_0'],hooks['instr_19_16'],
                     hooks['instr_3_0'],hooks['instr_15_12'],
                     hooks['instr_11_8'],hooks['instr_31_28'],
                     hooks['instr_27_26'],hooks['instr_25_20'],
                     hooks['instr_4_4']],
                    [(0,24),(16,20),(0,4),(12,16),(8,12),(28,32),(26,28),(20,26),(4,5)])})

    entities.update({'controller' : ControllerSingleCycle(hooks['instr_31_28'],
                    hooks['instr_27_26'],hooks['instr_25_20'],
                    hooks['instr_15_12'],hooks['instr_4_4'],
                    hooks['c'],hooks['v'],hooks['n'],hooks['z'],
                    hooks['pcsrc'],hooks['pcwr'],hooks['regsa'],
                    hooks['regdst'],hooks['regwrs'],hooks['regwr'],
                    hooks['exts'],hooks['alu8rcb'],hooks['alus'],
                    hooks['aluflagwr'],hooks['memwr'],hooks['regsrc'],
                    hooks['wdbs'])})

    entities.update({'ra1_mux' : Mux(4,[hooks['instr_3_0'],hooks['instr_19_16']],hooks['regsa'],hooks['ra1'])})
    entities.update({'ra2_mux' : Mux(4,[hooks['instr_11_8'],hooks['instr_3_0'],hooks['instr_15_12']],hooks['regdst'],hooks['ra2'])})
    entities.update({'ra3_mux' : Mux(4,[hooks['instr_19_16'],hooks['instr_15_12'],hooks['const14']],hooks['regwrs'],hooks['ra3'])})
    entities.update({'rwd_mux' : Mux(32,[hooks['wdb'],hooks['pc4']],hooks['wdbs'],hooks['rwd'])})
    entities.update({'extimm' : Extender(hooks['instr_23_0'],hooks['imm32'],hooks['exts'])})
    entities.update({'regfile' : RegisterFile(hooks['clk'],hooks['rst'],hooks['regwr'],hooks['rwd'],hooks['ra1'],hooks['ra2'],hooks['ra3'],hooks['rd1'],hooks['rd2'])})

    entities.update({'alu_mux' : Mux(32,[hooks['imm32'],hooks['rd2']],hooks['alu8rcb'],hooks['alub'])})
    entities.update({'add_br' : Adder(32,hooks['pc8'],hooks['imm32'],hooks['branch'])})
    entities.update({'alu' : Alu(hooks['rd1'],hooks['alub'],hooks['alus'],hooks['aluf'],hooks['aluc'],hooks['aluv'],hooks['alun'],hooks['aluz'])})
    entities.update({'aluflag_join' : BusJoin([hooks['aluc'],hooks['aluv'],hooks['alun'],hooks['aluz']],hooks['aluflag'])})
    entities.update({'aluflag_reg' : Register(4,hooks['clk'],hooks['rst'],hooks['aluflag'],hooks['flag'],enable = hooks['aluflagwr'])})
    entities.update({'flag_subset' : BusSubset(hooks['flag'],[hooks['c'],hooks['v'],hooks['n'],hooks['z']],[(0,1),(1,2),(2,3),(3,4)])})

    entities.update({'datamem' : Memory(hooks['aluf'],hooks['rd2'],hooks['memwr'],hooks['rst'],hooks['clk'],hooks['memrd'])})
    entities.update({'wdb_mux' : Mux(32,[hooks['memrd'],hooks['aluf']],hooks['regsrc'],hooks['wdb'])})
    entities.update({'pcwb_mux' : Mux(32,[hooks['branch'],hooks['pc4'],hooks['wdb']],hooks['pcsrc'],hooks['pcwb'])})

    #place memory (Internal) hooks into hook list
    hooks.update({'pc_reg' : entities['pc_reg']})
    hooks.update({'progmem' : entities['progmem']})
    hooks.update({'regfile' : entities['regfile']})
    hooks.update({'aluflag_reg' : entities['aluflag_reg']})
    hooks.update({'datamem' : entities['datamem']})

    # generate simulatable architecture
    arch = Architecture(0.0001,clk,rst,hooks,entities)
    return arch, hooks
