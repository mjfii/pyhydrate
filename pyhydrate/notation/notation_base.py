from typing import Union
import json
import yaml
import re
from .notation_dumper import NotationDumper
from .notation_representation import NotationRepresentation


class NotationBase(NotationRepresentation):
    """

    """
    # CONSTANTS
    _source_key: str = '__SOURCE_KEY__'
    _cleaned_key: str = '__CLEANED_KEY__'
    _hydrated_key: str = '__HYDRATED_KEY__'

    # CLASS VARIABLES
    _raw_value: Union[dict, list, None] = None
    _cleaned_value: Union[dict, list, None] = None
    _hydrated_value: Union[dict, list, None] = None
    _kwargs: dict = {}

    # r'(?=[A-Z])' - pascal case without number separation
    # r'(?<!^)(?=[A-Z])' - camel case without number separation
    # r'(?<!^)(?=[A-Z])|(?<=[a-z])(?=\d)'  # - camel case with number separation
    # r'(?<!^)(?=[A-Z])|(?<=-)(?=[a-z])|(?<=[a-z])(?=\d)'
    _cast_pattern = re.compile(r'(?<!\d)(?=\d)|(?<=\d)(?!\d)|(?<=[a-z])(?=[A-Z])')
    _indent: int = 3
    _depth: int = 1
    _request: str = 'value'

    # EXTERNAL METHODS
    def yaml(self) -> Union[str, None]:
        if isinstance(self._value, dict) or isinstance(self._value, list):
            return yaml.dump(self._value, sort_keys=False, Dumper=NotationDumper).rstrip()
        else:
            return yaml.dump(self._element, sort_keys=False, Dumper=NotationDumper).rstrip()

    def json(self) -> Union[str, None]:
        return json.dumps(self._value, indent=self._indent)

    # INTERNAL METHODS
    def cast_key(self, string: str) -> Union[str, None]:
        """

        :param string:
        :return:
        """
        _kebab_clean: str = string.replace('-', '_').replace(' ', '_')
        _parsed = self._cast_pattern.sub('_', _kebab_clean)
        return re.sub(r'_+', r'_', _parsed).lower().strip('_')

    def _print_debug(self, request: str, request_value: Union[str, int], stop: bool = False) -> None:

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
        return self.yaml()

    def __call__(self, *args, **kwargs) -> Union[dict, str, int, type, None]:

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
        return {self._type.__name__: self._value}

    @property
    def _value(self) -> Union[dict, list, None]:
        return self._cleaned_value

    @property
    def _type(self) -> type:
        return type(self._value)

    @property
    def _map(self) -> Union[dict, list, None]:
        return None


if __name__ == '__main__':
    pass
