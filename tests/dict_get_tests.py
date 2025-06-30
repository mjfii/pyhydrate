import json
import unittest

import pyhydrate as pyhy


class DictReadMethods(unittest.TestCase):
    _data = pyhy.PyHydrate(
        json.loads(open("./pyhydrate/data/basic-dict-get.json").read()), debug=True
    )

    def test_string_lookup(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_string() == "test string"

    def test_integer_lookup(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_integer() == 1

    def test_float_lookup(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_float() == 2.345

    def test_bool_lookup(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_bool() is True


if __name__ == "__main__":
    unittest.main()
