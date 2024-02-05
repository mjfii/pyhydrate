"""
Contains the NotationPrimitive class for accessing primitive values and types.

NotationPrimitive wraps primitive Python types like str, int, float,
bool, and None so they can be handled consistently in Notation structures.

It inherits from NotationBase to get common functionality.
"""
from typing import Union
from typing import List
from typing_extensions import Self
import warnings
from .notation_base import NotationBase


class NotationPrimitive(NotationBase):
    """
    Wrapper class for primitive values.

    Primitive types like str, int, float are wrapped in this class
    so they can be processed and output in a standard way.

    Valid types during initialization are restricted to:
        - str
        - int
        - float
        - bool
        - None

    Attributes:
        _primitives (List[type]): Valid primitive types.
    """
    # CLASS VARIABLES
    _primitives: List[type] = [str, int, float, bool, type(None)]

    def __init__(self, value: Union[str, int, float, bool, None], depth: int, **kwargs) -> None:
        """
        Initialize with the primitive value to wrap.

        Args:
            value: The primitive value.
            depth: The recursion depth that is incremented on initialization.
            **kwargs: Additional options.

        Raises:
            Warning: If value is not a primitive type.

        Returns:
            None
        """
        # set the local kwargs variable
        self._kwargs = kwargs

        # set the inherited class variables
        self._depth = depth + 1
        self._debug = self._kwargs.get('debug', False)

        #
        if type(value) in self._primitives:
            self._raw_value = value
            self._cleaned_value = value
        #
        else:
            self._raw_value = None
            self._cleaned_value = None
            _warning: str = (f"The `{self.__class__.__name__}` class does not support type '{type(value).__name__}'. "
                             f"`None` value and `NoneType` returned instead.")
            warnings.warn(_warning)

    def __getattr__(self, key: str) -> Self:
        """
        Primitive values do not have attributes. Returns a wrapper of
        NoneType/None to allow graceful failed access.

        Returns:
            NotationPrimitive(None):
        """
        self._print_debug('Get', key)
        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __getitem__(self, index) -> Self:
        """
        Primitive values do not support indexing/index slicing. Returns a
        wrapper of NoneType/None to allow graceful failed access.

        Returns:
            NotationPrimitive(None):
        """
        self._print_debug('Slice', index)
        return NotationPrimitive(None, self._depth, **self._kwargs)


if __name__ == '__main__':
    pass
