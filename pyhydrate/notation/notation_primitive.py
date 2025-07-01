"""
Contains the NotationPrimitive class for accessing primitive values and types.

NotationPrimitive wraps primitive Python types like str, int, float,
bool, and None so they can be handled consistently in Notation structures.

It inherits from NotationBase to get common functionality.
"""

from typing import Any, ClassVar, List, Union

from typing_extensions import Self

# Import at top level to avoid PLC0415
from ..error_handling import handle_type_conversion_error
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

    # Memory optimization with __slots__ (inherits from NotationBase)
    __slots__ = ()

    # CLASS VARIABLES
    _primitives: ClassVar[List[type]] = [str, int, float, bool, type(None)]

    def __init__(
        self, value: Union[str, float, bool, None], depth: int, **kwargs: Any
    ) -> None:
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
        self._debug = self._kwargs.get("debug", False)

        if type(value) in self._primitives:
            self._raw_value = value
        else:
            self._raw_value = None
            handle_type_conversion_error(
                value=value,
                target_type=type(None),
                operation=f"{self.__class__.__name__} initialization",
                suggestion="Provide a primitive value (str, int, float, bool, None)",
                debug=kwargs.get("debug", False),
            )

    def __getattr__(self, key: str) -> Self:
        """
        Primitive values do not have attributes. Returns a wrapper of
        NoneType/None to allow graceful failed access.

        Returns:
            NotationPrimitive(None):
        """
        self._print_debug("Get", key)
        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __getitem__(self, index: Any) -> Self:
        """
        Primitive values do not support indexing/index slicing. Returns a
        wrapper of NoneType/None to allow graceful failed access.

        Returns:
            NotationPrimitive(None):
        """
        self._print_debug("Slice", index)
        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __int__(self) -> int:
        """
        Convert primitive value to int if possible.

        Returns:
            int: The integer representation of the value.

        Raises:
            ValueError: If string value cannot be converted to int.
            TypeError: If value type cannot be converted to int.
        """
        if isinstance(self._raw_value, (int, float)):
            return int(self._raw_value)
        if isinstance(self._raw_value, str):
            try:
                # Use Python's native int() behavior - no float conversion
                return int(self._raw_value)
            except ValueError:
                raise ValueError(f"Cannot convert '{self._raw_value}' to int") from None
        elif isinstance(self._raw_value, bool):
            return int(self._raw_value)
        elif self._raw_value is None:
            raise TypeError("Cannot convert NoneType to int")
        else:
            raise TypeError(f"Cannot convert {type(self._raw_value).__name__} to int")

    def __float__(self) -> float:
        """
        Convert primitive value to float if possible.

        Returns:
            float: The float representation of the value.

        Raises:
            ValueError: If string value cannot be converted to float.
            TypeError: If value type cannot be converted to float.
        """
        if isinstance(self._raw_value, (int, float)):
            return float(self._raw_value)
        if isinstance(self._raw_value, str):
            try:
                return float(self._raw_value)
            except ValueError:
                raise ValueError(
                    f"Cannot convert '{self._raw_value}' to float"
                ) from None
        elif isinstance(self._raw_value, bool):
            return float(self._raw_value)
        elif self._raw_value is None:
            raise TypeError("Cannot convert NoneType to float")
        else:
            raise TypeError(f"Cannot convert {type(self._raw_value).__name__} to float")

    def __bool__(self) -> bool:
        """
        Convert value to boolean following Python's truthiness rules.

        Returns:
            bool: The boolean representation of the value.
        """
        if self._raw_value is None:
            return False
        return bool(self._raw_value)
