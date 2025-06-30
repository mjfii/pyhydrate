import json
import unittest
import warnings
from pathlib import Path

import pyhydrate as pyhy


class CallMethods(unittest.TestCase):
    _data = pyhy.PyHydrate(
        json.loads(Path("./pyhydrate/data/basic-dict-get.json").read_text()), debug=True
    )

    def test_yaml_string(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_integer("yaml") == "int: 1"

    def test_type(self) -> None:
        print("\n")
        assert self._data.level_one.level_two.level_3.test_integer("type") is int

    def test_json_string(self) -> None:
        print("\n")
        assert (
            self._data.level_one.level_two.level_3("json")
            == '{\n   "test_string": "test string",\n   "test_integer": 1,\n   "test_float": 2.345,\n   "test_bool": true\n}'
        )

    def test_invalid_call_type_warning(self) -> None:
        """Test that invalid call types issue a warning."""
        print("\n")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = self._data.level_one.level_two.level_3.test_integer("invalid_call")

            # Check that warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "Call type failed with str" in str(w[0].message)
            assert "invalid_call" in str(w[0].message)
            assert (
                "Valid options are: value, element, type, depth, map, json, yaml"
                in str(w[0].message)
            )

            # Check that None is returned
            assert result is None

    def test_invalid_call_type_warning_on_structure(self) -> None:
        """Test that invalid call types issue a warning on structure objects."""
        print("\n")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = self._data.level_one.level_two.level_3("bad_call")

            # Check that warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "Call type failed with str" in str(w[0].message)
            assert "bad_call" in str(w[0].message)
            assert (
                "Valid options are: value, element, type, depth, map, json, yaml"
                in str(w[0].message)
            )

            # Check that None is returned
            assert result is None


if __name__ == "__main__":
    unittest.main()
