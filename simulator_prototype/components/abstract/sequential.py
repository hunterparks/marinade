from abc import ABC, abstractmethod
from components.abstract.hooks import InternalHook
from components.abstract.entity import Entity

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
