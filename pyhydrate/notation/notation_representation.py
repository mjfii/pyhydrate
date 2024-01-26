from typing import Union
import textwrap
import json


class NotationRepresentation(object):
    # CONSTANTS

    _repr_key: str = 'PyHydrate'
    _idk: str = r'¯\_(ツ)_/¯'

    def __repr__(self) -> Union[str, None]:
        try:
            _working_value: Union[str, None] = self.__dict__.get('_raw_value', None)
        except AttributeError:
            return f"{self._repr_key}(None)"

        if not _working_value:
            try:
                _working_value = self.__dict__.get('_structure').__dict__.get('_raw_value', None)
            except AttributeError:
                return f"{self._repr_key}(None)"

        if _working_value:
            if isinstance(_working_value, str):
                return f"{self._repr_key}('{_working_value}')"
            elif (isinstance(_working_value, bool) or
                  isinstance(_working_value, float) or
                  isinstance(_working_value, int)):
                return f"{self._repr_key}({_working_value})"
            elif isinstance(_working_value, dict) or isinstance(_working_value, list):
                _return_value = textwrap.indent(json.dumps(_working_value, indent=3), 3 * ' ')
                return f"{self._repr_key}(\n{_return_value}\n)"
            else:
                return f"{self._repr_key}('{self._idk}')"
        else:
            return f"{self._repr_key}(None)"
