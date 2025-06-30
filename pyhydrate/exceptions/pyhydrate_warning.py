"""Base warning class for PyHydrate operations.

This module contains the PyHydrateWarning class which serves as the parent class
for all PyHydrate-specific warnings, allowing users to catch all library warnings
with a single except clause.
"""


class PyHydrateWarning(UserWarning):
    """Base warning class for all PyHydrate operations.

    This serves as the parent class for all PyHydrate-specific warnings,
    allowing users to catch all library warnings with a single except clause.
    """
