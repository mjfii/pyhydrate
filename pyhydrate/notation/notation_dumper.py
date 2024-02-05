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

    def increase_indent(self, flow=False, *args, **kwargs) -> None:
        """
        Increase indentation on dump of lists.

        Returns:
            None
        """
        return super().increase_indent(flow=flow, indentless=False)


if __name__ == '__main__':
    pass
