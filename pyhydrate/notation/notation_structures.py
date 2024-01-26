from typing import Union
from typing import List
from typing import Tuple

# from .notation_print import notation_print
from typing_extensions import Self
from .notation_base import NotationBase
from .notation_value import NotationValue

import json
import warnings


class NotationObject(NotationBase):
    """

    """

    def __init__(self, value: dict, depth: int = 0):
        """

        :param value:
        """
        self._depth = depth + 1

        if isinstance(value, dict):
            self._raw_value = value

            _cleaned: dict = {}
            _hydrated: dict = {}
            for _k, _v in value.items():
                _casted_key = self.cast_key(_k)

                if isinstance(_v, dict):
                    _hydrated[_casted_key] = NotationObject(_v, self._depth)
                    _cleaned[_casted_key] = NotationObject(_v, self._depth).value
                elif isinstance(_v, list):
                    _hydrated[_casted_key] = NotationArray(_v, self._depth)
                    _cleaned[_casted_key] = NotationArray(_v, self._depth).value
                else:
                    _hydrated[_casted_key] = NotationValue(_v, self._depth)
                    _cleaned[_casted_key] = NotationValue(_v, self._depth).value

            self._cleaned_value = _cleaned
            self._hydrated_value = _hydrated
        else:
            # self._raw_value = None
            _warning: str = (f"The `{self.__class__.__name__}` class does not support type '{type(value).__name__}'. "
                             f"`None` value and `NoneType` returned instead.")
            warnings.warn(_warning)

    def __getattr__(self, key: str):
        print(f"{'   ' * (self.depth - 1)} => Object :: Get == {key} :: Depth == {self.depth}")
        return self._hydrated_value.get(key, NotationValue(None))

    def __getitem__(self, index: int):
        print(f"{'   ' * (self.depth - 1)} => Object :: Slice == {index} :: Depth == {self.depth}")
        if isinstance(self._hydrated_value, dict):
            return NotationValue(None)


class NotationArray(NotationBase):
    """
    """

    def __init__(self, value: list, depth: int = 0):
        """

        :param value:
        """
        self._depth = depth + 1

        if isinstance(value, list):
            self._raw_value = value
            self._cleaned_value = value

            _hydrated: list = []
            for _k, _v in enumerate(value):
                if isinstance(_v, dict):
                    _hydrated.append(NotationObject(_v, self._depth))
                elif isinstance(_v, list):
                    _hydrated.append(NotationArray(_v, self._depth))
                else:
                    _hydrated.append(NotationValue(_v, self._depth))

            self._hydrated_value = _hydrated
        else:
            # self._value = NotationValue(None)
            _warning: str = (f"The `{self.__class__.__name__}` class does not support type '{type(value).__name__}'. "
                             f"`None` value and `NoneType` returned instead.")
            warnings.warn(_warning)

    def __getattr__(self, key: str):
        print(f"{'   ' * (self.depth - 1)} => Array :: Get == {key} :: Depth == {self.depth}")
        return NotationValue(None)

    def __getitem__(self, index: int) -> Union[Self, NotationObject, NotationValue]:
        print(f"{'   ' * (self.depth - 1)} => Array :: Slice == {index} :: Depth == {self.depth}")
        try:
            return self._hydrated_value[int(index)]
        except IndexError:
            print('index error')
            return NotationValue(None)
        except TypeError:
            print('type error')
            return NotationValue(None)
        except ValueError:
            print('value error')
            return NotationValue(None)


if __name__ == '__main__':
    pass
