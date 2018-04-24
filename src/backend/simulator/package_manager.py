#TODO clean this code up

from collections import OrderedDict

from simulator.components.abstract import AbstractPackage
from simulator.components.arm import ArmPackage
from simulator.components.core import CorePackage
from simulator.components.user import UserPackage

PackageList = {
    "abstract": AbstractPackage,
    "arm": ArmPackage,
    "core": CorePackage,
    "user": UserPackage
}


__default_packages = ["core"]


def set_default_packages(packages):
    global __default_packages
    __default_packages = packages


def construct(type, config, package=None, hooks=None):
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
