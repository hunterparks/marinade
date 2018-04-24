
from simulator.components.arm.alu_demo import Alu as AluDemo
from simulator.components.arm.alu_flag_register import ALUFlagRegister
from simulator.components.arm.alu_full import Alu as AluFull
from simulator.components.arm.controller_pipeline import ControllerPipeline
from simulator.components.arm.controller_single_cycle_demo import ControllerSingleCycle as ControllerSingleCycleDemo
from simulator.components.arm.controller_single_cycle_full import ControllerSingleCycle as ControllerSingleCycleFull
from simulator.components.arm.data_memory import DataMemory
from simulator.components.arm.exmem import Exmem
from simulator.components.arm.extender import Extender
from simulator.components.arm.hazard import HazardController
from simulator.components.arm.idex import Idex
from simulator.components.arm.ifid import Ifid
from simulator.components.arm.memory_read_sign_extend import MemoryReadSignExtender
from simulator.components.arm.memwb import Memwb
from simulator.components.arm.program_memory import ProgramMemory
from simulator.components.arm.register_file_demo import RegisterFile as RegisterFileDemo
from simulator.components.arm.register_file_full import RegisterFile as RegisterFileFull

ArmPackage = {
    "AluDemo": AluDemo,
    "AluFlagRegister": ALUFlagRegister,
    "AluFull": AluFull,
    "ControllerPipeline": ControllerPipeline,
    "ControllerSingleCycleDemo": ControllerSingleCycleDemo,
    "ControllerSingleCycleFull": ControllerSingleCycleFull,
    "DataMemory": DataMemory,
    "Exmem": Exmem,
    "Extender": Extender,
    "HazardController": HazardController,
    "Idex": Idex,
    "Ifid": Ifid,
    "MemoryReadSignExtender": MemoryReadSignExtender,
    "Memwb": Memwb,
    "ProgramMemory": ProgramMemory,
    "RegisterFileDemo": RegisterFileDemo,
    "RegisterFileFull": RegisterFileFull
}
