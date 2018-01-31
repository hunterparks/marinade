"""
ARM specific register file of length 16 with bit-width of 32.
"""

from components.core.register_file import RegisterFile as _RegisterFile
from components.core.register_file import Latch_Type, Logic_States


class RegisterFile(_RegisterFile):
    """
    ARM specific register file of length 16 with bit-width of 32.
    Component is sequential and thus requires a clock and reset to operate
    Note that this component is a wrapper on core component
    """

    def __init__(self, clock, reset, write_enable, write_data, ra1, ra2, ra3, wa1,
                 rd1, rd2, rd3, edge_type=Latch_Type.RISING_EDGE,
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

                edge_type : Register data latch type (for all)
                reset_type : Register reset signal active (for all)
                enable_type : Register file write enable active state
        """
        _RegisterFile.__init__(self, 16, 32, clock, reset, wa1, write_data, [ra1, ra2, ra3],
                               [rd1, rd2, rd3], write_enable, 0, edge_type, reset_type,
                               enable_type)
