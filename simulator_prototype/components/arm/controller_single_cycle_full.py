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
                 aluflagwr, memty, memwr, regsrc, wd3s):
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
        self._regsrc = regsrc
        self._wd3s = wd3s

    @staticmethod
    def _generate_pcsrc(conditionMet, op, rd):
        """
        PCSRC <= B"10" when a data processing instruction modifies pc
        PCSRC <= B"01" for pc+4
        PCSRC <= B"00" for branch instructions where condition is met
        """
        if op == ISA.OpCodes.BRANCH.value and conditionMet:
            return 0b00
        elif op == ISA.OpCodes.DATA_PROCESS.value and rd == 15:
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
    def _generate_regsa(op, shift, funct):
        """
        REGSA <= '1' to select Rn (data processing instructions)
        REGSA <= '0' to select Rn (mul instruction)
        """
        return not (op == ISA.OpCodes.DATA_PROCESS.value and ISA.is_multiply(funct, shift))

    @staticmethod
    def _generate_regdst(op, shift, funct):
        """
        REGDST <= B"10" to select Rd (str instruction)
        REGDST <= B"01" to select Rm (data processing intructions)
        REGDST <= B"00" to select Rm (mul instruction)
        """
        if op == ISA.OpCodes.MEMORY_SINGLE.value and not ISA.parse_function_get_l(funct):
            return 0b10
        elif op == ISA.OpCodes.DATA_PROCESS.value and ISA.is_multiply(funct, shift):
            return 0b00
        else:
            return 0b01

    @staticmethod
    def _generate_regsb(op, shift, funct):
        """
        REGSB <= '1' to select ra for data processing
        REGSB <= '0' to select ra for multiply and accumulate
        """
        return not (op == ISA.OpCodes.DATA_PROCESS.value and ISA.is_multiply(funct, shift))

    @staticmethod
    def _generate_regwrs(op, shift, funct):
        """
        REGWRS <= B"10" to select LR (bl instruction)
        REGWRS <= B"01" to select Rd (data processing instruction)
        REGWRS <= B"00" to select Rd (mul instruction)
        """
        if op == ISA.OpCodes.BRANCH.value and ISA.parse_function_get_l(funct, True):
            return 0b10
        elif op == ISA.OpCodes.DATA_PROCESS.value and ISA.is_multiply(funct, shift):
            return 0b00
        else:
            return 0b01

    @staticmethod
    def _generate_regwr(conditionMet, op, funct, rd):
        """
        REGWR <= '1' when an instruction writes back to the regfile
        REGWR <= '0' when an instruction does not write back to the regfile
             (str, branch, and cmp instructions)
        """
        if not conditionMet:
            return 0

        if rd == 15:  # PC not in register file, use PC path
            return 0b0
        elif op == ISA.OpCodes.DATA_PROCESS.value:
            cmd = ISA.parse_function_get_cmd(funct)
            if (cmd == ISA.DataCMDCodes.TST.value or
                cmd == ISA.DataCMDCodes.TEQ.value or
                cmd == ISA.DataCMDCodes.CMP.value or
                cmd == ISA.DataCMDCodes.CMN.value):
                return 0b0
            else:
                return 0b1
        elif op == ISA.OpCodes.MEMORY_SINGLE.value and not ISA.parse_function_get_l(funct):
            return 0b0
        elif op == ISA.OpCodes.BRANCH.value and ISA.parse_function_get_l(funct, True) == 0b0:
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
        if op == ISA.OpCodes.BRANCH.value:
            return 0b10
        elif op == ISA.OpCodes.MEMORY_SINGLE.value and not ISA.parse_function_get_i(funct):
            return 0b01
        else:
            return 0b00

    @staticmethod
    def _generate_alusrcb(op, funct):
        """
        ALUSRCB <= '1' when source B requires the output of RD2 (data
             processing instructions)
        ALUSRCB <= '0' when source B requires an extended immediate
        """
        if op == ISA.OpCodes.MEMORY_SINGLE.value and ISA.parse_function_get_i(funct):
            return 0b1
        elif op == ISA.OpCodes.DATA_PROCESS.value and not ISA.parse_function_get_i(funct):
            return 0b1
        else:
            return 0b0

    @staticmethod
    def _generate_alus(op, funct, shift):
        """
        ALUS <= "0000" for A + B
        ALUS <= "0001" for A - B
        ALUS <= "0010" for A & B
        ALUS <= "0011" for A | B
        ALUS <= "0100" for A ^ B
        ALUS <= "0101" for A
        ALUS <= "0110" for B
        ALUS <= "0111" for A * B
        ALUS <= "1000" for A + B + Cin
        ALUS <= "1001" for A - B - Cin
        ALUS <= "1010" for B - A
        ALUS <= "1011" for B - A - Cin
        ALUS <= "1100" for A & ~ B
        ALUS <= "1101" for ~ B
        ALUS <= "1110" for 0
        ALUS <= "1111" for 1
        """
        if op == ISA.OpCodes.DATA_PROCESS.value:
            if ISA.is_multiply(funct, shift):
                return 0b0111

            cmd = ISA.parse_function_get_cmd(funct)
            if cmd == ISA.DataCMDCodes.AND.value:
                return 0b0010
            elif cmd == ISA.DataCMDCodes.EOR.value:
                return 0b0100
            elif cmd == ISA.DataCMDCodes.SUB.value:
                return 0b0001
            elif cmd == ISA.DataCMDCodes.RSB.value:
                return 0b1010
            elif cmd == ISA.DataCMDCodes.ADD.value:
                return 0b0000
            elif cmd == ISA.DataCMDCodes.ADC.value:
                return 0b1000
            elif cmd == ISA.DataCMDCodes.SBC.value:
                return 0b1001
            elif cmd == ISA.DataCMDCodes.RSC.value:
                return 0b1011
            elif cmd == ISA.DataCMDCodes.TST.value:
                return 0b0010
            elif cmd == ISA.DataCMDCodes.TEQ.value:
                return 0b0100
            elif cmd == ISA.DataCMDCodes.CMP.value:
                return 0b0001
            elif cmd == ISA.DataCMDCodes.CMN.value:
                return 0b0000
            elif cmd == ISA.DataCMDCodes.ORR.value:
                return 0b0011
            elif cmd == ISA.DataCMDCodes.MOV.value:
                return 0b0110
            elif cmd == ISA.DataCMDCodes.BIC.value:
                return 0b1100
            elif cmd == ISA.DataCMDCodes.MVN.value:
                return 0b1101
            else:
                return 0b1111
        elif op == ISA.OpCodes.MEMORY_SINGLE.value:
            if ISA.parse_function_get_p(funct):  # pre-index
                return 0b0000 if ISA.parse_function_get_u(funct) else 0b0001
            else:  # post-index not supported, just pass A
                return 0b0101
        else:
            return 0b1111

    @staticmethod
    def _generate_shop(shift):
        """
        SHOP <= ShiftType from instruction
        """
        return ISA.parse_shift_operand_get_type(shift)

    @staticmethod
    def _generate_shctrl(op, funct, shift):
        """
        SHCTRL <= '00' diabled
        SHCTRL <= '01' enabled shift using constant for data processing instruction
        SHCTRL <= '10' diabled
        SHCTRL <= '11' enabled shift using register ra for data processing instruction
        """
        if op == ISA.OpCodes.DATA_PROCESS.value and not ISA.is_multiply(funct, shift):
            return (ISA.parse_shift_operand_get_roi(shift) << 1) | 1
        elif op == ISA.OpCodes.MEMORY_SINGLE.value and ISA.parse_function_get_i(funct):
            return (ISA.parse_shift_operand_get_roi(shift) << 1) | 1
        else:
            return 0b00

    @staticmethod
    def _generate_accen(op, funct, shift):
        """
        ACCEN <= '1' when accumulate set in multiply instruction (MLA)
        ACCEN <= '0' otherwise
        """
        if op == ISA.OpCodes.DATA_PROCESS.value and ISA.is_multiply(funct, shift):
            return ISA.parse_function_get_a(funct)
        else:
            return 0b0

    @staticmethod
    def _generate_aluflagwr(op, funct):
        """
        ALUFLAGWR <= '1' to set flags (cmp instructions or s bit set)
        ALUFLAGWR <= '0' flags will not be set
        """
        cmd = ISA.parse_function_get_cmd(funct)
        if op == ISA.OpCodes.DATA_PROCESS.value and (cmd == ISA.DataCMDCodes.TST.value or
                                                     cmd == ISA.DataCMDCodes.TEQ.value or
                                                     cmd == ISA.DataCMDCodes.CMP.value or
                                                     cmd == ISA.DataCMDCodes.CMN.value):
            return 0b1
        elif op == ISA.OpCodes.DATA_PROCESS.value and ISA.parse_function_get_s(funct):
            return 0b1
        else:
            return 0b0

    @staticmethod
    def _generate_memty(op, funct):
        """
        MEM_TY <= "00" --ignore
        MEM_TY <= "01" to read in byte mode
        MEM_TY <= "10" --ignore
        MEM_TY <= "11" to read in word mode
        """
        if op == ISA.OpCodes.MEMORY_SINGLE.value:
            return 0b01 if ISA.parse_function_get_b(funct) else 0b11
        else:
            return 0b11

    @staticmethod
    def _generate_memwr(conditionMet, op, funct):
        """
        MEMWR <= '1' allows data to be written to data memory (str
                 instructions)
        MEMWR <= '0' cannot write to data memory
        """
        if not conditionMet:
            return 0b0

        if op == ISA.OpCodes.MEMORY_SINGLE.value and not ISA.parse_function_get_l(funct):
            return 0b1
        else:
            return 0b0

    @staticmethod
    def _generate_regsrc(op, funct):
        """
        REGSRC <= '1' when output of ALU is feedback (ldr instructions)
        REGSRC <= '0' when output of data mem is feedback
        """
        if op == ISA.OpCodes.MEMORY_SINGLE.value and ISA.parse_function_get_l(funct):
            return 0b0
        else:
            return 0b1

    @staticmethod
    def _generate_wd3s(op, funct):
        """
        WDS3 <= '1' when a bl instruction is run else '0'
        """
        return op == ISA.OpCodes.BRANCH.value and ISA.parse_function_get_l(funct, True)

    def run(self, time=None):
        "Runs a timestep of controller, assert control signals on each"

        c = self._c.read()
        v = self._v.read()
        n = self._n.read()
        z = self._z.read()

        # parse instruction general
        instr = self._instr.read()
        conditionMet = ISA.condition_met(ISA.get_condition(instr), c, v, n, z)
        operation = ISA.get_opcode(instr)
        function = ISA.get_function(instr)
        shift = ISA.get_shift_operand(instr)
        rd = ISA.get_rd(instr, ISA.is_multiply(function, shift))

        self._pcsrc.write(self._generate_pcsrc(conditionMet, operation, rd))
        self._pcwr.write(self._generate_pcwr())
        self._regsa.write(self._generate_regsa(operation, shift, function))
        self._regdst.write(self._generate_regdst(operation, shift, function))
        self._regsb.write(self._generate_regsb(operation, shift, function))
        self._regwrs.write(self._generate_regwrs(operation, shift, function))
        self._regwr.write(self._generate_regwr(conditionMet, operation, function, rd))
        self._exts.write(self._generate_exts(operation, function))
        self._alusrcb.write(self._generate_alusrcb(operation, function))
        self._alus.write(self._generate_alus(operation, function, shift))
        self._shop.write(self._generate_shop(shift))
        self._shctrl.write(self._generate_shctrl(operation, function, shift))
        self._accen.write(self._generate_accen(operation, function, shift))
        self._aluflagwr.write(self._generate_aluflagwr(operation, function))
        self._memty.write(self._generate_memty(operation, function))
        self._memwr.write(self._generate_memwr(conditionMet, operation, function))
        self._regsrc.write(self._generate_regsrc(operation, function))
        self._wd3s.write(self._generate_wd3s(operation, function))

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
