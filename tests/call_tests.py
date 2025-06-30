import json
import unittest

import pyhydrate as pyhy


class CallMethods(unittest.TestCase):
    _data = pyhy.PyHydrate(
        json.loads(open("./pyhydrate/data/basic-dict-get.json").read()), debug=True
    )

    def test_yaml_string(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_integer("yaml") == "int: 1"

    def test_type(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_integer("type") == int

    def test_json_string(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3("json") == '{\n   "test_string": "test string",\n   "test_integer": 1,\n   "test_float": 2.345,\n   "test_bool": true\n}'


if __name__ == "__main__":
    unittest.main()
