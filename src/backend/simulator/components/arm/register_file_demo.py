"""
ARM specific register file of length 16 with bit-width of 32.
"""

from simulator.components.core.register_file import RegisterFile as _RegisterFile
from simulator.components.core.register_file import Latch_Type, Logic_States


class RegisterFile(_RegisterFile):
    """
    ARM specific register file of length 16 with bit-width of 32.
    Component is sequential and thus requires a clock and reset to operate
    Note that this component is a wrapper on core component
    """

    DEFAULT_LATCH_TYPE = Latch_Type.RISING_EDGE
    DEFAULT_RESET_TYPE = Logic_States.ACTIVE_HIGH
    DEFAULT_ENABLE_TYPE = Logic_States.ACTIVE_HIGH

    def __init__(self, clock, reset, write_enable, write_data, a1, a2, a3, rd1, rd2,
                 edge_type=DEFAULT_LATCH_TYPE, reset_type=DEFAULT_RESET_TYPE,
                 enable_type=DEFAULT_ENABLE_TYPE):
        """
            Constructor will check for valid parameters, exception thrown on invalid

            Parameters
                clock : system clock resource
                reset : system reset resource
                write_enable : global write enable for register file
                write_data : word data to write to register at address when enabled
                a1 : read one address
                a2 : read two address
                a3 : write address
                rd1 : register read contents one
                rd2 : register read contents two

                edge_type : Register data latch type (for all)
                reset_type : Register reset signal active (for all)
                enable_type : Register file write enable active state
        """
        _RegisterFile.__init__(self, 16, 32, clock, reset, a3, write_data, [a1, a2],
                               [rd1, rd2], write_enable, 0, edge_type, reset_type,
                               enable_type)

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
                            hooks[config["a1"]],hooks[config["a2"]],hooks[config["a3"]],
                            hooks[config["rd1"]],hooks[config["rd2"]],edge_type,
                            reset_type,enable_type)
