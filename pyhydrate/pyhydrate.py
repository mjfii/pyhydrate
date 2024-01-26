from typing import Union
from .notation import NotationValue
from .notation import NotationArray
from .notation import NotationObject
from .notation import NotationRepresentation


class PyHydrate(NotationRepresentation):
    """
    A class
    """

    _structure: Union[NotationArray, NotationObject, NotationValue, None] = None
    _root_type: Union[type, None] = None

    def __init__(self, source_value: Union[dict, list, str, None], debug: bool = False):
        """

        :param source_value:
        """

        if isinstance(source_value, list):
            self._root_type = list
            self._structure = NotationArray(source_value, 0)
        elif isinstance(source_value, dict):
            self._root_type = dict
            self._structure = NotationObject(source_value, 0)
        else:
            self._root_type = type(None)
            self._structure = NotationValue(None, 0)

    def __getattr__(self, key: str):
        return getattr(self._structure, key)

    def __getitem__(self, index: Union[int, None]):
        return self._structure[index]


if __name__ == '__main__':
    pass
