"""
Single-cycle controller as derived by Larry Skuse's VHDL work.
"""

from components.abstract.controller import Controller
from components.abstract.ibus import iBusRead, iBusWrite
import components.arm.arm_v4_isa as ISA

class ControllerSingleCycle(Controller):
    """
    Single-cycle controller component implements architecture controller
    which will take a current instruction (broken into subfields) and ALU
    status flags. Output is the control paths for the architecture which
    will be enforced until the next instruction.
    """

    def __init__(self, instruction, c, v, n, z, pcsrc, pcwr, regsa, regdst,
                 regsb, regwrs, regwr, exts, alusrcb, alus, shop, shctrl, accen,
                 aluflagwr, memty, memwr, memext, regsrc, wd3s):
        """
        inputs:
            instruction: 32-bit ARMv4 instruction bus for current instruction
            c: carry bit
            v: signed overflow bit
            n: negative bit
            z: zero bit
        outputs:
            pcsrc: selects the instruction given to the fetch stage
            pcwr: always a 1 for the single cycle processor
            regsa: selects what register is passed into input ra1 of the regfile
            regdst: selects what register is passed into input ra2 of the regfile
            regsb: select what register is passed into input ra3 of the regfile
            regwrs: selects which register is passed into input wa of the regfile
            regwr: selects whether to write back to the regfile
            exts: selects the appropriate extension for an immediate
            alusrcb: selects what value input b of the alu recieves
            alus: selects the operation of the alu
            shop: barrel shifter opertion (left, logic right, arith right, rotate)
            shctrl: barrel shifter control signal (enable and mode)
            accen: accumulator enable
            aluflagwr: selects whether the c, v, n, and z flags need to be updated
            memty: memory mode (type of mem-word: off, byte, half, word)
            memwr: selects whether to write to memory
            memext: arithmetic extend on byte, half-word boundary
            regsrc: selects whether the alu output or data memory is feedback
            wd3s: selects what data to write to the regfile
        """

        if not isinstance(instruction, iBusRead):
            raise TypeError('Instruction bus must be readable')
        elif instruction.size() != 32:
            raise ValueError('Instruction bus must be 32-bits')
        if not isinstance(c, iBusRead):
            raise TypeError('The c bus must be readable')
        elif c.size() != 1:
            raise ValueError('The c bus must have a size of 1-bit')
        if not isinstance(v, iBusRead):
            raise TypeError('The v bus must be readable')
        elif v.size() != 1:
            raise ValueError('The v bus must have a size of 1-bit')
        if not isinstance(n, iBusRead):
            raise TypeError('The n bus must be readable')
        elif n.size() != 1:
            raise ValueError('The n bus must have a size of 1-bit')
        if not isinstance(z, iBusRead):
            raise TypeError('The z bus must be readable')
        elif z.size() != 1:
            raise ValueError('The z bus must have a size of 1-bit')

        self._instr = instruction
        self._c = c
        self._v = v
        self._n = n
        self._z = z

        # Control output buses
        if not isinstance(pcsrc, iBusRead):
            raise TypeError('The pcsrc bus must be writable')
        elif pcsrc.size() != 2:
            raise ValueError('The pcsrc bus must have a size of 2-bits')
        if not isinstance(pcwr, iBusRead):
            raise TypeError('The pcwr bus must be writable')
        elif pcwr.size() != 1:
            raise ValueError('The pcwr bus must have a size of 1-bit')
        if not isinstance(regsa, iBusRead):
            raise TypeError('The regsa bus must be writable')
        elif regsa.size() != 1:
            raise ValueError('The regsa bus must have a size of 1-bit')
        if not isinstance(regdst, iBusRead):
            raise TypeError('The regdst bus must be writable')
        elif regdst.size() != 2:
            raise ValueError('The regdst bus must have a size of 2-bits')
        if not isinstance(regsb, iBusRead):
            raise TypeError('The regsb bus must be writable')
        elif regsb.size() != 1:
            raise ValueError('The regsb bus must have a size of 1-bit')
        if not isinstance(regwrs, iBusRead):
            raise TypeError('The regwrs bus must be writable')
        elif regwrs.size() != 2:
            raise ValueError('The regwrs bus must have a size of 2-bits')
        if not isinstance(regwr, iBusRead):
            raise TypeError('The regwr bus must be writable')
        elif regwr.size() != 1:
            raise ValueError('The regwr bus must have a size of 1-bit')
        if not isinstance(exts, iBusRead):
            raise TypeError('The exts bus must be writable')
        elif exts.size() != 2:
            raise ValueError('The exts bus must have a size of 2-bits')
        if not isinstance(alusrcb, iBusRead):
            raise TypeError('The alusrcb bus must be writable')
        elif alusrcb.size() != 1:
            raise ValueError('The alusrcb bus must have a size of 1-bit')
        if not isinstance(alus, iBusRead):
            raise TypeError('The alus bus must be writable')
        elif alus.size() != 4:
            raise ValueError('The alus bus must have a size of 4-bits')
        if not isinstance(shop, iBusRead):
            raise TypeError('The shop bus must be writable')
        elif shop.size() != 2:
            raise ValueError('The shop bus must have a size of 2-bits')
        if not isinstance(shctrl, iBusRead):
            raise TypeError('The shctrl bus must be writable')
        elif shctrl.size() != 2:
            raise ValueError('The shctrl bus must have a size of 2-bits')
        if not isinstance(accen, iBusRead):
            raise TypeError('The accen bus must be writable')
        elif accen.size() != 1:
            raise ValueError('The accen bus must have a size of 1-bit')
        if not isinstance(aluflagwr, iBusRead):
            raise TypeError('The aluflagwr bus must be writable')
        elif aluflagwr.size() != 1:
            raise ValueError('The aluflagwr bus must have a size of 1-bit')
        if not isinstance(memty, iBusRead):
            raise TypeError('The memty bus must be writable')
        elif memty.size() != 2:
            raise ValueError('The memty bus must have a size of 2-bits')
        if not isinstance(memwr, iBusRead):
            raise TypeError('The memwr bus must be writable')
        elif memwr.size() != 1:
            raise ValueError('The memwr bus must have a size of 1-bit')
        if not isinstance(regsrc, iBusRead):
            raise TypeError('The regsrc bus must be writable')
        elif regsrc.size() != 1:
            raise ValueError('The regsrc bus must have a size of 1-bit')
        if not isinstance(memext, iBusRead):
            raise TypeError('The memext bus must be writable')
        elif memext.size() != 2:
            raise ValueError('The memext bus must have a size of 2-bits')
        if not isinstance(wd3s, iBusRead):
            raise TypeError('The wd3s bus must be writable')
        elif wd3s.size() != 1:
            raise ValueError('The wd3s bus must have a size of 1-bit')

        self._pcsrc = pcsrc
        self._pcwr = pcwr
        self._regsa = regsa
        self._regdst = regdst
        self._regsb = regsb
        self._regwrs = regwrs
        self._regwr = regwr
        self._exts = exts
        self._alusrcb = alusrcb
        self._alus = alus
        self._shop = shop
        self._shctrl = shctrl
        self._accen = accen
        self._aluflagwr = aluflagwr
        self._memty = memty
        self._memwr = memwr
        self._memext = memext
        self._regsrc = regsrc
        self._wd3s = wd3s


    @staticmethod
    def _generate_pcsrc(op, cond, rd, z):
        """
        PCSRC <= B"10" when a data processing instruction modifies pc
        PCSRC <= B"01" for pc+4
        PCSRC <= B"00" for branch instructions where condition is met
        """
        if op == 0b10 and cond == 0b1110:
            return 0b00
        elif op == 0b10 and cond == 0b0000 and z == 0b1:
            return 0b00
        elif op == 0b10 and cond == 0b0001 and z == 0b0:
            return 0b00
        elif op == 0b00 and rd == 0b1111:
            return 0b10
        else:
            return 0b01

    @staticmethod
    def _generate_pcwr():
        """
        PCWR <= '1' for single cycle processor
        """
        return 0b1

    @staticmethod
    def _generate_regsa(op, bit4, funct):
        """
        REGSA <= '1' to select Rn (data processing instructions)
        REGSA <= '0' to select Rn (mul instruction)
        """
        if op == 0b00 and bit4 == 0b1 and (funct == 0b000000 or funct == 0b000001):
            return 0b0
        else:
            return 0b1

    @staticmethod
    def _generate_regdst(op, bit4, funct):
        """
        REGDST <= B"10" to select Rd (str instruction)
        REGDST <= B"01" to select Rm (data processing intructions)
        REGDST <= B"00" to select Rm (mul instruction)
        """
        if op == 0b01 and funct == 0b011000:
            return 0b10
        elif op == 0b00 and bit4 == 0b1 and (funct == 0b000000 or funct == 0b000001):
            return 0b00
        else:
            return 0b01

    @staticmethod
    def _generate_regwrs(op, bit4, funct):
        """
        REGWRS <= B"10" to select LR (bl instruction)
        REGWRS <= B"01" to select Rd (data processing instruction)
        REGWRS <= B"00" to select Rd (mul instruction)
        """
        if op == 0b10 and ((funct & 0b010000) >> 4) == 0b1:
            return 0b10
        elif op == 0b00 and bit4 == 0b1 and (funct == 0b000000 or funct == 0b000001):
            return 0b00
        else:
            return 0b01

    @staticmethod
    def _generate_regwr(op, funct):
        """
        REGWR <= '1' when an instruction writes back to the regfile
        REGWR <= '0' when an instruction does not write back to the regfile
             (str, branch, and cmp instructions)
        """
        if op == 0b00 and (funct == 0b010101 or funct == 0b110101):
            return 0b0
        elif op == 0b01 and funct == 0b011000:
            return 0b0
        elif op == 0b10 and ((funct & 0b010000) >> 4) == 0b0:
            return 0b0
        else:
            return 0b1

    @staticmethod
    def _generate_exts(op, funct):
        """
        EXTS <= B"00" for 8-bit immediate (data processing immediate)
        EXTS <= B"01" for 12-bit immediate (ldr and str instructions)
        EXTS <= B"10" for branch instruction
        """
        if op == 0b10:
            return 0b10
        elif op == 0b01 and (funct == 0b011000 or funct == 0b011001):
            return 0b01
        else:
            return 0b00

    @staticmethod
    def _generate_alusrcb(op, funct, bit4):
        """
        ALUSRCB <= '1' when source B requires the output of RD2 (data
             processing instructions)
        ALUSRCB <= '0' when source B requires an extended immediate
        """
        if op == 0b00:
            if (funct == 0b000000 or funct == 0b000010 or
                    funct == 0b000100 or funct == 0b000110 or
                    funct == 0b001000 or funct == 0b001010 or
                    funct == 0b001110 or funct == 0b010001 or
                    funct == 0b010011 or funct == 0b010101 or
                    funct == 0b010111 or funct == 0b011000 or
                    funct == 0b011000 or funct == 0b011010 or
                    funct == 0b011100 or funct == 0b011110 or
                    funct == 0b000001 or funct == 0b000011 or
                    funct == 0b000101 or funct == 0b000111 or
                    funct == 0b001001 or funct == 0b001011 or
                    funct == 0b011011 or funct == 0b011101 or
                    funct == 0b011111):
                return 0b1
            elif bit4 == 0b1 and (funct == 0b000000 or funct == 0b000001):
                return 0b1
            else:
                return 0b0
        else:
            return 0b0

    @staticmethod
    def _generate_alus(op, bit4, funct):
        """
        ALUS <= "0000" for +
        ALUS <= "0001" for -
        ALUS <= "0010" for and
        ALUS <= "0011" for or
        ALUS <= "0100" for xor
        ALUS <= "0101" for A
        ALUS <= "0110" for B
        ALUS <= "0111" for A*B
        ALUS <= "1111" for 1
        """
        if op == 0b00 and (funct == 0b000000 or funct == 0b000001) and bit4 == 0b1:
            return 0b0111
        elif op == 0b00 and (funct == 0b001000 or funct == 0b101000
                             or funct == 0b001001 or funct == 0b101001):
            return 0b0000
        elif op == 0b01 and (funct == 0b011000 or funct == 0b011001):
            return 0b0000
        elif op == 0b00 and (funct == 0b000100 or funct == 0b100100
                             or funct == 0b010101 or funct == 0b110101 or funct == 0b000101
                             or funct == 100101):
            return 0b0001
        elif op == 0b00 and (funct == 0b000000 or funct == 0b100000
                             or funct == 0b000001 or funct == 0b100001):
            return 0b0010
        elif op == 0b00 and (funct == 0b011000 or funct == 0b111000
                             or funct == 0b011001 or funct == 0b111001):
            return 0b0011
        elif op == 0b00 and (funct == 0b000010 or funct == 0b100010
                             or funct == 0b000011 or funct == 0b100011):
            return 0b0100
        elif op == 0b00 and (funct == 0b011010 or funct == 0b111010
                             or funct == 0b011011 or funct == 0b111011):
            return 0b0110
        else:
            return 0b1111

    @staticmethod
    def _generate_aluflagwr(op, funct):
        """
        ALUFLAGWR <= '1' to set flags (cmp instructions or s bit set)
        ALUFLAGWR <= '0' flags will not be set
        """
        if op == 0b00:
            # Note: need to look further into the logic when funct is 1
            if (funct == 0b010101 or funct == 0b110101 or
                    funct == 0b000001 or funct == 0b100001 or
                    funct == 0b000011 or funct == 0b100011 or
                    funct == 0b000101 or funct == 0b100101 or
                    funct == 0b000111 or funct == 0b100111 or
                    funct == 0b001001 or funct == 0b101001 or
                    funct == 0b001011 or funct == 0b101011 or
                    funct == 0b001101 or funct == 0b101101 or
                    funct == 0b001111 or funct == 0b101111 or
                    funct == 0b010001 or funct == 0b110001 or
                    funct == 0b010011 or funct == 0b110011 or
                    funct == 0b010111 or funct == 0b110111 or
                    funct == 0b011001 or funct == 0b111001 or
                    funct == 0b011011 or funct == 0b111011 or
                    funct == 0b011101 or funct == 0b111101 or
                    funct == 0b011111 or funct == 0b111111):
                return 0b1
            else:
                return 0b0
        else:
            return 0b0

    @staticmethod
    def _generate_memwr(op, funct):
        """
        MEMWR <= '1' allows data to be written to data memory (str
                 instructions)
        MEMWR <= '0' cannot write to data memory
        """
        if op == ISA.OpCodes.SINGLE_MEMORY and funct == 0b011000:
            return 0b1
        else:
            return 0b0

    @staticmethod
    def _generate_regsrc(op, funct):
        """
        REGSRC <= '1' when output of ALU is feedback (ldr instructions)
        REGSRC <= '0' when output of data mem is feedback
        """
        if op == ISA.OpCodes.SINGLE_MEMORY and funct == 0b011001:
            return 0b0
        else:
            return 0b1

    @staticmethod
    def _generate_wd3s(op, funct):
        """
        WDS3 <= '1' when a bl instruction is run else '0'
        """
        if op == ISA.OpCodes.BRANCH and ((funct & 0b010000) >> 4) == 0b1:
            return 0b1
        else:
            return 0b0


    def run(self, time=None):
        "Runs a timestep of controller, assert control signals on each"

        #parse instruction general
        instr = self._instr.read()
        condition = (instr & ISA.InstructionMasks.COND) >> 28
        operation = (instr & ISA.InstructionMasks.OPCODE) >> 26

    def inspect(self):
        "Return message noting that this controller does not contain state"
        return {'type': 'sc-controller', 'state': None}

    def modify(self, data=None):
        "Return message noting that this controller does not contain state"
        return {'error': 'sc-controller does not contain state'}

    def clear(self):
        "Not implemented for single cycle"
        return {'error': 'sc-controller does not contain state'}

    def on_rising_edge(self):
        "Not implemented for single cycle"
        pass

    def on_falling_edge(self):
        "Not implemented for single cycle"
        pass

    def on_reset(self):
        "Not implemented for single cycle"
        pass
