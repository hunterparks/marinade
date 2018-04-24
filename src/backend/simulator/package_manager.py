"""
Package Manager is the configuration parse module responsible for taking an
type request from the config file. The package manager is aware of several
packages as defined
    - abstract : corresponds to abstract components
    - arm : corresponds to ARM specific components
    - core  : corresponds to general component implementation
    - user : corresponds to user defined components for future extendability
"""

from collections import OrderedDict

from simulator.components.abstract import AbstractPackage
from simulator.components.arm import ArmPackage
from simulator.components.core import CorePackage
from simulator.components.user import UserPackage


# Map of available packages to import from.
PackageList = {
    "abstract": AbstractPackage,
    "arm": ArmPackage,
    "core": CorePackage,
    "user": UserPackage
}


# Module Variable defines package order to search
__default_packages = ["core"]


def set_default_packages(packages):
    """
    Sets the current list of packages to search for componet if a specific
    package is not specified

    packages is a list of strings with valid package names
    """
    global __default_packages
    __default_packages = packages


def construct(type, config, package=None, hooks=None):
    """
    Constructs a component that matches the type in the packages specified.
    type is string component name
    config is dictionary defining value for component
    package is the package to search or if None then search default packages
    hooks is the signals dictionary to link components
    """
    
    # Handle parameter options
    global __default_packages
    if package != None:
        valid_packages = package
    else:
        valid_packages = __default_packages

    if hooks == None:
        hooks = OrderedDict()

    # search through valid_packages in the order specified for type
    for p in valid_packages:
        if p in PackageList:
            if type in PackageList[p]:
                return PackageList[p][type].from_dict(config, hooks)
        else:
            raise Exception("package: {} not defined".format(p))
    raise Exception(
        "component {} does not exist in specified packages {}".format(type, valid_packages))
