"""Warning for invalid access attempts in PyHydrate.

This module contains the AccessPatternWarning class which is raised when
invalid access attempts are made on PyHydrate data structures.
"""

from .pyhydrate_warning import PyHydrateWarning


class AccessPatternWarning(PyHydrateWarning):
    """Warning issued for invalid access attempts on data structures.

    This warning is raised when:
    - Invalid attribute access on primitive values
    - Array index access on non-array objects
    - Out-of-bounds array access attempts
    """
