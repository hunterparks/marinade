from abc import ABC, abstractmethod
from components.abstract.hooks import InternalHook
from components.abstract.entity import Entity
from enum import Enum

class Edge_Type(Enum):
    LATCH_RISING_EDGE = 0
    LATCH_FALLING_EDGE = 1
    LATCH_BOTH_EDGE = 2

class Reset_Type(Enum):
    RESET_ACTIVE_LOW = 0
    RESET_ACTIVE_HIGH = 1

class Sequential(InternalHook, Entity):

    @abstractmethod
    def on_rising_edge(self):
        return NotImplemented

    @abstractmethod
    def on_falling_edge(self):
        return NotImplemented

    @abstractmethod
    def on_reset(self):
        return NotImplemented
