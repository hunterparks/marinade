"""
Pass test cases to importer for test suite
"""

import sys
sys.path.insert(0, '../../../')

from simulator.tests.simulation.single_cycle_processor_demo_t import SingleCycleProcessor_t as SCP_demo_t
from simulator.tests.simulation.single_cycle_processor_full_t import SingleCycleProcessor_t as SCP_full_t
from simulator.tests.simulation.pipeline_processor_t import PipelineProcessor_t as PP_demo_t
