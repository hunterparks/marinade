"""
Pipeline Proof of Concept

This module defines a proof of concept architecture for a simulated ARM
CPU. Note that the architecture is incomplete as some instructions /
instruction variants are unsupported.

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
from components.arm.controller_pipeline import ControllerPipeline
from components.arm.ifid import Ifid
from components.arm.idex import Idex
from components.arm.exmem import Exmem
from components.arm.memwb import Memwb
from components.arm.controller_pipeline import ControllerPipeline
from components.arm.hazard import HazardController

from architecture import Architecture


def program_pipeline_architecture(arch, program):
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


def generate_pipeline_architecture():
    "Illustrates the necessary process to construct an architecture"

    ########## define system resources ##########
    clk = Clock(10, 0)
    rst = Reset(0)
    hooks = OrderedDict([('clk', clk), ('rst', rst)])

    ########## define input hooks and constants ##########
    hooks.update({'const4': Constant(32, 4)})
    hooks.update({'const8': Constant(32, 8)})
    hooks.update({'const14': Constant(4, 14)})

    ########## define buses ##########
    hooks.update({'pc': Bus(32, 0)})
    hooks.update({'pc4': Bus(32, 0)})
    hooks.update({'pc8': Bus(32, 0)})
    hooks.update({'braddr': Bus(32, 0)})
    hooks.update({'nextaddr': Bus(32, 0)})
    hooks.update({'instrf': Bus(32, 0)})
    hooks.update({'instrd': Bus(32, 0)})
    hooks.update({'instrd_31_28': Bus(4, 0)})
    hooks.update({'instrd_27_26': Bus(2, 0)})
    hooks.update({'instrd_25_20': Bus(6, 0)})
    hooks.update({'instrd_19_16': Bus(4, 0)})
    hooks.update({'instrd_15_12': Bus(4, 0)})
    hooks.update({'instrd_11_8': Bus(4, 0)})
    hooks.update({'instrd_4': Bus(1, 0)})
    hooks.update({'instrd_3_0': Bus(4, 0)})
    hooks.update({'instrd_23_0': Bus(24, 0)})
    hooks.update({'imm32d': Bus(32, 0)})
    hooks.update({'imm32e': Bus(32, 0)})
    hooks.update({'rdm': Bus(32, 0)})
    hooks.update({'rdw': Bus(32, 0)})
    hooks.update({'rd1': Bus(32, 0)})
    hooks.update({'rd2': Bus(32, 0)})
    hooks.update({'rd1d': Bus(32, 0)})
    hooks.update({'rd2d': Bus(32, 0)})
    hooks.update({'rd1e': Bus(32, 0)})
    hooks.update({'rd2e': Bus(32, 0)})
    hooks.update({'rd2m': Bus(32, 0)})
    hooks.update({'ra1d': Bus(4, 0)})
    hooks.update({'ra2d': Bus(4, 0)})
    hooks.update({'ra3d': Bus(4, 0)})
    hooks.update({'ra1e': Bus(4, 0)})
    hooks.update({'ra2e': Bus(4, 0)})
    hooks.update({'ra3e': Bus(4, 0)})
    hooks.update({'ra3m': Bus(4, 0)})
    hooks.update({'ra3w': Bus(4, 0)})
    hooks.update({'fe': Bus(32, 0)})
    hooks.update({'fm': Bus(32, 0)})
    hooks.update({'fw': Bus(32, 0)})
    hooks.update({'alub': Bus(32, 0)})
    hooks.update({'aluc': Bus(1, 0)})
    hooks.update({'aluv': Bus(1, 0)})
    hooks.update({'alun': Bus(1, 0)})
    hooks.update({'aluz': Bus(1, 0)})
    hooks.update({'c': Bus(1, 0)})
    hooks.update({'v': Bus(1, 0)})
    hooks.update({'n': Bus(1, 0)})
    hooks.update({'z': Bus(1, 0)})
    hooks.update({'aluflag': Bus(4, 0)})
    hooks.update({'flag': Bus(4, 0)})
    hooks.update({'data': Bus(32, 0)})
    hooks.update({'wd': Bus(32, 0)})
    hooks.update({'wd3': Bus(32, 0)})

    ########## control signals ##########
    # decode stage
    hooks.update({'pcsrcd': Bus(2, 0)})
    hooks.update({'pcwrd': Bus(1, 0)})
    hooks.update({'regsad': Bus(1, 0)})
    hooks.update({'regdstd': Bus(2, 0)})
    hooks.update({'regwrsd': Bus(2, 0)})
    hooks.update({'regwrd': Bus(1, 0)})
    hooks.update({'extsd': Bus(2, 0)})
    hooks.update({'alusrcbd': Bus(1, 0)})
    hooks.update({'alusd': Bus(4, 0)})
    hooks.update({'aluflagwrd': Bus(1, 0)})
    hooks.update({'memwrd': Bus(1, 0)})
    hooks.update({'regsrcd': Bus(1, 0)})
    hooks.update({'wd3sd': Bus(1, 0)})
    # execute stage
    hooks.update({'pcsrce': Bus(2, 0)})
    hooks.update({'regwrse': Bus(2, 0)})
    hooks.update({'regwre': Bus(1, 0)})
    hooks.update({'alusrcbe': Bus(1, 0)})
    hooks.update({'aluse': Bus(4, 0)})
    hooks.update({'aluflagwre': Bus(1, 0)})
    hooks.update({'memwre': Bus(1, 0)})
    hooks.update({'regsrce': Bus(1, 0)})
    hooks.update({'wd3se': Bus(1, 0)})
    # memory stage
    hooks.update({'pcsrcm': Bus(2, 0)})
    hooks.update({'regwrsm': Bus(2, 0)})
    hooks.update({'regwrm': Bus(1, 0)})
    hooks.update({'memwrm': Bus(1, 0)})
    hooks.update({'regsrcm': Bus(1, 0)})
    hooks.update({'wd3sm': Bus(1, 0)})
    # write back stage
    hooks.update({'pcsrcw': Bus(2, 0)})
    hooks.update({'regwrsw': Bus(2, 0)})
    hooks.update({'regwrw': Bus(1, 0)})
    hooks.update({'regsrcw': Bus(1, 0)})
    hooks.update({'wd3sw': Bus(1, 0)})

    ########## hazard control signals ##########
    hooks.update({'fwda': Bus(2, 0)})
    hooks.update({'fwdb': Bus(2, 0)})
    hooks.update({'fwds': Bus(1, 0)})
    hooks.update({'stalld': Bus(1, 0)})
    hooks.update({'flushd': Bus(1, 0)})
    hooks.update({'flushe': Bus(1, 0)})

    ########## generate components ##########
    entities = OrderedDict([('clk', clk)])
    # memwb
    entities.update({'memwb': Memwb(hooks['pcsrcm'], hooks['regwrsm'], hooks['regwrm'],
                                   hooks['regsrcm'], hooks['wd3sm'], hooks['fm'], hooks['rdm'],
                                   hooks['ra3m'], hooks['clk'], hooks['pcsrcw'], hooks['regwrsw'],
                                   hooks['regwrw'], hooks['regsrcw'], hooks['wd3sw'],
                                   hooks['fw'], hooks['rdw'], hooks['ra3w'])})
    # exmem
    entities.update({'exmem': Exmem(hooks['pcsrce'], hooks['regwrse'], hooks['regwre'], 
                                    hooks['memwre'], hooks['regsrce'], hooks['wd3se'], 
                                    hooks['rd2'], hooks['fe'], hooks['ra3e'], hooks['clk'],
                                    hooks['pcsrcm'], hooks['regwrsm'], hooks['regwrm'],
                                    hooks['memwrm'], hooks['regsrcm'], hooks['wd3sm'],
                                    hooks['fm'], hooks['rd2m'], hooks['ra3m'])})
    # idex register
    entities.update({'idex': Idex(hooks['pcsrcd'], hooks['regwrsd'], hooks['regwrd'], 
                                  hooks['alusrcbd'], hooks['alusd'], hooks['aluflagwrd'],
                                  hooks['memwrd'], hooks['regsrcd'], 
                                  hooks['wd3sd'], hooks['rd1d'], hooks['rd2d'], hooks['imm32d'],
                                  hooks['ra1d'], hooks['ra2d'], hooks['ra3d'], hooks['flushe'],
                                  hooks['clk'], hooks['pcsrce'], hooks['regwrse'], hooks['regwre'],
                                  hooks['alusrcbe'], hooks['aluse'], hooks['aluflagwre'],
                                  hooks['memwre'], hooks['regsrce'], hooks['wd3se'], hooks['rd1e'],
                                  hooks['rd2e'], hooks['imm32e'], hooks['ra1e'], hooks['ra2e'],
                                  hooks['ra3e'])})
    # ifid
    entities.update({'ifid': Ifid(hooks['instrf'], hooks['stalld'], hooks['flushd'], hooks['clk'], 
                                  hooks['instrd'])})
    # fetch
    entities.update({'pc_reg': Register(32, hooks['clk'], hooks['rst'],
                                        hooks['nextaddr'], hooks['pc'], 0, enable=hooks['pcwrd'])})
    entities.update({'add8': Adder(32, hooks['pc'], hooks['const8'], hooks['pc8'])})
    entities.update({'add4': Adder(32, hooks['pc'], hooks['const4'], hooks['pc4'])})
    entities.update({'progmem': ProgramMemory(hooks['pc'], hooks['rst'], hooks['clk'], 
                                              hooks['instrf'])})
    # decode
    entities.update({'instr_subset': BusSubset(hooks['instrd'],  
                                               [hooks['instrd_23_0'], hooks['instrd_31_28'],
                                                hooks['instrd_27_26'], hooks['instrd_25_20'],
                                                hooks['instrd_19_16'], hooks['instrd_15_12'],
                                                hooks['instrd_11_8'], hooks['instrd_4'],
                                                hooks['instrd_3_0']],
                                               [(0, 24), (28, 32), (26, 28), (20, 26), (16, 20), (12, 16), (8, 12), (4, 5), (0, 4)])})
    entities.update({'controller': ControllerPipeline(hooks['instrd_31_28'], hooks['instrd_27_26'], 
                                                      hooks['instrd_25_20'], hooks['instrd_15_12'], 
                                                      hooks['instrd_4'], hooks['c'], hooks['v'], 
                                                      hooks['n'], hooks['z'], hooks['stalld'], 
                                                      hooks['pcsrcd'], hooks['pcwrd'], hooks['regsad'],
                                                      hooks['regdstd'], hooks['regwrsd'], hooks['regwrd'],
                                                      hooks['extsd'], hooks['alusrcbd'], hooks['alusd'],
                                                      hooks['aluflagwrd'], hooks['memwrd'], 
                                                      hooks['regsrcd'], hooks['wd3sd'])})
    entities.update({'ra1_mux': Mux(4, [hooks['instrd_3_0'], hooks['instrd_19_16']], hooks['regsad'], 
                                    hooks['ra1d'])})
    entities.update({'ra2_mux': Mux(4, [hooks['instrd_11_8'], hooks['instrd_3_0'], hooks['instrd_15_12']], 
                                    hooks['regdstd'], hooks['ra2d'])})
    entities.update({'ra3_mux': Mux(4, [hooks['instrd_19_16'], hooks['instrd_15_12'], hooks['const14']], 
                                    hooks['regwrsd'], hooks['ra3d'])})
    entities.update({'extimm': Extender(hooks['instrd_23_0'], hooks['extsd'], hooks['imm32d'])})
    entities.update({'add_branch': Adder(32, hooks['pc8'], hooks['imm32d'], hooks['braddr'])})
    entities.update({'regfile': RegisterFile(hooks['clk'], hooks['rst'], hooks['regwrw'], hooks['wd'],
                                             hooks['ra1d'], hooks['ra2d'], hooks['ra3w'], hooks['rd1d'], 
                                             hooks['rd2d'], edge_type=Latch_Type.FALLING_EDGE)})
    # execute
    entities.update({'hazard_controller': HazardController(hooks['ra1d'], hooks['ra2d'], 
                                                           hooks['ra1e'], hooks['ra2e'],
                                                           hooks['ra3e'], hooks['ra3m'],
                                                           hooks['ra3w'], hooks['regwrm'],
                                                           hooks['regwrw'], hooks['regsrce'],
                                                           hooks['regsrcw'], hooks['memwrm'],
                                                           hooks['pcsrcd'], hooks['fwda'],
                                                           hooks['fwdb'], hooks['fwds'],
                                                           hooks['stalld'], hooks['flushd'],
                                                           hooks['flushe'])})
    entities.update({'fwda_mux': Mux(32, [hooks['rd1e'], hooks['fm'], hooks['fw'], hooks['rdw']],
                                      hooks['fwda'], hooks['rd1'])})
    entities.update({'fwdb_mux': Mux(32, [hooks['rd2e'], hooks['fm'], hooks['fw'], hooks['rdw']],
                                      hooks['fwdb'], hooks['rd2'])})
    entities.update({'alu_mux': Mux(32, [hooks['imm32e'], hooks['rd2']], hooks['alusrcbe'], 
                                    hooks['alub'])})
    entities.update({'alu': Alu(hooks['rd1'], hooks['alub'], hooks['aluse'], hooks['fe'], 
                                hooks['aluc'], hooks['aluv'], hooks['alun'], hooks['aluz'])})
    entities.update({'aluflag_join': BusJoin([hooks['aluc'], hooks['aluv'], hooks['alun'], 
                                             hooks['aluz']], hooks['aluflag'])})
    entities.update({'aluflag_reg': Register(4, hooks['clk'], hooks['rst'],
                                             hooks['aluflag'], hooks['flag'], 
                                             enable=hooks['aluflagwre'])})
    entities.update({'flag_subset': BusSubset(hooks['flag'], [hooks['c'],
                                              hooks['v'], hooks['n'], hooks['z']], [(0, 1), (1, 2),
                                              (2, 3), (3, 4)])})
    # memory
    entities.update({'fwds_mux': Mux(32, [hooks['rd2m'], hooks['wd3']], hooks['fwds'], 
                                     hooks['data'])})
    entities.update({'datamem': DataMemory(hooks['fm'], hooks['data'], hooks['memwrm'],
                                           hooks['rst'], hooks['clk'], hooks['rdm'])})
    # writeback
    entities.update({'wd3_mux': Mux(32, [hooks['rdw'], hooks['fw']],
                                    hooks['regsrcw'], hooks['wd3'])})
    entities.update({'rwd_mux': Mux(32, [hooks['wd3'], hooks['pc4']], hooks['wd3sw'], hooks['wd'])})
    entities.update({'addr_mux': Mux(32, [hooks['braddr'], hooks['pc4'], hooks['wd3']], 
                                     hooks['pcsrcd'], hooks['nextaddr'])})

    # place memory (Internal) hooks into hook list
    hooks.update({'pc_reg': entities['pc_reg']})
    hooks.update({'progmem': entities['progmem']})
    hooks.update({'regfile': entities['regfile']})
    hooks.update({'aluflag_reg': entities['aluflag_reg']})
    hooks.update({'datamem': entities['datamem']})
    hooks.update({'controller': entities['controller']})
    #hooks.update({'hazard_controller': entities['hazard_controller']})
    hooks.update({'ifid': entities['ifid']})
    hooks.update({'idex': entities['idex']})
    hooks.update({'exmem': entities['exmem']})
    hooks.update({'memwb': entities['memwb']})

    # generate simulatable architecture
    arch = Architecture(0.0001, clk, rst, hooks, entities)
    return arch, hooks
