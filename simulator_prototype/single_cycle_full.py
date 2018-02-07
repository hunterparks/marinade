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

from components.arm.alu_demo import Alu
from components.arm.extender import Extender
from components.arm.data_memory import DataMemory
from components.arm.program_memory import ProgramMemory
from components.arm.register_file_demo import RegisterFile
from components.arm.controller_single_cycle import ControllerSingleCycle

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

    # DECODE
    # TODO add correct instruction tree breakdown
    entities.update({'instr_subset': BusSubset(hooks['instr'],
                                               [hooks['instr_23_0'], hooks['instr_19_16'],
                                                hooks['instr_3_0'], hooks['instr_15_12'],
                                                hooks['instr_11_8'], hooks['instr_31_28'],
                                                hooks['instr_27_26'], hooks['instr_25_20'],
                                                hooks['instr_4_4']],
                                               [(0, 24), (16, 20), (0, 4), (12, 16), (8, 12), (28, 32), (26, 28), (20, 26), (4, 5)])})

    # TODO add controller

    entities.update({'ra1_mux': Mux(4, [hooks['instr_3_0'], hooks['instr_19_16']],
                                    hooks['regsa'], hooks['ra1'])})
    entities.update({'ra2_mux': Mux(4, [hooks['instr_11_8'], hooks['instr_3_0'],
                                        hooks['instr_15_12']], hooks['regdst'], hooks['ra2'])})
    entities.update({'ra2_mux': Mux(4, [hooks['instr_11_8'], hooks['instr_15_12']],
                                    hooks['regsb'], hooks['ra3'])})
    entities.update({'wa_mux': Mux(4, [hooks['instr_19_16'], hooks['instr_15_12'],
                                       hooks['const14']], hooks['regwrs'], hooks['ra3'])})
    entities.update({'rwd_mux': Mux(32, [hooks['wdb'], hooks['pc4']], hooks['wdbs'],
                                    hooks['rwd'])})
    entities.update({'extimm': Extender(hooks['instr_23_0'], hooks['exts'],
                                        hooks['imm32'])})
    entities.update({'regfile': RegisterFile(hooks['clk'], hooks['rst'], hooks['regwr'],
                                             hooks['rwd'], hooks['ra1'], hooks['ra2'],
                                             hooks['ra3'], hooks['wa1'], hooks['rd1'],
                                             hooks['rd2'], hooks['rd3'], hooks['pc'])})

    # EXECUTE
    entities.update({'alu_mux': Mux(32, [hooks['imm32'], hooks['rd2']],
                                    hooks['alu8rcb'], hooks['alub'])})
    entities.update({'add_br': Adder(32, hooks['pc8'], hooks['imm32'], hooks['branch'])})
    entities.update({'alu': Alu(hooks['rd1'], hooks['alub'], hooks['rd3'], hooks['alus'],
                                hooks['instr_11_7'], hooks['c'] hooks['shop'], hooks['shctrl']
                                hooks['accen'], hooks['aluf'], hooks['aluc'], hooks['aluv'],
                                hooks['alun'], hooks['aluz'])})
    entities.update({'aluflag_join': BusJoin([hooks['aluc'], hooks['aluv'],
                                              hooks['alun'], hooks['aluz']], hooks['aluflag'])})
    entities.update({'aluflag_reg': Register(4, hooks['clk'], hooks['rst'],
                                             hooks['aluflag'], hooks['flag'], enable=hooks['aluflagwr'])})
    entities.update({'flag_subset': BusSubset(hooks['flag'], [hooks['c'],
                                                              hooks['v'], hooks['n'], hooks['z']], [(0, 1), (1, 2), (2, 3), (3, 4)])})

    # MEMORY
    entities.update({'datamem': DataMemory(hooks['aluf'], hooks['rd2'], hooks['memwr'],
                                           hooks['rst'], hooks['clk'], hooks['memrd'], hooks['memty'])})
    entities.update({'memsignext': MemoryReadSignExtender(hooks['memrd'], hooks['memext'],
                                                          hooks['memrd_ext'])})

    # WRITE-BACK
    entities.update({'wdb_mux': Mux(32, [hooks['memrd_ext'], hooks['aluf']],
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
