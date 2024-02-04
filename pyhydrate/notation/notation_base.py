"""
Provides shared base functionality for Notation classes.

The NotationBase class implements common methods and attributes
needed by all Notation objects such as formatted output, type
checking, recursion depth tracking, etc.

Child classes inherit from NotationBase to get this base functionality.
"""
from typing import Union
from typing import Pattern
from typing import Any
import json
import yaml
import re
from .notation_dumper import NotationDumper
from .notation_representation import NotationRepresentation


class NotationBase(NotationRepresentation):
    """
    Base Notation class with shared attributes and methods.

    NotationBase provides common functionality needed across all
    Notation classes like formatted output, casting keys, tracking
    depth, etc. Child classes will inherit this to reduce code duplication.

    Attributes:
        _raw_value (str): The original untouched value.
        _cleaned_value (str): The processed value after type checking.
        _hydrated_value (str): The wrapped Notation object.
        _cast_pattern (Pattern[Any]): Regex raw string pattern for formatting
        object/dict keys.
        _kwargs (dict): Additional options passed during initialization.
        _depth (int): Recursion depth of wrapper class.
    """

    # CLASS CONSTANTS
    _source_key: str = '__SOURCE_KEY__'
    _cleaned_key: str = '__CLEANED_KEY__'
    _hydrated_key: str = '__HYDRATED_KEY__'
    _cast_pattern: Pattern[Any] = re.compile(r'(?<!\d)(?=\d)|(?<=\d)(?!\d)|(?<=[a-z])(?=[A-Z])')

    # CLASS VARIABLES
    _raw_value: Union[dict, list, None] = None
    _cleaned_value: Union[dict, list, None] = None
    _hydrated_value: Union[dict, list, None] = None
    _kwargs: dict = {}
    _depth: int = 1

    # EXTERNAL METHODS
    def yaml(self) -> Union[str, None]:
        """
        Serialize the value to YAML format.

        Returns:
            str: The YAML string if value is dict/list, else the `element`
                 value of the NotationPrimitive.
        """
        if isinstance(self._value, dict) or isinstance(self._value, list):
            return yaml.dump(self._value, sort_keys=False, Dumper=NotationDumper).rstrip()
        else:
            return yaml.dump(self._element, sort_keys=False, Dumper=NotationDumper).rstrip()
        # TODO: handle None

    def json(self) -> Union[str, None]:
        """
        Serialize the value to JSON format.

        Returns:
            str: The JSON string if value is dict/list, else None.
        """
        return json.dumps(self._value, indent=self._indent)
        # TODO: handle None

    # INTERNAL METHODS
    def _cast_key(self, string: str) -> str:
        """
        Format keys to be lowercase and underscore separated.

        Parameters:
            string (str): The object/dict key that is to be
            restated as lower case snake formatting.

        Returns:
            str: A new key value to be used with dot notation.
        """
        _kebab_clean: str = string.replace('-', '_').replace(' ', '_')
        _parsed = self._cast_pattern.sub('_', _kebab_clean)
        return re.sub(r'_+', r'_', _parsed).lower().strip('_')

    def _print_debug(self, request: str, request_value: Union[str, int], stop: bool = False):
        """
        Print debug info about the object.

        Parameters:
            request (str): The request type that is trying to access the
            e.g. 'Call', 'Get', or 'Slice'.
            request_value (str, int): The attribute key or index slice
            used to access the underlying value.
            stop (bool): Used to stop printing, even if `debug` is True.
            Used primarily for internal purposes.
        """

        _component_type: Union[str, None] = None
        _output: Union[str, None] = None

        if self._debug and not stop:
            if self._type == dict:
                _component_type = 'Object'
                _output = ''
            elif self._type == list:
                _component_type = 'Array'
                _output = ''
            else:
                _component_type = 'Primitive'
                _output = f" :: Output == {self._value}"

            _print_value = (f"{'   ' * self._depth}>>> {_component_type} :: "
                            f"{request} == {request_value} :: Depth == {self._depth}"
                            f"{_output}")
            print(_print_value)

    # MAGIC METHODS
    def __str__(self) -> str:
        """
        Print the object in YAML format by default.

        This allows print(my_obj) to show a readable YAML string.

        Returns:
            str: The object in YAML format.
        """
        return self.yaml()

    def __call__(self, *args, **kwargs) -> Union[dict, list, str, int, float, bool, type, None]:
        """
        Call the object as a function to get specific values.

        Allowed values for args[0] are:
            - 'value': The cleaned _value attribute.
            - 'element': The _element attribute.
            - 'type': The object's type.
            - 'depth': The recursion depth.

        Utilized key/values for kwargs are:
            - debug: TODO:
            - indent: TODO:

        Args:
            *args: The value to retrieve.
            **kwargs: Additional options.

        Returns:
            dict, list, str, int, float, bool, type, None: Requested value, element, structure, or type.
        """
        #
        _stop: bool = kwargs.get('stop', False)

        # get the "call type" to return the correct result
        try:
            self._call = args[0]
        except IndexError:
            self._call = 'value'
        finally:
            self._print_debug('Call', self._call, _stop)

        #
        if self._call == 'value':
            return self._value
        elif self._call == 'element':
            return self._element
        elif self._call == 'type':
            return self._type
        elif self._call == 'depth':
            return self._depth
        elif self._call == 'map':
            return None
        else:
            # TODO: load warnings of bad call
            return None

    # INTERNAL READ-ONLY PROPERTIES
    @property
    def _element(self) -> Union[dict, None]:
        """
        The dict representation of the structure or primitive. There is one
        key and one value. The <key> is the type, and <value> is the value.

        Returns
            dict: {type: structure | primitive}
        """
        return {self._type.__name__: self._value}

    @property
    def _value(self) -> Union[dict, list, None]:
        """
        The cleaned value(s), i.e. keys are converted to lower case snake.

        Returns:
            str: the value with cleaned object keys.
        """
        return self._cleaned_value

    @property
    def _type(self) -> type:
        """
        The requested value's (structure or primitive) type.

        Returns:
            type: dict, list, str, int, float, bool, NoneType
        """
        return type(self._value)

    @property
    def _map(self) -> Union[dict, list, None]:
        """
        TBD

        Returns:
            dict, list: TBD
        """
        return None


if __name__ == '__main__':
    pass
