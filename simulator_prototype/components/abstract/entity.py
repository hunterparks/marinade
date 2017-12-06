from abc import ABC, abstractmethod

class Entity(ABC):

    @abstractmethod
    def run(self):
        return NotImplemented
