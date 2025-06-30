"""Warning for type conversion issues in PyHydrate.

This module contains the TypeConversionWarning class which is raised when
type conversion operations fail or encounter issues during PyHydrate operations.
"""

from .pyhydrate_warning import PyHydrateWarning


class TypeConversionWarning(PyHydrateWarning):
    """Warning issued when type conversion operations fail or encounter issues.

    This warning is raised when:
    - Invalid type conversion attempts in magic methods
    - Type mismatches during object initialization
    - Data type validation failures
    """
