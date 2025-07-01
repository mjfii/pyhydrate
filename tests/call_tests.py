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

    def test_toml_string(self) -> None:
        """Test TOML string serialization of primitive values."""
        print("\n")
        result = self._data.level_one.level_two.level_3.test_integer("toml")
        assert "int = 1" in result

    def test_toml_string_primitive(self) -> None:
        """Test TOML serialization of string primitive."""
        print("\n")
        result = self._data.level_one.level_two.level_3.test_string("toml")
        assert 'str = "test string"' in result

    def test_toml_structure(self) -> None:
        """Test TOML string serialization of dict structures."""
        print("\n")
        result = self._data.level_one.level_two.level_3("toml")
        # Should contain all the keys from the nested structure
        assert "test_string" in result
        assert "test_integer = 1" in result
        assert "test_float = 2.345" in result
        assert "test_bool = true" in result

    def test_toml_list_wrapped(self) -> None:
        """Test TOML serialization wraps lists in root table."""
        print("\n")
        array_data = pyhy.PyHydrate([1, 2, 3])
        result = array_data("toml")
        # Lists should be wrapped in a 'data' key for TOML compatibility
        assert "data = [" in result
        assert "1" in result
        assert "2" in result
        assert "3" in result

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
                "Valid options are: value, element, type, depth, map, json, yaml, toml"
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
                "Valid options are: value, element, type, depth, map, json, yaml, toml"
                in str(w[0].message)
            )

            # Check that None is returned
            assert result is None

    def test_map_call_on_object(self) -> None:
        """Test that map call returns key mappings for objects."""
        print("\n")
        result = self._data.level_one("map")

        # Should return a dictionary with key mappings
        assert isinstance(result, dict)
        # Should have the mapped key for level_two
        assert "level_two" in result
        assert result["level_two"] == "levelTWO"

    def test_map_call_on_nested_object(self) -> None:
        """Test that map call works on nested objects."""
        print("\n")
        result = self._data.level_one.level_two.level_3("map")

        # Should return a dictionary with key mappings
        assert isinstance(result, dict)
        # Should have mapped keys for the nested structure
        expected_mappings = {
            "test_string": "TestString",
            "test_integer": "testInteger",
            "test_float": "test_Float",
            "test_bool": "Test_BOOL",
        }
        for clean_key, original_key in expected_mappings.items():
            assert clean_key in result
            assert result[clean_key] == original_key

    def test_map_call_on_primitive(self) -> None:
        """Test that map call returns None for primitive values."""
        print("\n")
        result = self._data.level_one.level_two.level_3.test_integer("map")

        # Primitives should return None for map calls (wrapped in NotationPrimitive)
        from pyhydrate.notation.notation_primitive import NotationPrimitive

        assert isinstance(result, NotationPrimitive)
        assert result() is None

    def test_map_call_on_array(self) -> None:
        """Test that map call returns None for array values."""
        print("\n")
        # Create array data for testing
        array_data = pyhy.PyHydrate([1, 2, 3])
        result = array_data("map")

        # Arrays should return None for map calls (wrapped in NotationPrimitive)
        from pyhydrate.notation.notation_primitive import NotationPrimitive

        assert isinstance(result, NotationPrimitive)
        assert result() is None


if __name__ == "__main__":
    unittest.main()
