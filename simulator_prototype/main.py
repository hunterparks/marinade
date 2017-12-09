
import time

from components.core.bus import Bus
from components.core.clock import Clock
from components.core.reset import Reset
from components.core.logic_input import LogicInput
from components.abstract.sequential import Latch_Type, Logic_States

from components.core.register import Register
from components.core.adder import Adder
from components.arm.register_file import Register_File
from components.core.mux import Mux
from components.arm.alu import Alu
from components.core.bus_subset import BusSubset
from components.core.bus_join import BusJoin

if __name__ == "__main__":

    clk = Clock('clk',10,0)
    rst = Reset('rst',1)

    c1 = LogicInput('constant-1',32,1)
    c2 = LogicInput('constant-2',1,1)
    address = LogicInput('address',4,0)

    d_bus = Bus('d_bus',32,127)
    q_bus = Bus('q_bus',32,0)
    m_bus = Bus('n_bus',32,0)
    f_bus = Bus('f_bus',32,0)
    r_bus = Bus('r_bus',32,0)
    c_bus = Bus('c_bus',1,0)
    v_bus = Bus('v_bus',1,0)
    n_bus = Bus('n_bus',1,0)
    z_bus = Bus('z_bus',1,0)

    ss0_bus = Bus('ss0',8,0)
    ss1_bus = Bus('ss1',8,0)
    ss2_bus = Bus('ss2',8,0)
    ss3_bus = Bus('ss3',8,0)

    bj0 = Bus('bj0',32,0)


    #reg = Register('reg',32,clk,rst,d_bus,q_bus)
    add = Adder('adder',32,q_bus,c1,d_bus)
    regFile = Register_File('regfile',clk,rst,c2,d_bus,address,address,address,q_bus,m_bus)
    m = Mux('mux',32,[q_bus,m_bus],c2,f_bus)
    alu = Alu('alu',f_bus,q_bus,Bus('temp',1,0),r_bus,c_bus,v_bus,n_bus,z_bus)
    subset = BusSubset('subset',q_bus,[ss0_bus,ss1_bus,ss2_bus,ss3_bus],[(0,8),(8,16),(16,24),(24,32)])
    join = BusJoin('join',[ss3_bus,ss2_bus,ss1_bus,ss0_bus],bj0)

    add.run()
    #reg.run()
    regFile.run()
    m.run()
    alu.run()
    subset.run()
    join.run()

    while True:
        print('-----------------------------------------------------------')
        print(clk.inspect())
        print(rst.inspect())
        print(d_bus.inspect())
        #print(reg.inspect())
        print(q_bus.inspect())
        print(f_bus.inspect())
        print(r_bus.inspect())
        print(c_bus.inspect())
        print(v_bus.inspect())
        print(n_bus.inspect())
        print(z_bus.inspect())

        print(ss0_bus.inspect())
        print(ss1_bus.inspect())
        print(ss2_bus.inspect())
        print(ss3_bus.inspect())
        print(bj0.inspect())


        clk.generate()
        add.run()
        #reg.run()
        regFile.run()
        m.run()
        alu.run()
        subset.run()
        join.run()

        time.sleep(0.01)
