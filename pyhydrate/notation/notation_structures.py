"""
Provides the core NotationObject and NotationArray classes.

This module defines the two key classes used to represent nested
dict and list structures in the `notation` library.

NotationObject wraps a dict structure containing additional
NotationObjects, NotationArrays, and NotationPrimitives.

NotationArray wraps a list structure with the same nested elements.
"""
from typing import Union
from typing_extensions import Self
from .notation_base import NotationBase
from .notation_primitive import NotationPrimitive
import warnings


class NotationObject(NotationBase):
    """
    Class for representing nested dict/object structures.

    NotationObject wraps a dict to provide access to child elements
    using attribute and item access. Children can be other objects,
    arrays, or primitives.
    """

    def __init__(self, value: dict, depth: int, **kwargs) -> None:
        """
        Initialize with the raw dict and recursion depth.

        Parameters:
            value (dict):
            depth (int):
            kwargs (dict):
        """

        # set the local kwargs variable
        self._kwargs = kwargs

        # set the inherited class variables
        self._depth = depth + 1
        self._debug = self._kwargs.get('debug', False)

        if isinstance(value, dict):
            self._raw_value = value

            _cleaned: dict = {}
            _hydrated: dict = {}

            for _k, _v in value.items():
                _casted_key = self._cast_key(_k)

                if isinstance(_v, dict):
                    _hydrated[_casted_key] = NotationObject(_v, self._depth, **kwargs)
                    _cleaned[_casted_key] = _hydrated[_casted_key](stop=True)
                elif isinstance(_v, list):
                    _hydrated[_casted_key] = NotationArray(_v, self._depth, **kwargs)
                    _cleaned[_casted_key] = _hydrated[_casted_key](stop=True)
                else:
                    _hydrated[_casted_key] = NotationPrimitive(_v, self._depth, **kwargs)
                    _cleaned[_casted_key] = _hydrated[_casted_key](stop=True)

            self._cleaned_value = _cleaned
            self._hydrated_value = _hydrated
        else:
            _warning: str = (f"The `{self.__class__.__name__}` class does not support type '{type(value).__name__}'. "
                             f"`None` value and `NoneType` returned instead.")
            warnings.warn(_warning)

    def __getattr__(self, key: str) -> Union[Self, u'NotationArray', NotationPrimitive]:
        """
         Get a child element by attribute name.

         Parameters:
            key (str):

        Returns:
            Union[NotationObject, NotationArray, NotationPrimitive]
         """
        self._print_debug('Get', key)
        return self._hydrated_value.get(key, NotationPrimitive(None, self._depth, **self._kwargs))

    def __getitem__(self, index: int) -> NotationPrimitive:
        """
        Not implemented for objects.

        Parameters:
            index (int):

        Returns:
            NotationPrimitive(None)
        """
        self._print_debug('Slice', index)
        return NotationPrimitive(None, self._depth, **self._kwargs)


class NotationArray(NotationBase):
    """
    Class for representing nested list structures.

    NotationArray wraps a list with nested object/array/primitive
    elements similarly to NotationObject.
    """

    def __init__(self, value: list, depth: int, **kwargs) -> None:
        """
        Initialize with the raw list value.

        Parameters:
            value (list):
            depth (int):
            kwargs (dict):
        """

        # set the local kwargs variable
        self._kwargs = kwargs

        # set the inherited class variables
        self._depth = depth + 1
        self._debug = self._kwargs.get('debug', False)

        if isinstance(value, list):
            self._raw_value = value
            self._cleaned_value = value

            _hydrated: list = []
            for _k, _v in enumerate(value):
                if isinstance(_v, dict):
                    _hydrated.append(NotationObject(_v, self._depth, **self._kwargs))
                elif isinstance(_v, list):
                    _hydrated.append(NotationArray(_v, self._depth, **self._kwargs))
                else:
                    _hydrated.append(NotationPrimitive(_v, self._depth, **self._kwargs))

            self._hydrated_value = _hydrated
        else:
            # self._value = NotationValue(None)
            _warning: str = (f"The `{self.__class__.__name__}` class does not support type '{type(value).__name__}'. "
                             f"`None` value and `NoneType` returned instead.")
            warnings.warn(_warning)

    def __getattr__(self, key: str) -> NotationPrimitive:
        """
        Not implemented for arrays.

        Parameters:
            key (str):

        Returns:
            NotationPrimitive
        """
        self._print_debug('Get', key)
        return NotationPrimitive(None, self._depth, **self._kwargs)

    def __getitem__(self, index: int) -> Union[NotationObject, Self, NotationPrimitive]:
        """
        Get child element by index.

        Parameters:
            index (int):

        Returns:
            Union[NotationObject, NotationArray, NotationPrimitive]
        """
        self._print_debug('Slice', index)

        try:
            return self._hydrated_value[int(index)]
        except IndexError:
            print('index error')
            return NotationPrimitive(None, self._depth, **self._kwargs)
        except TypeError:
            print('type error')
            return NotationPrimitive(None, self._depth, **self._kwargs)
        except ValueError:
            print('value error')
            return NotationPrimitive(None, self._depth, **self._kwargs)


if __name__ == '__main__':
    pass
