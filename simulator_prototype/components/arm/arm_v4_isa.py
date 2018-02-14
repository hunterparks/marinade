"""
ARM v4 ISA Enumeration File

Purpose is to contain all relevant information pertaining to ARM v4.
Specifically so that architecture controllers can be developed around a common
set of enumerations.
"""

from enum import Enum

class InstructionMasks(Enum):
    "Main definitions used for general parsing"
    COND = 0xF0000000
    OPCODE = 0x0C000000
    FUNCT = 0x03E00000
    S = 0x00100000


class InstructionMasksFull(Enum):
    "Full definitions for all instruction parsing"
    COND = 0xF0000000
    OPCODE = 0x0C000000

    class DataProcessing(Enum):
        I = 0x02000000
        CMD = 0x01E00000
        S = 0x00100000
        RN = 0x000F0000
        RD = 0x0000F000
        OPERAND2 = 0x000003FF

        class ImmediateOperand2(Enum):
            ROTATE = 0x00000F00
            IMMEDIATE = 0x000000FF

        class RegisterOperand2(Enum):
            ROC = 0x00000010
            RM = 0x0000000F
            SHIFT_TYPE = 0x00000060

            class ShiftConstant(Enum):
                SHIFT_AMOUNT = 0x00000F80

            class ShiftRegister(Enum):
                RS = 0x00000F00
                FILL = 0x00000080  # value  = 0b0

    class Multiply(Enum):  # TODO fix this
        FILL_1 = 0x03000000  # value = 0b00
        CMD = 0x00E00000
        S = 0x00100000
        RD = 0x0000F000
        RA = 0x000F0000
        RM = 0x00000F00
        FILL_2 = 0x000000F0  # value = 0b1001
        RN = 0x0000000F

    class SingleDataSwap(Enum):
        "Ignored by controller implementation"
        FILL_1 = 0x03800000  # value = 0b00010
        B = 0x00400000
        FILL_2 = 0x00300000  # value = 0b00
        RN = 0x000F0000
        RD = 0x0000F000
        FILL_3 = 0x00000F00  # value = 0b0000
        FILL_4 = 0x000000F0  # value = 0b1001
        RM = 0x0000000F

    class SingleDataTransfer(Enum):
        I = 0x02000000
        P = 0x01000000
        U = 0x00800000
        B = 0x00400000
        W = 0x00200000
        L = 0x00100000
        RN = 0x000F0000
        RD = 0x0000F000
        IMMEDIATE = 0x00000FFF

    class Undefined(Enum):
        "Ignored by controller implementation"
        FILL_1 = 0x01000000  # value = 0b1
        DONT_CARE_1 = 0x00FFFFE0
        FILL_2 = 0x00000010  # value = 0b1
        DONT_CARE_2 = 0x0000000F

    class BlockDataTransfer(Enum):
        "Ignored by controller implementation"
        FILL = 0x01000000
        P = 0x01000000
        U = 0x00800000
        B = 0x00400000
        W = 0x00200000
        L = 0x00100000
        RN = 0x000F0000
        REGLIST = 0x0000FFFF

    class Branch(Enum):
        FILL = 0x01000000  # value = 0b1
        L = 0x01000000
        IMMEDIATE = 0x00FFFFFF

    class CoprocessorDataTransfer(Enum):
        "Ignored by controller implementation"
        FILL = 0x01000000
        P = 0x01000000
        U = 0x00800000
        B = 0x00400000
        W = 0x00200000
        L = 0x00100000
        RN = 0x000F0000
        CRD = 0x0000F000
        CPN = 0x00000F00
        OFFSET = 0x000000FF

    class CoprocessorDataOperation(Enum):
        "Ignored by controller implementation"
        FILL_1 = 0x03000000  # value = 0b10
        CP_OPC = 0x00F00000
        CRN = 0x000F0000
        CRD = 0x0000F000
        CPN = 0x00000F00
        CP = 0x000000E0
        FILL_2 = 0x00000010  # value  = 0b0
        CRM = 0x0000000F

    class CoprocessorRegisterTransfer(Enum):
        "Ignored by controller implementation"
        FILL_1 = 0x03000000  # value = 0b10
        CP_OPC = 0x00E00000
        L = 0x00100000
        CRN = 0x000F0000
        RD = 0x0000F000
        CPN = 0x00000F00
        CP = 0x000000E0
        FILL_2 = 0x00000010  # value  = 0b1
        CRM = 0x0000000F

    class SoftwareInterrupt(Enum):
        "Ignored by controller implementation"
        FILL = 0x03000000  # value = 0b11
        IGNORE_BY_PROC = 0x00FFFFFF


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
    DATA_PROCESS = 0b00
    SINGLE_MEMORY = 0b01
    BRANCH = 0b10  # also memory multiple on this opcode
    IGNORE = 0b11  # coprocessor, software interrupt


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
