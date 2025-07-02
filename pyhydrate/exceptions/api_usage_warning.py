"""Warning for incorrect API usage patterns in PyHydrate.

This module contains the APIUsageWarning class which is raised when
incorrect API usage patterns are detected in PyHydrate operations.
"""

from .pyhydrate_warning import PyHydrateWarning


class APIUsageWarning(PyHydrateWarning):
    """Warning issued for incorrect API usage patterns.

    This warning is raised when:
    - Invalid call types passed to __call__ method
    - Deprecated API usage patterns
    - Misuse of library features
    """
