import yaml
from typing import Union
from typing import List
import warnings
from .notation_base import NotationBase


class NotationValue(NotationBase):
    _value: Union[str, int, float, bool, None] = None
    _primitives: List[type] = [str, int, float, bool, type(None)]

    def __init__(self, value: Union[str, int, float, bool, None], depth: int = 0):

        self._depth = depth + 1

        if type(value) in self._primitives:
            self._raw_value = value
            self._cleaned_value = value
        else:
            self._raw_value = None
            self._cleaned_value = None
            _warning: str = (f"The `{self.__class__.__name__}` class does not support type '{type(value).__name__}'. "
                             f"`None` value and `NoneType` returned instead.")
            warnings.warn(_warning)

    def __getattr__(self, key: str):  # TODO: add self...
        print(f"{'   ' * (self.depth - 1)} => Value :: Get == {key} :: Depth == {self.depth}")
        return NotationValue(None)

    def __getitem__(self, index):
        print(f"{'   ' * (self.depth - 1)} => Value :: Slice == {index} :: Depth == {self.depth}")
        return NotationValue(None)


if __name__ == '__main__':
    pass
