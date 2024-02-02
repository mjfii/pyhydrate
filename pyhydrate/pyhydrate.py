from typing import Union
from .notation import NotationPrimitive
from .notation import NotationArray
from .notation import NotationObject
from .notation import NotationRepresentation


class PyHydrate(NotationRepresentation):
    """
    A class
    """

    # CLASS VARIABLES
    _root_type: Union[type, None] = None
    _structure: Union[NotationArray, NotationObject, NotationPrimitive, None] = None

    # MAGIC METHODS
    def __init__(self, source_value: Union[dict, list, str, None], **kwargs):
        """

        :param source_value:
        :param kwargs:
        """
        #
        self._debug = kwargs.get('debug', False)

        #
        if isinstance(source_value, list):
            self._root_type = list
            self._structure = NotationArray(source_value, 0, **kwargs)
        #
        elif isinstance(source_value, dict):
            self._root_type = dict
            self._structure = NotationObject(source_value, 0, **kwargs)
        #
        else:
            self._root_type = type(None)
            self._structure = NotationPrimitive(None, 0, **kwargs)

    def __str__(self) -> str:
        return self._structure.yaml()

    def __getattr__(self, key: str) -> Union[NotationArray, NotationObject, NotationPrimitive, None]:
        if self._debug:
            print(f">>> Root :: <{self.__class__.__name__}>")
        return getattr(self._structure, key)

    def __getitem__(self, index: Union[int, None]) -> Union[NotationArray, NotationObject, NotationPrimitive, None]:
        if self._debug:
            print(f"=> Root :: <{self.__class__.__name__}>")
        return self._structure[index]


if __name__ == '__main__':
    pass
