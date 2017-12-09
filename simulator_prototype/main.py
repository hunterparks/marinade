
#TODO assignment operator for buses as write ?
#TODO write being passed a bus !
#TODO join buses and sub buses

import time

from components.core.bus import Bus
from components.core.clock import Clock
from components.core.reset import Reset
from components.core.logic_input import LogicInput
from components.abstract.sequential import Latch_Type, Logic_States

from components.core.register import Register
from components.core.adder import Adder
from components.core.register_file import Register_File

if __name__ == "__main__":

    clk = Clock('clk',10,0)
    rst = Reset('rst',1)

    c1 = LogicInput('constant-1',32,1)
    c2 = LogicInput('constant-2',1,1)
    address = LogicInput('address',4,0)

    d_bus = Bus('d_bus',32,127)
    q_bus = Bus('q_bus',32,0)
    n_bus = Bus('n_bus',32,0)

    #reg = Register('reg',32,clk,rst,d_bus,q_bus,0,Latch_Type.FALLING_EDGE,Logic_States.ACTIVE_LOW,c2,Logic_States.ACTIVE_HIGH)
    add = Adder('adder',32,q_bus,c1,d_bus)
    regFile = Register_File('regfile',clk,rst,c2,d_bus,address,address,address,q_bus,n_bus)
    add.run()
    #reg.run()
    regFile.run()

    while True:
        print('-----------------------------------------------------------')
        print(clk.inspect())
        print(rst.inspect())
        print(d_bus.inspect())
        #print(reg.inspect())
        print(q_bus.inspect())

        clk.generate()
        add.run()
        #reg.run()
        regFile.run()

        time.sleep(0.01)
