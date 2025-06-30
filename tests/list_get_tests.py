import json
import unittest

import pyhydrate as pyhy


class DictReadMethods(unittest.TestCase):
    _data = pyhy.PyHydrate(
        json.loads(open("./pyhydrate/data/basic-list-get.json").read()), debug=True
    )

    def test_string_lookup(self) -> None:
        print("\n")
        assert " ".join(self._data[0]()) == "a set of strings"

    def test_integer_lookup(self) -> None:
        print("\n")
        assert sum(self._data[1]()) == 6

    def test_float_lookup(self) -> None:
        print("\n")
        assert self._data[2][3]() == -10.9876

    def test_bool_lookup(self) -> None:
        print("\n")
        assert self._data[3][1]() is False


if __name__ == "__main__":
    unittest.main()
