"""
Provides a custom YAML dumper for Notation structures.

This module contains the NotationDumper class which is a subclass of
yaml.Dumper. It overrides YAML indentation.
"""

import yaml


class NotationDumper(yaml.Dumper):
    """
    Custom YAML dumper class for Notation structures and primitives
    for use in `__str__` printing.

    This tells the YAML dumper not to indent list/array values
    withing the YAML string.
    """

    def increase_indent(self, *, flow: bool = False, indentless: bool = False) -> None:
        """
        Increase indentation on dump of lists.

        Args:
            flow: Boolean flag for flow style (keyword-only).
            indentless: Boolean flag for indentless style (keyword-only, unused but required for API compatibility).

        Returns:
            None
        """
        # Note: indentless parameter is unused but required for parent class API compatibility
        _ = indentless  # Explicitly acknowledge unused parameter
        return super().increase_indent(flow=flow, indentless=False)
