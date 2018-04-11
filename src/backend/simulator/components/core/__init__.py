
from simulator.components.core.adder import Adder
from simulator.components.core.bus_join import BusJoin
from simulator.components.core.bus_subset import BusSubset
from simulator.components.core.bus import Bus
from simulator.components.core.clock import Clock
from simulator.components.core.constant import Constant
from simulator.components.core.logic_input import LogicInput
from simulator.components.core.memory import Memory
from simulator.components.core.mux import Mux
from simulator.components.core.register_file import RegisterFile
from simulator.components.core.register import Register
from simulator.components.core.reset import Reset

CorePackage = {
    "Adder": Adder,
    "BusJoin": BusJoin,
    "BusSubset": BusSubset,
    "Bus": Bus,
    "Clock": Clock,
    "Constant": Constant,
    "LogicInput": LogicInput,
    "Memory": Memory,
    "Mux": Mux,
    "RegisterFile": RegisterFile,
    "Register": Register,
    "Reset": Reset
}
