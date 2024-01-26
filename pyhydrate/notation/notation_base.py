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

    # r'(?=[A-Z])' - pascal case without number separation
    # r'(?<!^)(?=[A-Z])' - camel case without number separation
    # r'(?<!^)(?=[A-Z])|(?<=[a-z])(?=\d)'  # - camel case with number separation
    _cast_pattern = re.compile(r'(?<!^)(?=[A-Z])|(?<=-)(?=[a-z])|(?<=[a-z])(?=\d)')
    _indent: int = 3
    _depth: int = 1

    def __str__(self) -> str:
        return self.yaml

    def __call__(self, *args, **kwargs) -> Union[dict, None]:
        print(f"{'   ' * (self.depth - 1)} => Value :: Call == value :: Depth == {self.depth}")
        return self.value

    # EXTERNAL READ-ONLY PROPERTIES
    @property
    def element(self) -> Union[dict, None]:
        return {self.type.__name__: self.value}

    @property
    def value(self) -> Union[dict, list, None]:
        return self._cleaned_value

    @property
    def type(self) -> type:
        return type(self.value)

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def map(self) -> Union[dict, list, None]:
        return None

    #
    @property
    def yaml(self) -> Union[str, None]:
        if isinstance(self.value, dict) or isinstance(self.value, list):
            return yaml.dump(self.value, sort_keys=False, Dumper=NotationDumper).rstrip()
        else:
            return yaml.dump(self.element, sort_keys=False, Dumper=NotationDumper).rstrip()

    @property
    def json(self) -> Union[str, None]:
        return json.dumps(self.value, indent=self._indent)

    # INTERNAL METHODS
    def cast_key(self, string: str) -> Union[str, None]:
        """

        :param string:
        :return:
        """
        _kebab_clean: str = string.replace('-', '_')
        return self._cast_pattern.sub('_', _kebab_clean).lower()


if __name__ == '__main__':
    pass
