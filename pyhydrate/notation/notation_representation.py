"""
Provides custom `repr` formatting for Notation classes.

This module contains the NotationRepresentation class which gives a
customized string representation for NotationObjects, NotationArrays,
and other classes that inherit from it.

The goal is to standardize the `repr` output for enhanced debugging
and inspection of nested Notation data structures.
"""
from typing import Union
import textwrap
import json


class NotationRepresentation(object):
    """
    Base class providing custom `repr` formatting.

    The __repr__ method is implemented to give a detailed summary of
    the object including its class name, value, and type information.

    Child classes will inherit this to get customized string formatting.

    Attributes:
        _repr_key (str): Name of object class.
        _idk (str): Raw string value if real value is missing.
        _debug (bool): Whether to print debug statements - from kwargs.
        _indent (int): Spacing for pretty printing - from kwargs.
    """

    # CLASS CONSTANTS
    _repr_key: str = 'PyHydrate'
    _idk: str = r'¯\_(ツ)_/¯'

    # CLASS DEFAULT PARAMETERS
    _debug: bool = False
    _indent: int = 3

    def __repr__(self) -> str:
        """
        Implement customized `__repr__` formatting and representation.

        Returns:
            str
        """

        # Try to get the raw value from the object
        try:
            _working_value: Union[str, None] = self.__dict__.get('_raw_value', None)
        except AttributeError:
            return f"{self._repr_key}(None)"

        # Try to get the raw value from withing the structure object
        # TODO: is this necessary?
        if not _working_value:
            try:
                _working_value = self.__dict__.get('_structure').__dict__.get('_raw_value', None)
            except AttributeError:
                return f"{self._repr_key}(None)"

        # Handle different working value types
        if _working_value:
            # return the quoted string
            if isinstance(_working_value, str):
                return f"{self._repr_key}('{_working_value}')"
            # return the non-string unquoted primitive
            elif (isinstance(_working_value, bool) or
                  isinstance(_working_value, float) or
                  isinstance(_working_value, int)):
                return f"{self._repr_key}({_working_value})"
            # return an indented string
            # TODO: this is incomplete, the structure should be quoted and escaped
            elif isinstance(_working_value, dict) or isinstance(_working_value, list):
                _return_value: str = textwrap.indent(json.dumps(_working_value, indent=3), 3 * ' ')
                return f"{self._repr_key}(\n{_return_value}\n)"
            # the primitive or structure is not handled, a warning should exist,
            # return and unknown representation
            else:
                return f"{self._repr_key}('{self._idk}')"
        # a known representation does not exist, return None/unknown
        else:
            return f"{self._repr_key}(None)"


if __name__ == '__main__':
    pass
