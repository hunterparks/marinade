"""
Single-Cycle Full Proof of Concept

This module defines a proof of concept architecture for a simulated ARM
CPU. Note that this architecture implements all instructions necessary for an
introductory architecture course. The instructions omitted include,
    - Coprocessor
    - Long multiplication
    - Branch Exchange (No thumb code)
    - Memory access multiple

The reason that this module exists is to provide a test platform for the
simulator. In addition, this architecture is used to develop the API for
interface with front-end processes.

Note that this module will be obsolete once an architecture serializer is
developed.
"""

import time
from collections import OrderedDict

from components.abstract.sequential import Latch_Type, Logic_States

from components.core.bus import Bus
from components.core.mux import Mux
from components.core.clock import Clock
from components.core.reset import Reset
from components.core.adder import Adder
from components.core.bus_join import BusJoin
from components.core.register import Register
from components.core.constant import Constant
from components.core.bus_subset import BusSubset
from components.core.logic_input import LogicInput

from components.arm.alu_full import Alu
from components.arm.alu_flag_register import ALUFlagRegister
from components.arm.extender import Extender
from components.arm.data_memory import DataMemory
from components.arm.program_memory import ProgramMemory
from components.arm.register_file_full import RegisterFile
from components.arm.controller_single_cycle_full import ControllerSingleCycle

from architecture import Architecture


def program_single_cycle_architecture(arch, program):
    "Provides a simple test program to run on architecture (for demo)"

    program_msg = {
        'modify': {
            'name': 'progmem',
            'parameters': {
                'start': 0,
                'data': program
            }
        }
    }
    res = arch.hook(program_msg)


def generate_single_cycle_architecture():
    "Illustrates the necessary process to construct an architecture"

    # define system resources
    clk = Clock(10, 0)
    rst = Reset(0)
    hooks = OrderedDict([('clk', clk), ('rst', rst)])

    # define input hooks and constants
    hooks.update({'const8': Constant(32, 8)})
    hooks.update({'const4': Constant(32, 4)})
    hooks.update({'const14': Constant(4, 14)})

    # define buses
    hooks.update({'pc': Bus(32, 0)})
    hooks.update({'pc8': Bus(32, 0)})
    hooks.update({'pc4': Bus(32, 0)})
    hooks.update({'instr': Bus(32, 0)})
    hooks.update({'instr_23_0': Bus(24, 0)})
    hooks.update({'instr_19_16': Bus(4, 0)})
    hooks.update({'instr_3_0': Bus(4, 0)})
    hooks.update({'instr_15_12': Bus(4, 0)})
    hooks.update({'instr_11_8': Bus(4, 0)})
    hooks.update({'instr_11_7': Bus(5, 0)})
    hooks.update({'imm32': Bus(32, 0)})
    hooks.update({'ra1': Bus(4, 0)})
    hooks.update({'ra2': Bus(4, 0)})
    hooks.update({'ra3': Bus(4, 0)})
    hooks.update({'wa': Bus(4, 0)})
    hooks.update({'rwd': Bus(32, 0)})
    hooks.update({'rd1': Bus(32, 0)})
    hooks.update({'rd2': Bus(32, 0)})
    hooks.update({'rd3': Bus(32, 0)})
    hooks.update({'alub': Bus(32, 0)})
    hooks.update({'branch': Bus(32, 0)})
    hooks.update({'aluf': Bus(32, 0)})
    hooks.update({'aluc': Bus(1, 0)})
    hooks.update({'aluv': Bus(1, 0)})
    hooks.update({'alun': Bus(1, 0)})
    hooks.update({'aluz': Bus(1, 0)})
    hooks.update({'aluflag': Bus(4, 0)})
    hooks.update({'flag': Bus(4, 0)})
    hooks.update({'c': Bus(1, 0)})
    hooks.update({'v': Bus(1, 0)})
    hooks.update({'n': Bus(1, 0)})
    hooks.update({'z': Bus(1, 0)})
    hooks.update({'memrd': Bus(32, 0)})
    hooks.update({'memrd_ext': Bus(32, 0)})
    hooks.update({'wdb': Bus(32, 0)})
    hooks.update({'pcwb': Bus(32, 0)})

    # control signals
    hooks.update({'pcwr': Bus(1, 0)})
    hooks.update({'regsa': Bus(1, 0)})
    hooks.update({'regsb': Bus(1, 0)})
    hooks.update({'regdst': Bus(2, 0)})
    hooks.update({'regwrs': Bus(2, 0)})
    hooks.update({'wdbs': Bus(1, 0)})
    hooks.update({'regwr': Bus(1, 0)})
    hooks.update({'exts': Bus(2, 0)})
    hooks.update({'alusrcb': Bus(1, 0)})
    hooks.update({'alus': Bus(4, 0)})
    hooks.update({'aluflagwr': Bus(1, 0)})
    hooks.update({'shop': Bus(2, 0)})
    hooks.update({'shctrl': Bus(2, 0)})
    hooks.update({'accen': Bus(1, 0)})
    hooks.update({'memwr': Bus(1, 0)})
    hooks.update({'memty': Bus(2, 0)})
    hooks.update({'regsrc': Bus(1, 0)})
    hooks.update({'pcsrc': Bus(2, 0)})

    # FETCH
    entities = OrderedDict([('clk', clk)])
    entities.update({'pc_reg': Register(32, hooks['clk'], hooks['rst'],
                                        hooks['pcwb'], hooks['pc'], 0, enable=hooks['pcwr'],
                                        edge_type=Latch_Type.FALLING_EDGE)})
    entities.update({'add8': Adder(32, hooks['pc'], hooks['const8'], hooks['pc8'])})
    entities.update({'add4': Adder(32, hooks['pc'], hooks['const4'], hooks['pc4'])})
    entities.update({'progmem': ProgramMemory(
        hooks['pc'], hooks['rst'], hooks['instr'])})

    # DECODE
    entities.update({'instr_subset': BusSubset(hooks['instr'],
                                               [hooks['instr_23_0'], hooks['instr_19_16'],
                                                hooks['instr_3_0'], hooks['instr_15_12'],
                                                hooks['instr_11_8'], hooks['instr_11_7']],
                                               [(0, 24), (16, 20), (0, 4), (12, 16), (8, 12), (7, 12)])})

    entities.update({'controller': ControllerSingleCycle(hooks['instr'], hooks['c'], hooks['v'],
                                                         hooks['n'], hooks['z'], hooks['pcsrc'],
                                                         hooks['pcwr'], hooks['regsa'], hooks['regdst'], hooks['regsb'], hooks['regwrs'],
                                                         hooks['regwr'], hooks['exts'], hooks['alusrcb'], hooks['alus'], hooks['shop'],
                                                         hooks['shctrl'], hooks['accen'], hooks['aluflagwr'], hooks['memty'], hooks['memwr'],
                                                         hooks['regsrc'], hooks['wdbs'])})

    entities.update({'ra1_mux': Mux(4, [hooks['instr_3_0'], hooks['instr_19_16']],
                                    hooks['regsa'], hooks['ra1'])})
    entities.update({'ra2_mux': Mux(4, [hooks['instr_11_8'], hooks['instr_3_0'],
                                        hooks['instr_15_12']], hooks['regdst'], hooks['ra2'])})
    entities.update({'ra2_mux': Mux(4, [hooks['instr_11_8'], hooks['instr_15_12']],
                                    hooks['regsb'], hooks['ra3'])})
    entities.update({'wa_mux': Mux(4, [hooks['instr_19_16'], hooks['instr_15_12'],
                                       hooks['const14']], hooks['regwrs'], hooks['wa'])})
    entities.update({'rwd_mux': Mux(32, [hooks['wdb'], hooks['pc4']], hooks['wdbs'],
                                    hooks['rwd'])})
    entities.update({'extimm': Extender(hooks['instr_23_0'], hooks['exts'],
                                        hooks['imm32'])})
    entities.update({'regfile': RegisterFile(hooks['clk'], hooks['rst'], hooks['regwr'],
                                             hooks['rwd'], hooks['ra1'], hooks['ra2'],
                                             hooks['ra3'], hooks['wa'], hooks['rd1'],
                                             hooks['rd2'], hooks['rd3'], hooks['pc'])})

    # EXECUTE
    entities.update({'alu_mux': Mux(32, [hooks['imm32'], hooks['rd2']],
                                    hooks['alusrcb'], hooks['alub'])})
    entities.update({'add_br': Adder(32, hooks['pc8'], hooks['imm32'], hooks['branch'])})
    entities.update({'alu': Alu(hooks['rd1'], hooks['alub'], hooks['rd3'], hooks['alus'],
                                hooks['instr_11_7'], hooks['c'], hooks['shop'], hooks['shctrl'],
                                hooks['accen'], hooks['aluf'], hooks['aluc'], hooks['aluv'],
                                hooks['alun'], hooks['aluz'])})

    entities.update({'aluflag_reg': ALUFlagRegister(hooks['aluc'], hooks['aluv'], hooks['alun'],
                                                    hooks['aluz'], hooks['rst'], hooks['clk'],
                                                    hooks['aluflagwr'], hooks['c'], hooks['v'],
                                                    hooks['n'], hooks['z'])})

    # MEMORY
    entities.update({'datamem': DataMemory(hooks['aluf'], hooks['rd2'], hooks['memwr'],
                                           hooks['rst'], hooks['clk'], hooks['memrd'], hooks['memty'])})

    # WRITE-BACK
    entities.update({'wdb_mux': Mux(32, [hooks['memrd'], hooks['aluf']],
                                    hooks['regsrc'], hooks['wdb'])})
    entities.update({'pcwb_mux': Mux(32, [hooks['branch'], hooks['pc4'], hooks['wdb']],
                                     hooks['pcsrc'], hooks['pcwb'])})

    # place memory (Internal) hooks into hook list
    hooks.update({'pc_reg': entities['pc_reg']})
    hooks.update({'progmem': entities['progmem']})
    hooks.update({'regfile': entities['regfile']})
    hooks.update({'aluflag_reg': entities['aluflag_reg']})
    hooks.update({'datamem': entities['datamem']})
    hooks.update({'controller': entities['controller']})

    # generate simulatable architecture
    arch = Architecture(0.0001, clk, rst, hooks, entities)
    return arch, hooks
