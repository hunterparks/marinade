from simulator.components.abstract.controller import Controller
from simulator.components.abstract.ibus import iBusRead, iBusWrite


class ControllerPipeline(Controller):
    "Pipeline Controller - Implements pipeline architecture controller"


    def __init__(self, cond, op, funct, rd, bit4, c, v, n, z, stallf, pcsrcd,
                 pcwrd, regsad, regdstd, regwrsd, regwrd, extsd, alusrcbd, 
                 alusd, aluflagwrd, memwrd, regsrcd, wd3sd):
        """
        inputs:
            cond: 4-bits that represent bits 31..28 of the instruction
            op: 2-bits that represent bits 27..26 of the instruction
            funct: 6-bits that represent bits 25..20 of the instruction
            rd: 4-bits that represent bits 15..12 of the instruction
            bit4: the 4th bit of the instruction
            c: carry bit
            v: signed overflow bit
            n: negative bit
            z: zero bit
            stallf: used to detect if the pipeline is stalled
        outputs:
            pcsrcd: selects the instruction given to the fetch stage
            pcwrd: always a 1 for the single cycle processor
            regsad: selects what reg is passed into input a1 of the regfile
            regdstd: selects what reg is passed into input a2 of the regfile
            regwrsd: selects which reg is passed into input a3 of the regfile
            regwrd: selects whether to write back to the regfile
            extsd: selects the appropriate extension for an immediate
            alusrcbd: selects what value input b of the alu recieves
            alusd: selects the operation of the alu
            aluflagwrd: selects whether the c, v, n, and z flags need to be updated
            memwrd: selects whether to write to memory
            regsrcd: selects whether the alu output or data memory is feedback
            wd3sd: selects what data to write to the regfile
        """
        # Inputs
        if not isinstance(cond, iBusRead):
            raise TypeError('The cond bus must be readable')
        elif cond.size() != 4:
            raise ValueError('The cond bus must have a size of 4-bits')
        if not isinstance(op, iBusRead):
            raise TypeError('The op bus must be readable')
        elif op.size() != 2:
            raise ValueError('The op bus must have a size of 2-bits')
        if not isinstance(funct, iBusRead):
            raise TypeError('The funct bus must be readable')
        elif funct.size() != 6:
            raise ValueError('The funct bus must have a size of 6-bits')
        if not isinstance(rd, iBusRead):
            raise TypeError('The rd bus must be readable')
        elif rd.size() != 4:
            raise ValueError('The rd bus must have a size of 3-bits')
        if not isinstance(bit4, iBusRead):
            raise TypeError('The bit4 bus must be readable')
        elif bit4.size() != 1:
            raise ValueError('The bit4 bus must have a size of 1-bit')
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
        if not isinstance(stallf, iBusRead):
            raise TypeError('The stallf bus must be readable')
        elif stallf.size() != 1:
            raise ValueError('The stallf bus must have a size of 1 bit')

        self._cond = cond
        self._op = op
        self._funct = funct
        self._rd = rd
        self._bit4 = bit4
        self._c = c
        self._v = v
        self._n = n
        self._z = z
        self._stallf = stallf

        # Outputs
        if not isinstance(pcsrcd, iBusRead):
            raise TypeError('The pcsrcd bus must be writable')
        elif pcsrcd.size() != 2:
            raise ValueError('The pcsrcd bus must have a size of 2-bits')
        if not isinstance(pcwrd, iBusRead):
            raise TypeError('The pcwrd bus must be writable')
        elif pcwrd.size() != 1:
            raise ValueError('The pcwrd bus must have a size of 1-bit')
        if not isinstance(regsad, iBusRead):
            raise TypeError('The regsad bus must be writable')
        elif regsad.size() != 1:
            raise ValueError('The regsad bus must have a size of 1-bit')
        if not isinstance(regdstd, iBusRead):
            raise TypeError('The regdstd bus must be writable')
        elif regdstd.size() != 2:
            raise ValueError('The regdstd bus must have a size of 2-bits')
        if not isinstance(regwrsd, iBusRead):
            raise TypeError('The regwrsd bus must be writable')
        elif regwrsd.size() != 2:
            raise ValueError('The regwrsd bus must have a size of 2-bits')
        if not isinstance(regwrd, iBusRead):
            raise TypeError('The regwrd bus must be writable')
        elif regwrd.size() != 1:
            raise ValueError('The regwrd bus must have a size of 1-bit')
        if not isinstance(extsd, iBusRead):
            raise TypeError('The extsd bus must be writable')
        elif extsd.size() != 2:
            raise ValueError('The extsd bus must have a size of 2-bits')
        if not isinstance(alusrcbd, iBusRead):
            raise TypeError('The alusrcbd bus must be writable')
        elif alusrcbd.size() != 1:
            raise ValueError('The alusrcbd bus must have a size of 1-bit')
        if not isinstance(alusd, iBusRead):
            raise TypeError('The alusd bus must be writable')
        elif alusd.size() != 4:
            raise ValueError('The alusd bus must have a size of 4-bits')
        if not isinstance(aluflagwrd, iBusRead):
            raise TypeError('The aluflagwrd bus must be writable')
        elif aluflagwrd.size() != 1:
            raise ValueError('The aluflagwrd bus must have a size of 1-bit')
        if not isinstance(memwrd, iBusRead):
            raise TypeError('The memwrd bus must be writable')
        elif memwrd.size() != 1:
            raise ValueError('The memwrd bus must have a size of 1-bit')
        if not isinstance(regsrcd, iBusRead):
            raise TypeError('The regsrcd bus must be writable')
        elif regsrcd.size() != 1:
            raise ValueError('The regsrcd bus must have a size of 1-bit')
        if not isinstance(wd3sd, iBusRead):
            raise TypeError('The wd3sd bus must be writable')
        elif wd3sd.size() != 1:
            raise ValueError('The wd3sd bus must have a size of 1-bit')

        self._pcsrcd = pcsrcd
        self._pcwrd = pcwrd
        self._regsad = regsad
        self._regdstd = regdstd
        self._regwrsd = regwrsd
        self._regwrd = regwrd
        self._extsd = extsd
        self._alusrcbd = alusrcbd
        self._alusd = alusd
        self._aluflagwrd = aluflagwrd
        self._memwrd = memwrd
        self._regsrcd = regsrcd
        self._wd3sd = wd3sd


    @staticmethod
    def _generate_pcsrcd(op,cond,rd,z):
        """
        PCSRCD <= B"10" when a data processing instruction modifies pc
        PCSRCD <= B"01" for pc+4
        PCSRCD <= B"00" for branch instructions where condition is met
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
    def _generate_pcwrd(stallf):
        """
        PCWRD <= '1' always
        """
        return 1


    @staticmethod
    def _generate_regsad(op,bit4,funct):
        """
        REGSAD <= '1' to select Rn (data processing instructions)
        REGSAD <= '0' to select Rn (mul instruction)
        """
        if op == 0b00 and bit4 == 0b1 and (funct == 0b000000 or funct == 0b000001):
            return 0b0
        else:
            return 0b1


    @staticmethod
    def _generate_regdstd(op, bit4, funct):
        """
        REGDSTD <= B"10" to select Rd (str instruction)
        REGDSTD <= B"01" to select Rm (data processing intructions)
        REGDSTD <= B"00" to select Rm (mul instruction)
        """
        if op == 0b01 and funct == 0b011000:
            return 0b10
        elif (op == 0b00 and bit4 == 0b1 
                and (funct == 0b000000 or funct == 0b000001)):
            return 0b00
        else:
            return 0b01


    @staticmethod
    def _generate_regwrsd(op, bit4, funct):
        """
        REGWRSD <= B"10" to select LR (bl instruction)
        REGWRSD <= B"01" to select Rd (data processing instruction)
        REGWRSD <= B"00" to select Rd (mul instruction)
        """
        if op == 0b10 and ((funct & 0b010000) >> 4) == 0b1:
            return 0b10
        elif (op == 0b00 and bit4 == 0b1 
                and (funct == 0b000000 or funct == 0b000001)):
            return 0b00
        else:
            return 0b01


    @staticmethod
    def _generate_regwrd(op, funct):
        """
        REGWRD <= '1' when an instruction writes back to the regfile
        REGWRD <= '0' when an instruction does not write back to the regfile
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
    def _generate_extsd(op, funct):
        """
        EXTSD <= B"00" for 8-bit immediate (data processing immediate)
        EXTSD <= B"01" for 12-bit immediate (ldr and str instructions)
        EXTSD <= B"10" for branch instruction
        """
        if op == 0b10:
            return 0b10
        elif op == 0b01 and (funct == 0b011000 or funct == 0b011001):
            return 0b01
        else:
            return 0b00


    @staticmethod
    def _generate_alusrcbd(op, funct, bit4):
        """
        ALUSRCBD <= '1' when source B requires the output of RD2 (data
             processing instructions)
        ALUSRCBD <= '0' when source B requires an extended immediate
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
    def _generate_alusd(op, bit4, funct):
        """
        ALUSD <= "0000" for +
        ALUSD <= "0001" for -
        ALUSD <= "0010" for and
        ALUSD <= "0011" for or
        ALUSD <= "0100" for xor
        ALUSD <= "0101" for A
        ALUSD <= "0110" for B
        ALUSD <= "0111" for A*B
        ALUSD <= "1111" for 1
        """
        if (op == 0b00 and (funct == 0b000000 or funct == 0b000001) 
                and bit4 == 0b1):
            return 0b0111
        elif op == 0b00 and (funct == 0b001000 or funct == 0b101000
                             or funct == 0b001001 or funct == 0b101001):
            return 0b0000
        elif op == 0b01 and (funct == 0b011000 or funct == 0b011001):
            return 0b0000
        elif op == 0b00 and (funct == 0b000100 or funct == 0b100100
                             or funct == 0b010101 or funct == 0b110101
                             or funct == 0b000101 or funct == 0b100101):
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
    def _generate_aluflagwrd(op, funct):
        """
        ALUFLAGWRD <= '1' to set flags (cmp instructions or s bit set)
        ALUFLAGWRD <= '0' flags will not be set
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
    def _generate_memwrd(op, funct):
        """
        MEMWR <= '1' allows data to be written to data memory (str
                 instructions)
        MEMWR <= '0' cannot write to data memory
        """
        if op == 0b01 and funct == 0b011000:
            return 0b1
        else:
            return 0b0


    @staticmethod
    def _generate_regsrcd(op, funct):
        """
        REGSRC <= '1' when output of ALU is feedback
        REGSRC <= '0' when output of data mem is feedback (ldr instructions)
        """
        if op == 0b01 and funct == 0b011001:
            return 0b0
        else:
            return 0b1


    @staticmethod
    def _generate_wd3sd(op, funct):
        """
        WD3S <= '1' when a bl instruction is run else '0'
        """
        if op == 0b10 and ((funct & 0b010000) >> 4) == 0b1:
            return 0b1
        else:
            return 0b0


    def run(self, time=None):
        "Timestep handler function computes control output given instruction"

        # Read inputs
        op = self._op.read()
        funct = self._funct.read()
        bit4 = self._bit4.read()
        cond = self._cond.read()
        rd = self._rd.read()
        z = self._z.read()
        stallf = self._stallf.read()

        # Generate control outputs
        self._pcsrcd.write(self._generate_pcsrcd(op, cond, rd, z))
        self._pcwrd.write(self._generate_pcwrd(stallf))
        self._regsad.write(self._generate_regsad(op, bit4, funct))
        self._regdstd.write(self._generate_regdstd(op, bit4, funct))
        self._regwrsd.write(self._generate_regwrsd(op, bit4, funct))
        self._regwrd.write(self._generate_regwrd(op, funct))
        self._extsd.write(self._generate_extsd(op, funct))
        self._alusrcbd.write(self._generate_alusrcbd(op, funct, bit4))
        self._alusd.write(self._generate_alusd(op, bit4, funct))
        self._aluflagwrd.write(self._generate_aluflagwrd(op, funct))
        self._memwrd.write(self._generate_memwrd(op, funct))
        self._regsrcd.write(self._generate_regsrcd(op, funct))
        self._wd3sd.write(self._generate_wd3sd(op, funct))


    def inspect(self):
        "Return message noting that this controller does not contain state"
        return {'type': 'pipeline-controller', 'state': None}


    def modify(self, data=None):
        "Return message noting that this controller does not contain state"
        return {'error': 'pipeline-controller does not contain state'}


    def clear(self):
        "Return a message noting that the controller cannot be cleared"
        return {'error': 'pipeline-controller cannot be cleared'}


    def on_rising_edge(self):
        "Not implemented for pipeline"
        pass


    def on_falling_edge(self):
        "Not implemented for pipeline"
        pass


    def on_reset(self):
        "Not implemented for pipeline"
        pass

    @classmethod
    def from_dict(cls, config):
        "Implements conversion from configuration to component"
        return NotImplemented

    def to_dict(self):
        "Implements conversion from component to configuration"
        return NotImplemented
