"""
ARM specific register file of length 16 with bit-width of 32.
"""

from simulator.components.abstract.ibus import iBusRead
from simulator.components.core.register_file import RegisterFile as _RegisterFile
from simulator.components.core.register_file import Latch_Type, Logic_States


class RegisterFile(_RegisterFile):
    """
    ARM specific register file of length 16 with bit-width of 32.
    Component is sequential and thus requires a clock and reset to operate
    Note that this component is a wrapper on core component
    """

    def __init__(self, clock, reset, write_enable, write_data, ra1, ra2, ra3, wa1,
                 rd1, rd2, rd3, pc, edge_type=Latch_Type.RISING_EDGE,
                 reset_type=Logic_States.ACTIVE_HIGH,
                 enable_type=Logic_States.ACTIVE_HIGH):
        """
            Constructor will check for valid parameters, exception thrown on invalid

            Parameters
                clock : system clock resource
                reset : system reset resource
                write_enable : global write enable for register file
                write_data : word data to write to register at address when enabled
                ra1 : read one address
                ra2 : read two address
                ra3 : read three address
                wa1 : write one address
                rd1 : register read contents one
                rd2 : register read contents two
                rd3 : register read contents three
                pc : link to PC from architecture to regfile. (Read only)

                edge_type : Register data latch type (for all)
                reset_type : Register reset signal active (for all)
                enable_type : Register file write enable active state
        """
        # link PC for register read
        if not isinstance(pc, iBusRead):
            raise TypeError('PC bus must be readable')
        elif pc.size() != 32:
            raise ValueError('PC bus must be 32 bits')
        self._pc = pc

        #note read addresses for run
        if not isinstance(ra1, iBusRead):
            raise TypeError('RA1 bus must be readable')
        elif ra1.size() != 4:
            raise ValueError('RA1 bus must be 4 bits')
        if not isinstance(ra2, iBusRead):
            raise TypeError('RA2 bus must be readable')
        elif ra2.size() != 4:
            raise ValueError('RA2 bus must be 4 bits')
        if not isinstance(ra3, iBusRead):
            raise TypeError('RA3 bus must be readable')
        elif ra3.size() != 4:
            raise ValueError('RA3 bus must be 4 bits')
        self._ra1 = ra1
        self._ra2 = ra2
        self._ra3 = ra3

        #note read buses for run
        if not isinstance(rd1, iBusRead):
            raise TypeError('RD1 bus must be readable')
        elif rd1.size() != 32:
            raise ValueError('RD1 bus must be 32 bits')
        if not isinstance(rd2, iBusRead):
            raise TypeError('RD2 bus must be readable')
        elif rd2.size() != 32:
            raise ValueError('RD2 bus must be 32 bits')
        if not isinstance(rd3, iBusRead):
            raise TypeError('RD3 bus must be readable')
        elif rd3.size() != 32:
            raise ValueError('RD3 bus must be 32 bits')
        self._rd1 = rd1
        self._rd2 = rd2
        self._rd3 = rd3

        # create general register file
        _RegisterFile.__init__(self, 15, 32, clock, reset, wa1, write_data, [ra1, ra2, ra3],
                               [rd1, rd2, rd3], write_enable, 0, edge_type, reset_type,
                               enable_type)

    def run(self, time=None):
        """
        Check if any of the read addresses are PC else route to general
        general file.
        """

        _RegisterFile.run(self)

        if self._ra1.read() == 15:
            self._rd1.write(self._pc.read())
        if self._ra2.read() == 15:
            self._rd2.write(self._pc.read())
        if self._ra3.read() == 15:
            self._rd3.write(self._pc.read())

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"

        if "edge_type" in config:
            edge_type = Latch_Type.fromString(config["edge_type"])
        else:
            edge_type = RegisterFile.DEFAULT_LATCH_TYPE

        if "reset_type" in config:
            reset_type = Logic_States.fromString(config["reset_type"])
        else:
            reset_type = RegisterFile.DEFAULT_RESET_TYPE

        if "enable_type" in config:
            enable_type = Logic_States.fromString(config["enable_type"])
        else:
            enable_type = RegisterFile.DEFAULT_ENABLE_TYPE

        return RegisterFile(hooks[config["clock"]],hooks[config["reset"]],
                            hooks[config["write_enable"]],hooks[config["write_data"]],
                            hooks[config["ra1"]],hooks[config["ra2"]],hooks[config["ra3"]],
                            hooks[config["wa1"]],hooks[config["rd1"]],hooks[config["rd2"]],
                            hooks[config["rd3"]],hooks[config["pc"]],edge_type,reset_type,
                            enable_type)
