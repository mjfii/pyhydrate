"""Utility function for formatting standardized warning messages.

This module contains the format_warning_message function which provides
consistent warning message formatting across all PyHydrate operations.
"""

from typing import Any, Union


def format_warning_message(
    operation: str,
    actual_type: type,
    expected_type: Union[type, str, None] = None,
    value: Any = None,
    suggestion: Union[str, None] = None,
) -> str:
    """Format a standardized warning message for PyHydrate operations.

    Args:
        operation: The operation that failed (e.g., "Type conversion", "Access")
        actual_type: The actual type encountered
        expected_type: The expected type (optional)
        value: The value that caused the issue (optional)
        suggestion: Suggested fix for the user (optional)

    Returns:
        Formatted warning message string
    """
    message_parts = [f"{operation} failed"]

    if expected_type:
        expected_str = (
            expected_type if isinstance(expected_type, str) else expected_type.__name__
        )
        message_parts.append(f"expected {expected_str}, got {actual_type.__name__}")
    else:
        message_parts.append(f"with {actual_type.__name__}")

    if value is not None:
        message_parts.append(f"(value: {value!r})")

    base_message = " ".join(message_parts)

    if suggestion:
        return f"{base_message}. {suggestion}"

    return base_message
