import json
from json import JSONDecodeError
import yaml
from typing import Union
from .notation import NotationPrimitive
from .notation import NotationArray
from .notation import NotationObject
from .notation import NotationRepresentation


class PyHydrate(NotationRepresentation):

    # CLASS VARIABLES
    _root_type: Union[type, None] = None
    _structure: Union[NotationArray, NotationObject, NotationPrimitive, None] = None

    # INTERNAL METHODS
    def _print_root(self):
        if self._debug:
            print(f">>> Root :: <{self.__class__.__name__}>")

    # MAGIC METHODS
    def __init__(self, source_value: Union[dict, list, str, int, float, bool, None], **kwargs) -> None:

        #
        self._debug = kwargs.get('debug', False)

        # try to translate string to json, if we fail, just quit attempt
        if isinstance(source_value, str):
            try:
                source_value = json.loads(source_value)
            except JSONDecodeError:
                pass

        # if we still have a string, try to translate as if it were yaml
        if isinstance(source_value, str):
            source_value = yaml.safe_load(source_value)

        #
        if isinstance(source_value, dict):
            self._root_type = dict
            self._structure = NotationObject(source_value, 0, **kwargs)
        #
        elif isinstance(source_value, list):
            self._root_type = list
            self._structure = NotationArray(source_value, 0, **kwargs)
        #
        elif (isinstance(source_value, int) or isinstance(source_value, float)
              or isinstance(source_value, bool) or isinstance(source_value, str)):
            self._root_type = type(source_value)
            self._structure = NotationPrimitive(source_value, 0, **kwargs)
        #
        elif isinstance(source_value, type(None)):
            self._root_type = type(None)
            self._structure = NotationPrimitive(None, 0, **kwargs)
        else:
            self._root_type = type(None)
            self._structure = None

    def __str__(self) -> str:
        self._print_root()
        return self._structure('yaml')

    def __getattr__(self, key: str) -> Union[NotationArray, NotationObject, NotationPrimitive, None]:
        self._print_root()
        return getattr(self._structure, key)

    def __getitem__(self, index: Union[int, None]) -> Union[NotationArray, NotationObject, NotationPrimitive, None]:
        self._print_root()
        return self._structure[index]

    def __call__(self, *args, **kwargs) -> Union[dict, list, str, int, float, bool, type, None]:
        self._print_root()
        try:
            return self._structure(args[0])
        except IndexError:
            return self._structure()


if __name__ == '__main__':
    pass
