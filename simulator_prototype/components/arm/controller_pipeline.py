from components.abstract.controller import Controller
from components.abstract.ibus import iBusRead, iBusWrite


class ControllerPipeline(Controller):
    """
    Pipeline controller component implements architecture controller
    which will take a current instruction (broken into subfields) and ALU
    status flags. Output is the control paths for the architecture which
    will be enforced until the next instruction.
    """
    def __init__(self, cond, op, funct, rd, bit4, c, v, n, z, pcsrcd, pcwrd, regsad, regdstd,
                regwrsd, regwrd, extsd, alusrcbd, alusd, aluflagwrd, memwrd, regsrcd, wd3sd):
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
        outputs:
            pcsrcd: selects the instruction given to the fetch stage
            pcwrd: always a 1 for the single cycle processor
            regsad: selects what register is passed into input a1 of the regfile
            regdstd: selects what register is passed into input a2 of the regfile
            regwrsd: selects which register is passed into input a3 of the regfile
            regwrd: selects whether to write back to the regfile
            extsd: selects the appropriate extension for an immediate
            alusrcbd: selects what value input b of the alu recieves
            alusd: selects the operation of the alu
            aluflagwrd: selects whether the c, v, n, and z flags need to be updated
            memwrd: selects whether to write to memory
            regsrcd: selects whether the alu output or data memory is feedback
            wd3sd: selects what data to write to the regfile
        """
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

        self._cond = cond
        self._op = op
        self._funct = funct
        self._rd = rd
        self._bit4 = bit4
        self._c = c
        self._v = v
        self._n = n
        self._z = z

        #Control output buses
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
    def _generate_pcwrd():
        """
        PCWR <= '1'
        Note: Might need to change
        """
        return 0b1

    @staticmethod
    def _generate_regsad(op,bit4,funct):
        """
        REGSA <= '1' to select Rn (data processing instructions)
        REGSA <= '0' to select Rn (mul instruction)
        """
        if op == 0b00 and bit4 == 0b1 and (funct == 0b000000 or funct == 0b000001):
            return 0b0
        else:
            return 0b1