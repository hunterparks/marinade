"""
Note this class is envisioned to be the parent of data memory, program
memory, and virtual IO devices
"""
#TODO define the memory addressing methods (and behavior)

from components.abstract.sequential import Sequential, Latch_Type, Logic_States


class MemoryBlock(Sequential):
    pass
