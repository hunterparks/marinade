
from enum import Enum

class Architecture:

    @classmethod
    def INIFINITE_STEPS(cls):
        return 'infinite'

    def __init__(self, time_step):

        self._time_step = time_step

        self._main_clock = None
        self._main_reset = None

        self._inspect_list = []

        self._logic_list = []
        self._internal_list = []

        self._entity_list = []

    def logic_step(self):
        pass

    def logic_run(self,steps='infinite'):
        pass

    def time_step(self):
        pass

    def time_run(self,steps='infinite'):
        pass
