"""
    The goal of the seqential logic class is to provide an interface for all
    children to develop reset and clock based functionality
"""

from abc import ABC, abstractmethod
from components.abstract.hooks import InternalHook
from components.abstract.entity import Entity
from enum import Enum

class Latch_Type(Enum):
    """
        Defines clock sequential logic latch type
    """

    RISING_EDGE = 0
    FALLING_EDGE = 1
    BOTH_EDGE = 2

class Reset_Type(Enum):
    """
        Defines reset sequential logic on type
    """

    ACTIVE_LOW = 0
    ACTIVE_HIGH = 1

class Sequential(InternalHook, Entity):
    """
        All sequential components should be children of the Sequential class.
        The goal is to enfore the clock and reset behavior necessary for
        correct sequential logic operation. Additionally, sequential logic
        should be considered obserable by the rest of the backend
    """

    @abstractmethod
    def on_rising_edge(self):
        "On clock rising edge in entity run, this function should be called"
        return NotImplemented

    @abstractmethod
    def on_falling_edge(self):
        "On clock falling edge in entity run, this function should be called"
        return NotImplemented

    @abstractmethod
    def on_reset(self):
        "On reset event in entity run, this function should be called"
        return NotImplemented
