"""PyHydrate exception and warning classes.

This package contains all custom exception and warning classes used throughout
PyHydrate for consistent error handling and user feedback.

The package follows the repository standard of one class per module for better
organization and maintainability.
"""

from .access_pattern_warning import AccessPatternWarning
from .api_usage_warning import APIUsageWarning
from .format_warning_message import format_warning_message
from .pyhydrate_warning import PyHydrateWarning
from .type_conversion_warning import TypeConversionWarning

__all__ = [
    "APIUsageWarning",
    "AccessPatternWarning",
    "PyHydrateWarning",
    "TypeConversionWarning",
    "format_warning_message",
]
