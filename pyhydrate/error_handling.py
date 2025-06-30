"""Error handling utilities for PyHydrate.

This module provides standardized error handling functions and logging utilities
to ensure consistent behavior across the PyHydrate library.
"""

import logging
import warnings
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from .notation.notation_primitive import NotationPrimitive

from .exceptions import (
    AccessPatternWarning,
    APIUsageWarning,
    TypeConversionWarning,
    format_warning_message,
)


def setup_logger(name: str, *, debug: bool = False) -> logging.Logger:
    """Set up a logger for PyHydrate with appropriate level and formatting.

    Args:
        name: Logger name (typically __name__)
        debug: Whether to enable debug-level logging

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(name)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG if debug else logging.WARNING)
    return logger


def handle_type_conversion_error(
    value: Any,
    target_type: type,
    operation: str = "Type conversion",
    suggestion: Union[str, None] = None,
    *,
    debug: bool = False,
) -> None:
    """Handle type conversion errors with standardized warning.

    Args:
        value: The value that failed to convert
        target_type: The target type for conversion
        operation: Description of the operation (default: "Type conversion")
        suggestion: Optional suggestion for fixing the issue
        debug: Whether to log debug information
    """
    message = format_warning_message(
        operation=operation,
        actual_type=type(value),
        expected_type=target_type,
        value=value,
        suggestion=suggestion,
    )

    warnings.warn(message, TypeConversionWarning, stacklevel=3)

    if debug:
        logger = setup_logger(__name__, debug=True)
        logger.debug(f"Conversion failed: {value!r} -> {target_type.__name__}")


def handle_access_pattern_error(
    accessor: str,
    target_type: type,
    accessed_type: type,
    suggestion: Union[str, None] = None,
    *,
    debug: bool = False,
) -> "NotationPrimitive":
    """Handle invalid access patterns with standardized warning.

    Args:
        accessor: The access pattern attempted (e.g., attribute name, index)
        target_type: The expected type for this access pattern
        accessed_type: The actual type being accessed
        suggestion: Optional suggestion for fixing the issue
        debug: Whether to log debug information

    Returns:
        NotationPrimitive(None) for graceful failure
    """
    # Lazy import to avoid circular dependency
    from .notation.notation_primitive import NotationPrimitive

    message = format_warning_message(
        operation=f"Access pattern '{accessor}'",
        actual_type=accessed_type,
        expected_type=target_type,
        suggestion=suggestion,
    )

    warnings.warn(message, AccessPatternWarning, stacklevel=3)

    if debug:
        logger = setup_logger(__name__, debug=True)
        logger.debug(f"Invalid access: {accessor} on {accessed_type.__name__}")

    return NotationPrimitive(None, depth=0)


def handle_api_usage_error(
    operation: str,
    provided_value: Any,
    valid_options: Union[list, None] = None,
    suggestion: Union[str, None] = None,
    *,
    debug: bool = False,
) -> None:
    """Handle API usage errors with standardized warning.

    Args:
        operation: The operation that was attempted
        provided_value: The invalid value provided
        valid_options: List of valid options (if applicable)
        suggestion: Optional suggestion for fixing the issue
        debug: Whether to log debug information
    """
    if valid_options:
        suggestion = suggestion or f"Valid options are: {', '.join(valid_options)}"

    message = format_warning_message(
        operation=operation,
        actual_type=type(provided_value),
        value=provided_value,
        suggestion=suggestion,
    )

    warnings.warn(message, APIUsageWarning, stacklevel=3)

    if debug:
        logger = setup_logger(__name__, debug=True)
        logger.debug(f"Invalid API usage: {operation} with {provided_value!r}")


def log_debug_access(
    logger_name: str,
    access_type: str,
    target: str,
    depth: int,
    value_type: type,
    *,
    debug: bool = False,
) -> None:
    """Log debug information for data access patterns.

    Args:
        logger_name: Name for the logger
        access_type: Type of access (e.g., "attribute", "index", "call")
        target: The target being accessed
        depth: Current recursion depth
        value_type: Type of the value being accessed
        debug: Whether debug logging is enabled
    """
    if not debug:
        return

    logger = setup_logger(logger_name, debug=True)
    indent = "  " * depth
    logger.debug(
        f"{indent}{access_type.capitalize()} access: {target} -> {value_type.__name__}"
    )


def create_none_primitive(**kwargs: Any) -> "NotationPrimitive":
    """Create a NotationPrimitive(None) with consistent parameters.

    This utility ensures all None primitives are created with the same
    pattern across the codebase.

    Args:
        **kwargs: Keyword arguments to pass to NotationPrimitive

    Returns:
        NotationPrimitive instance wrapping None
    """
    # Lazy import to avoid circular dependency
    from .notation.notation_primitive import NotationPrimitive

    return NotationPrimitive(None, **kwargs)
