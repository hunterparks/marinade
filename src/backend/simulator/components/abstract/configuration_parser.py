"""
Abstract Class defining the methods necessary to move between JSON configuration
file and simulation architecture.

All objects in architecture must implement this functionality in order to use
configuration files. These can be regarded as special constructors.
"""

from abc import ABC, abstractmethod


class ConfigurationParser(ABC):
    """
    Converts between a configuration representation and the component
    representation for each component implementing this.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        return NotImplemented
