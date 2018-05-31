"""
Pass test cases to importer for test suite
"""

import sys
sys.path.insert(0, '../../../')

from simulator.tests.arm.alu_demo_t import Alu_t as AluDemo_t
from simulator.tests.arm.alu_full_t import Alu_t as AluFull_t
from simulator.tests.arm.extender_t import Extender_t
from simulator.tests.arm.data_memory_t import DataMemory_t
from simulator.tests.arm.program_memory_t import ProgramMemory_t
from simulator.tests.arm.register_file_demo_t import RegisterFile_Demo_t
from simulator.tests.arm.register_file_full_t import RegisterFile_Full_t
from simulator.tests.arm.controller_single_cycle_demo_t import ControllerSingleCycle_t as ControllerSingleCycleDemo_t
from simulator.tests.arm.controller_single_cycle_full_t import ControllerSingleCycle_t as ControllerSingleCycleFull_t
from simulator.tests.arm.memory_read_sign_extend_t import MemoryReadSignExtender_t
from simulator.tests.arm.alu_flag_register_t import ALUFlagRegister_t
