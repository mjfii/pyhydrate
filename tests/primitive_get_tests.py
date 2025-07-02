import unittest

import pyhydrate as pyhy


class PrimitiveReadMethods(unittest.TestCase):
    def test_string(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate("a string", debug=True)
        assert _data() == "a string"

    def test_int(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate(123, debug=True)
        assert _data() == 123

    def test_float(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate(456.7890, debug=True)
        assert _data() == 456.789

    def test_bool(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate(True, debug=True)
        assert _data() is True

    def test_none(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate(None, debug=True)
        assert _data() is None

    def test_dict(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate({}, debug=True)
        assert _data("yaml") == "{}"

    def test_list(self) -> None:
        print("\n")
        _data = pyhy.PyHydrate([], debug=True)
        assert _data("yaml") == "[]"
