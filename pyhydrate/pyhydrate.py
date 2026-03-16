"""
PyHydrate - Elegant dot notation access for nested data structures.

This module provides the main PyHydrate class, which enables intuitive dot notation
access to nested data structures including dictionaries, lists, JSON, YAML, and TOML
with automatic key normalization and graceful error handling.

Key Features:
    - Automatic parsing of JSON, YAML, and TOML strings
    - Dot notation access (e.g., data.user.name)
    - Automatic key normalization (camelCase → snake_case)
    - Lazy loading for memory efficiency
    - Graceful error handling with informative warnings
    - Multiple output formats (JSON, YAML, Python types)
    - Magic method support for type conversion

Basic Usage:
    >>> from pyhydrate import PyHydrate
    >>> data = PyHydrate({"user": {"firstName": "John", "age": 30}})
    >>> data.user.first_name()  # Automatic camelCase → snake_case
    'John'
    >>> data.user.age()
    30
    >>> data.user("json")  # Export as JSON
    '{"firstName": "John", "age": 30}'

Input Format Support:
    - Python dictionaries and lists
    - JSON strings (parsed automatically)
    - YAML strings (parsed automatically)
    - TOML strings (parsed automatically)
    - Primitive values (str, int, float, bool, None)

Memory Efficiency:
    PyHydrate uses lazy loading to minimize memory usage. Child objects are only
    created when accessed, reducing memory consumption by ~67% compared to eager
    loading approaches.

Debug Mode:
    >>> data = PyHydrate(source, debug=True)
    Enables detailed logging of data access patterns for troubleshooting.

Architecture:
    PyHydrate inherits from NotationBase and orchestrates the creation of
    appropriate notation objects (NotationObject, NotationArray, NotationPrimitive)
    based on the input data type.
"""

import contextlib
import json
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Union

import yaml

# Handle TOML imports for different Python versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

# Import at top level to avoid PLC0415
from .error_handling import setup_logger
from .notation import (
    NotationArray,
    NotationObject,
    NotationPrimitive,
    NotationProxy,
)
from .notation.notation_base import NotationBase


class PyHydrate(NotationBase):
    """
    Main entry point for PyHydrate library providing dot notation access to data.

    PyHydrate automatically detects input data types and creates appropriate
    wrapper objects for intuitive access using dot notation. It supports
    automatic parsing of JSON, YAML, and TOML strings, along with native
    Python data structures.

    The class implements lazy loading for memory efficiency and provides
    comprehensive error handling with graceful fallbacks.

    Attributes:
        _root_type: The original data type of the input value
        _structure: The wrapped notation object (NotationObject/Array/Primitive)

    Examples:
        >>> # Dictionary access
        >>> data = PyHydrate({"user": {"name": "Alice", "age": 25}})
        >>> data.user.name()
        'Alice'

        >>> # JSON string parsing
        >>> json_data = PyHydrate('{"status": "active", "count": 42}')
        >>> json_data.status()
        'active'

        >>> # List access
        >>> list_data = PyHydrate([{"id": 1}, {"id": 2}])
        >>> list_data[0].id()
        1

        >>> # Key normalization
        >>> camel_data = PyHydrate({"firstName": "Bob", "lastName": "Smith"})
        >>> camel_data.first_name()  # camelCase → snake_case
        'Bob'

        >>> # Output formats
        >>> data.user("json")  # JSON string
        >>> data.user("yaml")  # YAML string
        >>> data.user("type")  # Python type
        >>> data.user()       # Raw value
    """

    # Memory optimization with __slots__
    __slots__ = ("_root_type", "_source_path", "_structure")

    # Internal attributes that should bypass __setattr__ data path
    _INTERNAL_ATTRS: frozenset = frozenset(
        {
            "_raw_value",
            "_root_type",
            "_source_path",
            "_structure",
            "_kwargs",
            "_depth",
            "_debug",
            "_call",
            "_parent",
            "_parent_key",
        }
    )

    # INTERNAL METHODS
    def _print_root(self) -> None:
        """
        Internal method for debug logging of root data access.

        Logs the root access pattern when debug mode is enabled,
        showing the class name and underlying data type.
        """
        if self._debug:
            logger = setup_logger(
                f"{self.__class__.__module__}.{self.__class__.__name__}", debug=True
            )
            logger.debug(
                f"Root access: {self.__class__.__name__} -> {type(self._raw_value).__name__}"
            )

    @staticmethod
    def _load_from_path(file_path: Path) -> Any:
        """
        Load data from a file path with automatic format detection.

        Determines the file format based on extension and loads the content
        using the appropriate parser. Supports JSON, YAML, and TOML formats.

        Args:
            file_path: Path to the file to load

        Returns:
            Any: Parsed data from the file

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file extension is not supported
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get file extension for format detection
        extension = file_path.suffix.lower()
        content = file_path.read_text(encoding="utf-8")

        if extension == ".json":
            return json.loads(content)
        if extension in (".yaml", ".yml"):
            return yaml.safe_load(content)
        if extension == ".toml":
            if tomllib is None:
                raise ValueError(
                    "TOML support not available. Install tomli for Python < 3.11"
                )
            return tomllib.loads(content)
        raise ValueError(
            f"Unsupported file extension: {extension}. "
            f"Supported formats: .json, .yaml, .yml, .toml"
        )

    # MAGIC METHODS
    def __init__(
        self,
        source_value: Union[dict, list, str, float, bool, None] = None,
        *,
        path: Union[str, Path, None] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize PyHydrate with automatic data type detection and parsing.

        The constructor can accept either direct data or a file path. For file paths,
        it automatically detects the format based on file extension (.json, .yaml,
        .yml, .toml) and loads the content appropriately. String inputs are parsed
        as JSON, TOML, then YAML in that order.

        Args:
            source_value: Input data of any supported type:
                - dict: Wrapped in NotationObject
                - list: Wrapped in NotationArray
                - str: Parsed as JSON/TOML/YAML, then wrapped appropriately
                - int/float/bool/None: Wrapped in NotationPrimitive
                - If None and path is provided, data will be loaded from file
            path: Path to a file containing data to load:
                - Supports .json, .yaml, .yml, .toml file extensions
                - Automatically detects format from extension
                - Takes precedence over source_value if both provided
            **kwargs: Additional options:
                - debug (bool): Enable debug logging (default: False)
                - Other options passed to notation wrapper classes

        Raises:
            ValueError: If neither source_value nor path is provided
            FileNotFoundError: If the specified path does not exist
            ValueError: If file extension is not supported

        Examples:
            >>> # Dictionary input
            >>> data = PyHydrate({"key": "value"})

            >>> # File path input
            >>> data = PyHydrate(path="config.json")
            >>> data = PyHydrate(path="settings.yaml")
            >>> data = PyHydrate(path="data.toml")

            >>> # JSON string input (auto-parsed)
            >>> data = PyHydrate('{"key": "value"}')

            >>> # YAML string input (auto-parsed)
            >>> data = PyHydrate('key: value')

            >>> # Debug mode
            >>> data = PyHydrate(source, debug=True)
            >>> data = PyHydrate(path="config.json", debug=True)
        """
        self._kwargs = kwargs
        self._debug = kwargs.get("debug", False)
        self._parent = None
        self._parent_key = None
        self._source_path = Path(path) if path is not None else None

        # Handle file path input
        if path is not None:
            source_value = self._load_from_path(Path(path))
        # Note: source_value=None is a valid value (for None primitives)

        # try to translate string to json, if we fail, just quit attempt
        if isinstance(source_value, str):
            with contextlib.suppress(JSONDecodeError):
                source_value = json.loads(source_value)

        # if we still have a string, try to translate as if it were toml
        if isinstance(source_value, str) and tomllib is not None:
            with contextlib.suppress(tomllib.TOMLDecodeError, ValueError):
                source_value = tomllib.loads(source_value)

        # if we still have a string, try to translate as if it were yaml
        if isinstance(source_value, str):
            source_value = yaml.safe_load(source_value)

        if isinstance(source_value, dict):
            self._root_type = dict
            self._structure = NotationObject(source_value, 0, **kwargs)
        elif isinstance(source_value, list):
            self._root_type = list
            self._structure = NotationArray(source_value, 0, **kwargs)
        elif isinstance(source_value, (int, float, bool, str)):
            self._root_type = type(source_value)
            self._structure = NotationPrimitive(source_value, 0, **kwargs)
        elif isinstance(source_value, type(None)):
            self._root_type = type(None)
            self._structure = NotationPrimitive(None, 0, **kwargs)
        else:
            self._root_type = type(None)
            self._structure = None

    def __str__(self) -> str:
        """
        Return YAML string representation of the wrapped data.

        This method triggers debug logging if enabled and returns
        the data formatted as a YAML string for readable output.

        Returns:
            str: YAML-formatted string representation of the data
        """
        self._print_root()
        return self._structure("yaml")

    def __int__(self) -> int:
        """
        Convert the wrapped value to int.

        Delegates to the underlying structure's __int__ method,
        which handles type conversion with appropriate error handling.

        Returns:
            int: Integer representation of the wrapped value

        Raises:
            TypeError: If conversion to int is not possible
            ValueError: If the value cannot be interpreted as an integer
        """
        return int(self._structure)

    def __float__(self) -> float:
        """
        Convert the wrapped value to float.

        Delegates to the underlying structure's __float__ method,
        which handles type conversion with appropriate error handling.

        Returns:
            float: Float representation of the wrapped value

        Raises:
            TypeError: If conversion to float is not possible
            ValueError: If the value cannot be interpreted as a float
        """
        return float(self._structure)

    def __bool__(self) -> bool:
        """
        Convert the wrapped value to bool.

        Delegates to the underlying structure's __bool__ method,
        which handles truthiness evaluation with appropriate logic.

        Returns:
            bool: Boolean representation of the wrapped value
        """
        return bool(self._structure)

    def __getattr__(
        self, key: str
    ) -> Union[NotationArray, NotationObject, NotationPrimitive, NotationProxy, None]:
        """
        Enable dot notation access to nested data.

        This method is called when accessing attributes that don't exist
        on the PyHydrate instance, delegating to the wrapped structure
        for dot notation access (e.g., data.user.name).

        If the underlying structure is a primitive (e.g., empty PyHydrate()),
        returns a NotationProxy for potential write-through creation.

        Args:
            key (str): The attribute name to access

        Returns:
            Union[NotationArray, NotationObject, NotationPrimitive, NotationProxy, None]:
                The wrapped value at the specified key, or proxy if not found
        """
        if isinstance(self._structure, NotationPrimitive):
            return NotationProxy(parent=self, parent_key=key)
        return getattr(self._structure, key)

    def __getitem__(
        self, index: Union[int, None]
    ) -> Union[NotationArray, NotationObject, NotationPrimitive, None]:
        """
        Enable bracket notation access for list-like data.

        This method enables array-style access (e.g., data[0]) by
        delegating to the wrapped structure's __getitem__ method.

        Args:
            index (Union[int, None]): The index to access

        Returns:
            Union[NotationArray, NotationObject, NotationPrimitive, None]:
                The wrapped value at the specified index, or None if not found
        """
        return self._structure[index]

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Set a value via dot notation or initialize internal attributes.

        Internal attributes are set normally. All other keys are treated
        as data writes. If the underlying structure is not a NotationObject,
        it is promoted to one (enabling creation from scratch).

        Args:
            key (str): The attribute/key name
            value: The value to set
        """
        if key in PyHydrate._INTERNAL_ATTRS or key.startswith("__"):
            object.__setattr__(self, key, value)
            return
        # Promote structure to NotationObject if needed
        if not isinstance(self._structure, NotationObject):
            new_obj = NotationObject({}, 0, **self._kwargs)
            object.__setattr__(self, "_structure", new_obj)
            object.__setattr__(self, "_root_type", dict)
            object.__setattr__(self, "_raw_value", new_obj._raw_value)
        setattr(self._structure, key, value)

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set an element by index for list-like data.

        Args:
            index (int): The index to set
            value: The value to set
        """
        if isinstance(self._structure, NotationArray):
            self._structure[index] = value

    def __delattr__(self, key: str) -> None:
        """
        Delete a key from the underlying data.

        Args:
            key (str): The key to delete

        Raises:
            AttributeError: If key is an internal attribute or not found
        """
        if key in PyHydrate._INTERNAL_ATTRS or key.startswith("__"):
            raise AttributeError(f"Cannot delete internal attribute '{key}'")
        if isinstance(self._structure, NotationObject):
            delattr(self._structure, key)
        else:
            raise TypeError(f"Cannot delete '{key}' on non-object structure")

    def __delitem__(self, index: int) -> None:
        """
        Delete an element by index for list-like data.

        Args:
            index (int): The index to delete

        Raises:
            TypeError: If the underlying structure is not an array
        """
        if isinstance(self._structure, NotationArray):
            del self._structure[index]
        else:
            raise TypeError("Cannot delete items on non-array structure")

    def save(
        self,
        path: Union[str, Path, None] = None,
        *,
        output_format: Union[str, None] = None,
    ) -> None:
        """
        Save the current data to a file.

        Determines the output format from the file extension (or explicit
        output_format parameter) and writes the serialized data.

        Args:
            path: File path to write to. If None, uses the original
                source path from construction.
            output_format: Force a specific format ('json', 'yaml', 'toml').
                If None, detected from file extension.

        Raises:
            ValueError: If no path is available or format cannot be determined
        """
        if path is None:
            path = self._source_path
        if path is None:
            raise ValueError("No file path specified and no source path available")

        file_path = Path(path)
        fmt = output_format or self._detect_format(file_path)

        content = self._structure(fmt)
        if content is None:
            raise ValueError(f"Cannot serialize to '{fmt}'")

        # Ensure trailing newline for file output
        if not content.endswith("\n"):
            content += "\n"

        file_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _detect_format(file_path: Path) -> str:
        """
        Detect the serialization format from a file extension.

        Args:
            file_path: The file path to inspect

        Returns:
            str: The format string ('json', 'yaml', or 'toml')

        Raises:
            ValueError: If the extension is not recognized
        """
        ext_map = {
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
        }
        ext = file_path.suffix.lower()
        if ext not in ext_map:
            raise ValueError(
                f"Cannot detect format from extension: '{ext}'. "
                f"Supported: .json, .yaml, .yml, .toml"
            )
        return ext_map[ext]

    def __call__(
        self, *args: Any
    ) -> Union[dict, list, str, int, float, bool, type, None]:
        """
        Enable function-style value extraction and format conversion.

        This method allows the PyHydrate object to be called like a function
        to extract values in different formats. With no arguments, returns
        the raw value. With format arguments, returns formatted output.

        Args:
            *args: Optional format specifiers:
                - No args: Returns raw cleaned value
                - 'json': Returns JSON string representation
                - 'yaml': Returns YAML string representation
                - 'type': Returns Python type of the value
                - 'element': Returns {type: value} dictionary
                - 'depth': Returns recursion depth

        Returns:
            Union[dict, list, str, int, float, bool, type, None]:
                The value in the requested format

        Examples:
            >>> data = PyHydrate({"name": "Alice", "age": 30})
            >>> data.name()  # Raw value
            'Alice'
            >>> data.age('json')  # JSON format
            '30'
            >>> data.name('type')  # Python type
            <class 'str'>
        """
        try:
            return self._structure(args[0])
        except IndexError:
            return self._structure()
