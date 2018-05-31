"""
Tests architecture's configuration parser package manager
"""

from collections import OrderedDict
import unittest
import sys

sys.path.insert(0, '../../../')
import simulator.package_manager as package_manager
from simulator.components.core.bus import Bus


class PackageManager_t(unittest.TestCase):
    """
    Tests package manager for valid search of arbitrary components in arbitrary
    packages
    """

    def test_construct_default(self):
        """Prove construction works with default packages"""
        package_manager.set_default_packages(["core"])  # Default of module

        components = OrderedDict()
        obj_bus = package_manager.construct(
            "Bus", {
                "width": 8,
                "value": 0
            }, None, components
        )
        components.update({"bus1": obj_bus})

    def test_construct_package_param(self):
        """Prove construction works with specified package"""
        package_manager.set_default_packages(["core"])  # Default of module

        components = OrderedDict({
            "imm": Bus(24),
            "exts": Bus(2),
            "imm32": Bus(32)
        })
        obj_extender = package_manager.construct(
            "Extender", {
                "imm": "imm",
                "exts": "exts",
                "imm32": "imm32"
            }, ["arm"], components
        )
        components.update({"extender": obj_extender})

    def test_set_default_packages(self):
        """Prove package selection mechanism works"""
        package_manager.set_default_packages(["core"])  # Default of module

        components = OrderedDict({
            "imm": Bus(24),
            "exts": Bus(2),
            "imm32": Bus(32)
        })

        # Expect failure
        try:
            obj_extender = package_manager.construct(
                "Extender", {
                    "imm": "imm",
                    "exts": "exts",
                    "imm32": "imm32"
                }, None, components
            )
            components.update({"extender": obj_extender})
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)

        # Expect success
        package_manager.set_default_packages(["arm"])  # Change default packages
        obj_extender = package_manager.construct(
            "Extender", {
                "imm": "imm",
                "exts": "exts",
                "imm32": "imm32"
            }, None, components
        )
        components.update({"extender": obj_extender})


if __name__ == "__main__":
    unittest.main()
