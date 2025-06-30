"""
Shared type definitions for the PyHydrate library.

This module centralizes type hints and forward references to avoid
circular import dependencies between notation classes.
"""

from typing import Union

# Import at runtime since they're used in Union types
from .notation.notation_primitive import NotationPrimitive
from .notation.notation_structures import NotationArray, NotationObject

# Union type for all notation types
NotationTypes = Union[NotationPrimitive, NotationObject, NotationArray]

# Union type for structure types only
StructureTypes = Union[NotationObject, NotationArray]

# Union type for values that can be wrapped
WrappableTypes = Union[dict, list, str, int, float, bool, None]
