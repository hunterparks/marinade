"""
Single-cycle controller as derived by Larry Skuse's VHDL work.
"""

from components.abstract.controller import Controller
from components.abstract.ibus import iBusRead, iBusWrite


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

    def run(self, time=None):
        "Runs a timestep of controller, assert control signals on each"
        pass

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
