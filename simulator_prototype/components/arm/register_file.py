"""
    ARM specific register file of length 16 with bit-width of 32.
"""

from components.core.register_file import RegisterFile as _RegisterFile
from components.core.register_file import Latch_Type, Logic_States

class RegisterFile(_RegisterFile):
    """
        ARM specific register file of length 16 with bit-width of 32.

        Parameters
            clock :
            reset :
            write_enable :
            write_data :
            a1 :
            a2 :
            a3 :
            rd1 :
            rd2 :

            edge_type : Register data latch type (for all)
            reset_type : Register reset signal active (for all)
            enable_type : Register file write enable active state
    """

    def __init__(self,clock,reset,write_enable, write_data, a1, a2, a3, rd1, rd2,
                 edge_type = Latch_Type.FALLING_EDGE, reset_type = Logic_States.ACTIVE_LOW,
                 enable_type = Logic_States.ACTIVE_HIGH):
        """

        """
        _RegisterFile.__init__(self,16,32,clock,reset,a3,write_data,[a1,a2],[rd1,rd2],write_enable,0,edge_type,reset_type,enable_type)
