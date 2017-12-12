from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite

class Extender(Combinational):
    def __init__(self, name, imm, imm32, exts):
        self._name = name
        if(imm.size() != 23 ):
            raise ValueError('Immediate must be 23-bits')
        self._imm = imm
        self._imm32 = imm32
        '''
        exts = 0 for data processing instructions
        exts = 1 for load and store instructions
        exts = 2 or 3 for branch instructions 
        '''
        self._exts = exts

    def inspect(self):
        # returns a dictionary message to application defining current state
        return {'name' : self._name, 'type' : 'regfile', 'size' : None, 'state': self._exts.read()}

    def run(self, time = None):
        '''
        would normally extend with 0's for when exts contains a 0 or 1
        this is not necessary in Python
        ''' 
        if self._exts.read() == 0:
            self._imm32.write(self._imm.read() >> 25)
        elif self._exts.read() == 1:
            self._imm32.write(self._imm.read() >> 21)
        else:
            # sign extend the immediate and add put 0's in the 2 least significant bits
            new_imm = self._imm.read()
            signed_bit = new_imm >> 22
            if signed_bit == 1:
                new_imm = 0xFC | new_imm 
            self._imm32.write(new_imm << 2)