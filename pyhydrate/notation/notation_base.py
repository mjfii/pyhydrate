"""
Provides shared base functionality for Notation classes.

The NotationBase class implements common methods and attributes
needed by all Notation objects such as formatted output, type
checking, recursion depth tracking, etc.

Child classes inherit from NotationBase to get this base functionality.
"""

import json
import re
import sys
import textwrap
from typing import Any, Pattern, Union

import yaml

# Handle TOML imports for different Python versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

# TOML writer
try:
    import toml
except ImportError:
    toml = None

from .notation_dumper import NotationDumper


class NotationBase(object):
    """
    Base Notation class with shared attributes and methods.

    NotationBase provides common functionality needed across all
    Notation classes like formatted output, casting keys, tracking
    depth, etc. Child classes will inherit this to reduce code duplication.

    Attributes:
        _cast_pattern (Pattern[Any]): Regex raw string pattern for formatting
        object/dict keys.
    """

    # CLASS CONSTANTS
    _source_key: str = "__SOURCE_KEY__"
    _cleaned_key: str = "__CLEANED_KEY__"
    _hydrated_key: str = "__HYDRATED_KEY__"
    _repr_key: str = "PyHydrate"
    _idk: str = r"¯\_(ツ)_/¯"

    # CLASS DEFAULT PARAMETERS
    _indent: int = 3

    r"""
    This regex uses lookaheads and lookbehinds to match 3 different cases:
        - (?<!\d)(?=\d) - Matches positions that are preceded by a non-digit
                          and followed by a digit. This will match between a
                          non-digit and a digit character.
        - (?<=\d)(?!\d) - Matches positions that are preceded by a digit and
                          followed by a non-digit. This will match between a
                          digit and a non-digit character.
        - (?<=[a-z])(?=[A-Z]) - Matches positions that are preceded by a
                                lowercase letter and followed by an uppercase
                                letter. This will match between a lowercase
                                and uppercase letter.

    So in summary, this regex will match:
        - Between a non-digit and digit character
        - Between a digit and non-digit character
        - Between a lowercase and uppercase letter

    It uses lookarounds to match the positions between the specified characters
    without including those characters in the match.
    """
    _cast_pattern: Pattern[Any] = re.compile(
        r"(?<!\d)(?=\d)|(?<=\d)(?!\d)|(?<=[a-z])(?=[A-Z])"
    )

    # Memory optimization with __slots__
    __slots__ = ("_call", "_debug", "_depth", "_kwargs", "_raw_value")

    # INTERNAL METHODS
    def _cast_key(self, string: str) -> str:
        """
        Format keys to be lowercase and underscore separated.

        Parameters:
            string (str): The object/dict key that is to be
            restated as lower case snake formatting.

        Returns:
            str
        """
        _kebab_clean: str = string.replace("-", "_").replace(" ", "_")
        _parsed = self._cast_pattern.sub("_", _kebab_clean)
        return re.sub(r"_+", r"_", _parsed).lower().strip("_")

    def _print_debug(
        self, request: str, request_value: Union[str, int], *, stop: bool = False
    ) -> None:
        """
        Print debug info about the object.

        Parameters:
            request (str): The request type that is trying to access the
            e.g. 'Call', 'Get', or 'Slice'.
            request_value (str, int): The attribute key or index slice
            used to access the underlying value.
            stop (bool): Used to stop printing, even if `debug` is True.
            Used primarily for internal purposes.

        Returns:
            None
        """

        _component_type: Union[str, None] = None
        _output: Union[str, None] = None

        if self._debug and not stop:
            from ..error_handling import setup_logger

            if self._type is dict:
                _component_type = "Object"
                _output = ""
            elif self._type is list:
                _component_type = "Array"
                _output = ""
            else:
                _component_type = "Primitive"
                _output = f" :: Output == {self._value}"

            logger = setup_logger(
                f"{self.__class__.__module__}.{self.__class__.__name__}", debug=True
            )
            logger.debug(
                f"{'   ' * self._depth}>>> {_component_type} :: "
                f"{request} == {request_value} :: Depth == {self._depth}{_output}"
            )

    # MAGIC METHODS
    def __str__(self) -> str:
        """
        Print the object in YAML format by default.

        This allows print(my_obj) to show a readable YAML string.

        Returns:
            str: The object in YAML format.
        """
        return self._yaml

    def __repr__(self) -> str:
        """
        Implement customized `__repr__` formatting and representation.

        Returns:
            str
        """

        # Try to get the raw value from the object
        try:
            _working_value: Union[str, None] = getattr(self, "_raw_value", None)
        except AttributeError:
            return f"{self._repr_key}(None)"

        # Try to get the raw value from withing the structure object
        # TODO: is this necessary?
        if not _working_value:
            try:
                _structure = getattr(self, "_structure", None)
                if _structure:
                    _working_value = getattr(_structure, "_raw_value", None)
            except AttributeError:
                return f"{self._repr_key}(None)"

        # Handle different working value types
        if _working_value:
            # return the quoted string
            if isinstance(_working_value, str):
                return f"{self._repr_key}('{_working_value}')"
            # return the non-string unquoted primitive
            if isinstance(_working_value, (bool, float, int)):
                return f"{self._repr_key}({_working_value})"
            # return an indented string
            # TODO: this is incomplete, the structure should be quoted and escaped
            if isinstance(_working_value, (dict, list)):
                _return_value: str = textwrap.indent(
                    json.dumps(_working_value, indent=3), 3 * " "
                )
                return f"{self._repr_key}(\n{_return_value}\n)"
            # the primitive or structure is not handled, a warning should exist,
            # return and unknown representation
            return f"{self._repr_key}('{self._idk}')"
        # a known representation does not exist, return None/unknown
        return f"{self._repr_key}(None)"

    def __call__(
        self, *args: Any, **kwargs: Any
    ) -> Union[dict, list, str, int, float, bool, type, None]:
        """
        Call the object as a function to get specific values.

        Allowed values for args[0] are:
            - 'value': The cleaned _value attribute.
            - 'element': The _element attribute.
            - 'type': The object's type.
            - 'depth': The recursion depth.
            - 'map': The key mapping (when implemented).
            - 'json': JSON string representation.
            - 'yaml': YAML string representation.
            - 'toml': TOML string representation.

        Invalid call types will issue a UserWarning and return None.

        Utilized key/values for kwargs are:
            - debug: TODO:
            - indent: TODO:

        Args:
            *args: The value to retrieve.
            **kwargs: Additional options.

        Returns:
            Union[dict, list, str, int, float, bool, type, None]: The requested value or None for invalid call types.

        Warnings:
            UserWarning: When an invalid call type is provided.
        """
        _stop: bool = kwargs.get("stop", False)

        # get the "call type" to return the correct result
        try:
            self._call = args[0]
        # if no "call type" was provided, use `value`
        except IndexError:
            self._call = "value"
        finally:
            # if no "call type" is None, also use `value`
            if not self._call:
                self._call = "value"
            self._print_debug("Call", self._call, stop=_stop)

        # based on the "call type", return the requested data
        if self._call == "value":
            return self._value
        if self._call == "element":
            return self._element
        if self._call == "type":
            return self._type
        if self._call == "depth":
            return self._depth
        if self._call == "map":
            return self._map
        if self._call == "json":
            return self._json
        if self._call == "yaml":
            return self._yaml
        if self._call == "toml":
            return self._toml
        # Invalid call type - issue warning and return None
        from ..error_handling import handle_api_usage_error

        valid_calls = [
            "value",
            "element",
            "type",
            "depth",
            "map",
            "json",
            "yaml",
            "toml",
        ]
        handle_api_usage_error(
            operation="Call type",
            provided_value=self._call,
            valid_options=valid_calls,
            debug=self._debug,
        )
        return None

    # INTERNAL READ-ONLY PROPERTIES
    @property
    def _element(self) -> dict:
        """
        The dict representation of the structure or primitive. There is one
        key and one value. The <key> is the type, and <value> is the value.

        Returns:
            dict {type: structure | primitive}
        """
        return {self._type.__name__: self._value}

    @property
    def _value(self) -> Union[dict, list, None]:
        """
        The cleaned value(s), i.e. keys are converted to lower case snake.
        Now computed on-demand for memory efficiency.

        Returns:
            Union[dict, list, None]
        """
        return self._cleaned_value

    @property
    def _type(self) -> type:
        """
        The requested value's (structure or primitive) type.

        Returns:
            type
        """
        return type(self._value)

    @property
    def _cleaned_value(self) -> Union[dict, list, None]:
        """
        Compute cleaned value on demand for memory efficiency.

        Returns:
            Union[dict, list, None]
        """
        return self._get_cleaned_value()

    def _get_cleaned_value(self) -> Union[dict, list, None]:
        """
        Helper method to compute cleaned value on demand.
        Override in child classes for specific behavior.

        Returns:
            Union[dict, list, None]
        """
        return self._raw_value

    def _create_child(self, value: Union[dict, list, Any]) -> "NotationBase":
        """
        Factory method for creating child notation objects.

        Parameters:
            value: The raw value to wrap

        Returns:
            NotationBase: The appropriate notation object
        """
        if isinstance(value, dict):
            from .notation_structures import NotationObject

            return NotationObject(value, self._depth, **self._kwargs)
        if isinstance(value, list):
            from .notation_structures import NotationArray

            return NotationArray(value, self._depth, **self._kwargs)
        from .notation_primitive import NotationPrimitive

        return NotationPrimitive(value, self._depth, **self._kwargs)

    @property
    def _map(self) -> Union[dict, None]:
        """
        Returns the key mapping dictionary for objects, or None for other types.

        For NotationObject instances, returns a dictionary mapping cleaned keys
        (snake_case) to their original keys (camelCase, kebab-case, etc.).
        For other types (arrays, primitives), returns None.

        Returns:
            Union[dict, None]: Key mappings dict for objects, None otherwise
        """
        # Check if this instance has key mappings (NotationObject)
        if hasattr(self, "_key_mappings"):
            return getattr(self, "_key_mappings", None)
        return None

    @property
    def _yaml(self) -> Union[str, None]:
        """
        Serialize the value to YAML format. Returns The YAML string if value is
        dict/list, else the `element` value of the NotationPrimitive.

        Handles None values by returning them in the standard element format.

        Returns:
            Union[str, None]
        """
        if self._value is None:
            return yaml.dump(
                self._element, sort_keys=False, Dumper=NotationDumper
            ).rstrip()
        if isinstance(self._value, (dict, list)):
            return yaml.dump(
                self._value, sort_keys=False, Dumper=NotationDumper
            ).rstrip()
        return yaml.dump(self._element, sort_keys=False, Dumper=NotationDumper).rstrip()

    @property
    def _json(self) -> Union[str, None]:
        """
        Serialize the value to JSON format. Returns the JSON string if value is
        dict/list, else the element format for primitives including None.

        Handles None values by returning them in JSON format.

        Returns:
            Union[str, None]
        """
        # Get indent from kwargs or use default
        indent = getattr(self, "_indent", 3)

        if self._value is None:
            return json.dumps(self._element, indent=indent)
        if isinstance(self._value, (dict, list)):
            return json.dumps(self._value, indent=indent)
        # For primitives, return the element format for consistency
        return json.dumps(self._element, indent=indent)

    @property
    def _toml(self) -> Union[str, None]:
        """
        Serialize the value to TOML format. Returns the TOML string if value is
        dict/list, else the element format for primitives including None.

        Handles None values by returning them in TOML format.
        Only dict objects can be serialized to TOML (TOML specification requirement).

        Returns:
            Union[str, None]
        """
        if toml is None:
            from ..error_handling import handle_api_usage_error

            handle_api_usage_error(
                operation="TOML serialization",
                provided_value="unavailable",
                valid_options=["install toml library: pip install toml"],
                debug=self._debug,
            )
            return None

        if self._value is None:
            # TOML doesn't support None, return element format if it's a dict
            if isinstance(self._element, dict):
                return toml.dumps(self._element)
            return None
        if isinstance(self._value, dict):
            return toml.dumps(self._value)
        if isinstance(self._value, list):
            # TOML requires a root table, wrap list in a dict
            return toml.dumps({"data": self._value})
        # For primitives, return the element format if it's a dict
        if isinstance(self._element, dict):
            return toml.dumps(self._element)
        return None
