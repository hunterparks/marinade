"""
Limits module captures the hard limits for the system. Components and
architectures are advised to follow the limits listed as they are implicitly
assumed during simulation operation.

Eventually these values could be made configurable by an architecture.
"""

MAX_FREQUENCY = 1000  # Hz
MIN_FREQUENCY = 0  # Hz


MAX_MEMORY_BLOCK = 1024  # words
MIN_MEMORY_BLOCK = 1  # words

MAX_BYTES_IN_WORD = 4  # 32-bit word maximum

MIN_ADDRESS = 0
MAX_ADDRESS = 4096
