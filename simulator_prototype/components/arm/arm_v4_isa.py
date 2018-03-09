"""
ARM v4 ISA Enumeration File

Purpose is to contain all relevant information pertaining to ARM v4.
Specifically so that architecture controllers can be developed around a common
set of enumerations.
"""

from enum import Enum


def get_condition(instr):
    return (instr & 0xF0000000) >> 28


def get_opcode(instr):
    return (instr & 0x0C000000) >> 26


def get_function(instr):
    return (instr & 0x03F00000) >> 20


def parse_function_get_i(funct):
    return (funct & 0b100000) >> 5


def parse_function_get_cmd(funct, alt=False):
    if alt:
        return (funct & 0b001110) >> 1
    else:
        return (funct & 0b011110) >> 1


def parse_function_get_s(funct):
    return (funct & 0b000001) >> 0  # aluflag save


def parse_function_get_p(funct):
    return (funct & 0b010000) >> 4  # pre/post indexing bit 1 = pre


def parse_function_get_u(funct):
    return (funct & 0b001000) >> 3  # up/down bit (offset modification) 1 = up


def parse_function_get_b(funct):
    return (funct & 0b000100) >> 2  # unsigned byte is 1 else word


def parse_function_get_w(funct):
    return (funct & 0b000010) >> 1  # write-back to base


def parse_function_get_l(funct, alt=False):
    if alt:
        return (funct & 0b010000) >> 4  # link
    else:
        return (funct & 0b000001) >> 0  # load/store


def parse_function_get_a(funct):
    return (funct & 0b000010) >> 1


def get_rn(instr, alt=False):
    if alt:
        return (instr & 0x0000000F) >> 0
    else:
        return (instr & 0x000F0000) >> 16


def get_rd(instr, alt=False):
    if alt:
        return (instr & 0x000F0000) >> 16
    else:
        return (instr & 0x0000F000) >> 12


def get_rm(instr, alt=False):
    if alt:
        return (instr & 0x00000F00) >> 8
    else:
        return (instr & 0x0000000F) >> 0


def get_ra(instr, alt=False):
    if alt:
        return (instr & 0x0000F000) >> 12
    else:
        return (instr & 0x00000F00) >> 8


def get_shift_operand(instr):
    return (instr & 0x00000FF0) >> 4


def parse_shift_operand_get_roi(shift):
    return (shift & 0x01) >> 0


def parse_shift_operand_get_type(shift):
    return (shift & 0x06) >> 1


def parse_shift_operand_get_reg_fill(shift):
    return (shift & 0x08) >> 3


def is_multiply(funct, shift):
    if parse_function_get_cmd(funct) & 0xE or parse_function_get_i(funct):
        return False
    elif parse_shift_operand_get_roi(shift) and parse_shift_operand_get_reg_fill(shift):
        return True
    else:
        return False


def condition_met(cond, c, v, n, z):
    if cond == ConditionField.EQ.value:
        return z
    elif cond == ConditionField.NE.value:
        return not z
    elif cond == ConditionField.CS.value:
        return c
    elif cond == ConditionField.CC.value:
        return not c
    elif cond == ConditionField.MI.value:
        return n
    elif cond == ConditionField.PL.value:
        return not n
    elif cond == ConditionField.VS.value:
        return v
    elif cond == ConditionField.VC.value:
        return not v
    elif cond == ConditionField.HI.value:
        return c and not z
    elif cond == ConditionField.LS.value:
        return not c or z
    elif cond == ConditionField.GE.value:
        return n == v
    elif cond == ConditionField.LT.value:
        return n != v
    elif cond == ConditionField.GT.value:
        return not z and (n == v)
    elif cond == ConditionField.LE.value:
        return ((z or n) and not v) or (not n and v)
    elif cond == ConditionField.AL.value:
        return True
    else:
        return False


class ConditionField(Enum):
    EQ = 0b0000  # Z set (equal)
    NE = 0b0001  # Z clear (not equal)
    CS = 0b0010  # C set (unsigned higher or same)
    CC = 0b0011  # C clear (unsigned lower)
    MI = 0b0100  # N set (negative)
    PL = 0b0101  # N clear (positive or zero)
    VS = 0b0110  # V set (overflow)
    VC = 0b0111  # V clear (no overflow)
    HI = 0b1000  # C set and Z clear (unsigned higher)
    LS = 0b1001  # C clear or Z set (unsigned lower or same)
    GE = 0b1010  # N set and V set, or N clear and V clear (greater or equal)
    LT = 0b1011  # N set and V clear, or N clear and V set (less than)
    GT = 0b1100  # Z clear, and either N set and V set, or N clear and V clear (greater than)
    LE = 0b1101  # Z set, or N set and V clear, or N clear and V set (less than or equal)
    AL = 0b1110  # Always
    NV = 0b1111  # Never


class OpCodes(Enum):
    DATA_PROCESS = 0  # register, immediate, and multiply
    MEMORY_SINGLE = 1  # Read and write
    MEMORY_MULTIPLE = 2  # Access range not supported
    BRANCH = 2  # PC manipulation
    IGNORE = 3  # coprocessor, software interrupt not supported


class DataCMDCodes(Enum):
    AND = 0b0000  # and
    EOR = 0b0001  # exculsive or
    SUB = 0b0010  # subtract
    RSB = 0b0011  # reverse subtract
    ADD = 0b0100  # add
    ADC = 0b0101  # add with carry
    SBC = 0b0110  # subtract with carry
    RSC = 0b0111  # reverse subtract with carry
    TST = 0b1000  # test (as and)
    TEQ = 0b1001  # test (as exculsive or)
    CMP = 0b1010  # test (as subtract)
    CMN = 0b1011  # test (as add)
    ORR = 0b1100  # or
    MOV = 0b1101  # move
    BIC = 0b1110  # and not
    MVN = 0b1111  # not


class ShiftType(Enum):
    LL = 0b00  # logical left shift
    LR = 0b01  # logical right shift
    AR = 0b10  # arithmetic right shift
    RR = 0b11  # rotate right
