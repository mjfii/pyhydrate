from typing import Union
import json
import textwrap
import hashlib
from typing_extensions import Self
import yaml
import re


class YamlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


class PyHydrate(object):
    """
    A class
    """
    _raw_key: str = '_raw_key_'
    _cleaned_key: str = '_cleaned_key_'
    _hydrated_key: str = '_hydrated_key_'
    _pattern = re.compile(r'(?<!^)(?=[A-Z])')

    def __init__(self, raw_value: Union[dict, str, None]):
        """

        :param raw_value:
        """
        self.raw = raw_value

    def __getattr__(self, key: str) -> Union[str, None]:
        try:
            return self.__dict__[self._hydrated_key][key]
        except KeyError:
            try:
                return self.__dict__[key]
            except KeyError:
                return None

    def __str__(self) -> str:
        """

        :return:
        """
        return yaml.dump(self.__dict__[self._cleaned_key], sort_keys=False, Dumper=YamlDumper)

    def __repr__(self) -> str:
        _params: str = textwrap.indent(json.dumps(self.__dict__[self._raw_key], indent=3), 3 * ' ')
        return f"FunctionParameters(\n{_params}\n)"

    def __eq__(self, comparable: Self) -> bool:
        """

        :param comparable:
        :return:
        """
        if isinstance(comparable, PyHydrate):
            return self.hash == comparable.hash
        else:
            return False

    def _snake_case(self, camel_case: str) -> Union[str, None]:
        """
        Convert a camel or pascal case string to a lower case snake string.
        :param camel_case:
        :return: str or None
        """
        return self._pattern.sub('_', camel_case).lower().replace('-', '_')

    def _clean_raw(self, raw: dict) -> Union[dict, None]:
        """

        :return:
        """
        return {self._snake_case(k): self._clean_raw(v) if isinstance(v, dict) else v for k, v in raw.items()}

    @property
    def raw(self) -> Union[dict, None]:
        """

        :return:
        """
        try:
            return yaml.dump(self.__dict__[self._raw_key], sort_keys=False, Dumper=YamlDumper)
        except KeyError:
            return None

    @raw.setter
    def raw(self, value: Union[dict, None]):

        if isinstance(value, dict):
            _cleaned = self._clean_raw(value)
            _hydrated: dict = {}
            for _key, _value in _cleaned.items():
                if isinstance(_value, dict):
                    _hydrated[self._snake_case(_key)] = PyHydrate(_value)
                else:
                    _hydrated[self._snake_case(_key)] = _value

            self.__dict__[self._raw_key] = value
            self.__dict__[self._cleaned_key] = _cleaned
            self.__dict__[self._hydrated_key] = _hydrated
        else:
            self.__dict__[self._raw_key] = None
            self.__dict__[self._cleaned_key] = None
            self.__dict__[self._hydrated_key] = None

    @property
    def cleaned(self) -> Union[dict, None]:
        """

        :return:
        """
        try:
            return yaml.dump(self.__dict__[self._cleaned_key], sort_keys=False, Dumper=YamlDumper)
        except KeyError:
            return None

    @property
    def hash(self) -> str:
        """
        Provided unique MD5 hash
        :return: str
        """
        return hashlib.md5(json.dumps(dict(sorted(self.__dict__[self._cleaned_key].items()))).encode()).hexdigest()


if __name__ == '__main__':
    _payload = json.loads(open('../tests/complete-test-001.json', 'r').read())
    _cls = PyHydrate(_payload)
    print(_cls.hash)
    pass
