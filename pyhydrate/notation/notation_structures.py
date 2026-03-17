"""
Provides the core NotationObject and NotationArray classes.

This module defines the two key classes used to represent nested
dict and list structures in the `notation` library.

NotationObject wraps a dict structure containing additional
NotationObjects, NotationArrays, and NotationPrimitives.

NotationArray wraps a list structure with the same nested elements.
"""

from typing import TYPE_CHECKING, Any, Union

from typing_extensions import Self

from .notation_base import NotationBase

if TYPE_CHECKING:
    from .notation_primitive import NotationPrimitive


class NotationObject(NotationBase):
    """
    Class for representing nested dict/object structures.

    NotationObject wraps a dict to provide access to child elements
    using attribute and item access. Children can be other objects,
    arrays, or primitives.

    Uses lazy loading to minimize memory usage.
    """

    # Memory optimization with __slots__
    __slots__ = ("_hydrated_cache", "_key_mappings")

    # Internal attributes that should bypass __setattr__ data path
    _INTERNAL_ATTRS: frozenset = frozenset(
        {
            "_raw_value",
            "_hydrated_cache",
            "_key_mappings",
            "_kwargs",
            "_depth",
            "_debug",
            "_call",
            "_parent",
            "_parent_key",
        }
    )

    def __init__(self, value: dict, depth: int, **kwargs: Any) -> None:
        """
        Initialize with the raw dict and recursion depth.
        Uses lazy loading to minimize memory usage.

        Parameters:
            value (dict): The raw dictionary to wrap
            depth (int): Current recursion depth
            kwargs (dict): Additional configuration options
        """
        # Set instance variables
        self._kwargs = kwargs
        self._depth = depth + 1
        self._debug = self._kwargs.get("debug", False)
        self._parent = None
        self._parent_key = None

        if isinstance(value, dict):
            self._raw_value = value
            self._hydrated_cache = {}  # Lazy cache for hydrated children
            self._key_mappings = {}  # Cache for key transformations

            # Pre-compute key mappings but don't hydrate children
            for key in value:
                cleaned_key = self._cast_key(key)
                self._key_mappings[cleaned_key] = key
        else:
            self._raw_value = None
            self._hydrated_cache = {}
            self._key_mappings = {}
            from ..error_handling import handle_type_conversion_error

            handle_type_conversion_error(
                value=value,
                target_type=dict,
                operation=f"{self.__class__.__name__} initialization",
                suggestion="Provide a dictionary or dict-like object",
                debug=kwargs.get("debug", False),
            )

    def __getattr__(
        self, key: str
    ) -> Union[Self, "NotationArray", "NotationPrimitive"]:
        """
        Get a child element by attribute name using lazy loading.

        For missing keys, returns a NotationProxy that supports deep
        auto-creation of intermediate dicts on assignment.

        Parameters:
            key (str): The attribute name to access

        Returns:
            Union[NotationObject, NotationArray, NotationPrimitive, NotationProxy]
        """
        self._print_debug("Get", key)

        # Check if already cached
        if key in self._hydrated_cache:
            return self._hydrated_cache[key]

        # Look up the original key
        raw_key = self._key_mappings.get(key)
        if raw_key and raw_key in self._raw_value:
            # Lazy create the child object
            raw_value = self._raw_value[raw_key]
            self._hydrated_cache[key] = self._create_child(
                raw_value, parent=self, parent_key=raw_key
            )
            return self._hydrated_cache[key]

        # Key not found, return a proxy for potential write-through
        from .notation_proxy import _DEFAULT_MAX_PROXY_DEPTH, NotationProxy

        max_depth = self._kwargs.get("max_proxy_depth", _DEFAULT_MAX_PROXY_DEPTH)
        return NotationProxy(parent=self, parent_key=key, max_depth=max_depth)

    def _get_cleaned_value(self) -> Union[dict, None]:
        """
        Compute cleaned value on demand for memory efficiency.

        Returns:
            Union[dict, None]: Dictionary with cleaned keys and values
        """
        if self._raw_value is None:
            return None

        cleaned = {}
        for raw_key, raw_value in self._raw_value.items():
            cleaned_key = self._cast_key(raw_key)
            if isinstance(raw_value, dict):
                # Recursively clean nested dictionaries
                cleaned[cleaned_key] = self._get_cleaned_child_value(raw_value)
            elif isinstance(raw_value, list):
                # Recursively clean nested lists
                cleaned[cleaned_key] = [
                    self._get_cleaned_child_value(item) for item in raw_value
                ]
            else:
                # Primitive values stay as-is
                cleaned[cleaned_key] = raw_value
        return cleaned

    def _get_cleaned_child_value(
        self, value: Union[dict, list, Any]
    ) -> Union[dict, list, Any]:
        """
        Helper method to recursively clean child values without full hydration.

        Parameters:
            value: The value to clean

        Returns:
            The cleaned value
        """
        if isinstance(value, dict):
            return {
                self._cast_key(k): self._get_cleaned_child_value(v)
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [self._get_cleaned_child_value(item) for item in value]
        return value

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Set a value via dot notation or initialize internal attributes.

        Internal attributes (those in _INTERNAL_ATTRS or starting with '__')
        are set normally. All other keys are treated as data writes to the
        underlying dict.

        Parameters:
            key (str): The attribute/key name
            value: The value to set
        """
        if key in NotationObject._INTERNAL_ATTRS or key.startswith("__"):
            object.__setattr__(self, key, value)
            return
        self._set_value(key, value)

    def _set_value(self, key: str, value: Any) -> None:
        """
        Set a data value in the underlying dict.

        If the key maps to an existing original key (via key normalization),
        the original key is updated. Otherwise, the key is stored as provided.

        Parameters:
            key (str): The cleaned/user-facing key name
            value: The value to set (will be unwrapped if a Notation object)
        """
        raw_value = self._unwrap(value)
        # Preserve original key format if it exists
        original_key = self._key_mappings.get(key, key)
        self._raw_value[original_key] = raw_value
        # Update key mappings
        cleaned = self._cast_key(original_key)
        self._key_mappings[cleaned] = original_key
        # Invalidate cache for this key
        for k in (key, cleaned):
            self._hydrated_cache.pop(k, None)

    def __delattr__(self, key: str) -> None:
        """
        Delete a key from the underlying dict.

        Parameters:
            key (str): The attribute/key name to delete

        Raises:
            AttributeError: If the key is not found
        """
        original_key = self._key_mappings.get(key)
        if original_key and original_key in self._raw_value:
            del self._raw_value[original_key]
            del self._key_mappings[key]
            self._hydrated_cache.pop(key, None)
        else:
            raise AttributeError(f"'{key}' not found")

    def __getitem__(self, index: int) -> "NotationPrimitive":
        """
        Not implemented for objects.

        Parameters:
            index (int):

        Returns:
            NotationPrimitive(None)
        """
        self._print_debug("Slice", index)
        from .notation_primitive import NotationPrimitive

        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __int__(self) -> int:
        """
        Convert object to int (should fail for dict structures).

        Raises:
            TypeError: Always raises as dict cannot be converted to int
        """
        raise TypeError("Cannot convert dict to int")

    def __float__(self) -> float:
        """
        Convert object to float (should fail for dict structures).

        Raises:
            TypeError: Always raises as dict cannot be converted to float
        """
        raise TypeError("Cannot convert dict to float")

    def __bool__(self) -> bool:
        """
        Convert object to bool following Python's truthiness rules.
        Empty dicts are False, non-empty dicts are True.

        Returns:
            bool: False if dict is empty, True otherwise
        """
        if self._raw_value is None:
            return False
        return bool(self._raw_value)


class NotationArray(NotationBase):
    """
    Class for representing nested list structures.

    NotationArray wraps a list with nested object/array/primitive
    elements similarly to NotationObject.

    Uses lazy loading to minimize memory usage.
    """

    # Memory optimization with __slots__
    __slots__ = ("_hydrated_cache",)

    def __init__(self, value: list, depth: int, **kwargs: Any) -> None:
        """
        Initialize with the raw list value.
        Uses lazy loading to minimize memory usage.

        Parameters:
            value (list): The raw list to wrap
            depth (int): Current recursion depth
            kwargs (dict): Additional configuration options
        """
        # Set instance variables
        self._kwargs = kwargs
        self._depth = depth + 1
        self._debug = self._kwargs.get("debug", False)
        self._parent = None
        self._parent_key = None

        if isinstance(value, list):
            self._raw_value = value
            self._hydrated_cache = {}  # Lazy cache for hydrated elements
        else:
            self._raw_value = None
            self._hydrated_cache = {}
            from ..error_handling import handle_type_conversion_error

            handle_type_conversion_error(
                value=value,
                target_type=list,
                operation=f"{self.__class__.__name__} initialization",
                suggestion="Provide a list or list-like object",
                debug=kwargs.get("debug", False),
            )

    def _get_cleaned_value(self) -> Union[list, None]:
        """
        Compute cleaned value on demand for memory efficiency.

        Returns:
            Union[list, None]: List with cleaned values
        """
        if self._raw_value is None:
            return None

        # For arrays, the cleaned value is the same as raw value
        # since we don't transform array indices
        return self._raw_value

    def __getattr__(self, key: str) -> "NotationPrimitive":
        """
        Not implemented for arrays.

        Parameters:
            key (str): The attribute name

        Returns:
            NotationPrimitive: Always returns None primitive
        """
        self._print_debug("Get", key)
        from .notation_primitive import NotationPrimitive

        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __getitem__(
        self, index: int
    ) -> Union["NotationObject", Self, "NotationPrimitive"]:
        """
        Get child element by index using lazy loading.

        Parameters:
            index (int): The index to access

        Returns:
            Union[NotationObject, NotationArray, NotationPrimitive]
        """
        self._print_debug("Slice", index)

        try:
            int_index = int(index)

            # Check if already cached
            if int_index in self._hydrated_cache:
                return self._hydrated_cache[int_index]

            # Check bounds (allow negative indexing like Python lists)
            if self._raw_value is None or not (
                -len(self._raw_value) <= int_index < len(self._raw_value)
            ):
                raise IndexError("Index out of range")

            # Lazy create the child object
            raw_value = self._raw_value[int_index]
            self._hydrated_cache[int_index] = self._create_child(raw_value)
            return self._hydrated_cache[int_index]

        except (IndexError, TypeError, ValueError):
            from .notation_primitive import NotationPrimitive

            # Don't cache error results as they might be valid later
            return NotationPrimitive(None, self._depth, **self._kwargs)

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set an element by index in the underlying list.

        Parameters:
            index (int): The index to set
            value: The value to set (will be unwrapped if a Notation object)
        """
        raw_value = self._unwrap(value)
        int_index = int(index)
        self._raw_value[int_index] = raw_value
        self._hydrated_cache.pop(int_index, None)

    def __delitem__(self, index: int) -> None:
        """
        Delete an element by index from the underlying list.

        Parameters:
            index (int): The index to delete

        Raises:
            IndexError: If the index is out of range
        """
        int_index = int(index)
        del self._raw_value[int_index]
        # Clear entire cache since indices shift after deletion
        self._hydrated_cache.clear()

    def __int__(self) -> int:
        """
        Convert array to int (should fail for list structures).

        Raises:
            TypeError: Always raises as list cannot be converted to int
        """
        raise TypeError("Cannot convert list to int")

    def __float__(self) -> float:
        """
        Convert array to float (should fail for list structures).

        Raises:
            TypeError: Always raises as list cannot be converted to float
        """
        raise TypeError("Cannot convert list to float")

    def __bool__(self) -> bool:
        """
        Convert array to bool following Python's truthiness rules.
        Empty lists are False, non-empty lists are True.

        Returns:
            bool: False if list is empty, True otherwise
        """
        if self._raw_value is None:
            return False
        return bool(self._raw_value)
