from abc import ABC, abstractmethod

class iBusRead(ABC):

    @abstractmethod
    def read(self):
        return NotImplemented

class iBusWrite(ABC):

    @abstractmethod
    def write(self,data):
        return NotImplemented
