"""Warning for implicit conversion of immutable types to mutable structures.

This module contains the ImmutableConversionWarning class which is raised when
an immutable input type (e.g., tuple, frozenset) is converted to a mutable list
during PyHydrate initialization.
"""

from .pyhydrate_warning import PyHydrateWarning


class ImmutableConversionWarning(PyHydrateWarning):
    """Warning issued when immutable data is converted to a mutable structure.

    This warning is raised when:
    - A tuple is converted to a list
    - A frozenset is converted to a list
    """
