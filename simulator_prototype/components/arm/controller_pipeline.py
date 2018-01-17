from components.abstract.controller import Controller
from components.abstract.ibus import iBusRead, iBusWrite


class ControllerPipeline(Controller):
    """
    Pipeline controller component implements architecture controller
    which will take a current instruction (broken into subfields) and ALU
    status flags. Output is the control paths for the architecture which
    will be enforced until the next instruction.
    """