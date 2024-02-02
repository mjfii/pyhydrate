from typing import Union
from typing import List
from typing_extensions import Self
import warnings
from .notation_base import NotationBase


class NotationPrimitive(NotationBase):

    # CLASS VARIABLES
    _primitives: List[type] = [str, int, float, bool, type(None)]

    def __init__(self, value: Union[str, int, float, bool, None], depth: int, **kwargs):

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
        self._print_debug('Get', key)
        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __getitem__(self, index) -> Self:
        self._print_debug('Slice', index)
        return NotationPrimitive(None, self._depth, **self._kwargs)


if __name__ == '__main__':
    pass
