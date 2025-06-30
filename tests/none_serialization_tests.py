import json
import unittest

import pyhydrate as pyhy


class NoneSerializationTests(unittest.TestCase):
    """Test proper None handling in YAML and JSON serialization."""

    def test_none_value_yaml(self) -> None:
        """Test YAML serialization of direct None value."""
        test_none = pyhy.PyHydrate(None)
        result = test_none("yaml")
        assert result == "NoneType: null"

    def test_none_value_json(self) -> None:
        """Test JSON serialization of direct None value."""
        test_none = pyhy.PyHydrate(None)
        result = test_none("json")
        expected = json.dumps({"NoneType": None}, indent=3)
        assert result == expected

    def test_dict_with_none_values_yaml(self) -> None:
        """Test YAML serialization of dict containing None values."""
        test_data = {"key": None, "other": "value", "nested": {"inner": None}}
        test_dict = pyhy.PyHydrate(test_data)
        result = test_dict("yaml")

        # Should contain the None values properly serialized
        assert "key: null" in result
        assert "other: value" in result
        assert "inner: null" in result

    def test_dict_with_none_values_json(self) -> None:
        """Test JSON serialization of dict containing None values."""
        test_data = {"key": None, "other": "value"}
        test_dict = pyhy.PyHydrate(test_data)
        result = test_dict("json")

        # Parse back to verify structure
        parsed = json.loads(result)
        assert parsed["key"] is None
        assert parsed["other"] == "value"

    def test_list_with_none_values_yaml(self) -> None:
        """Test YAML serialization of list containing None values."""
        test_data = [None, "value", None, 42]
        test_list = pyhy.PyHydrate(test_data)
        result = test_list("yaml")

        # Should contain proper null representations
        assert "- null" in result
        assert "- value" in result
        assert "- 42" in result

    def test_list_with_none_values_json(self) -> None:
        """Test JSON serialization of list containing None values."""
        test_data = [None, "value", None]
        test_list = pyhy.PyHydrate(test_data)
        result = test_list("json")

        # Parse back to verify structure
        parsed = json.loads(result)
        assert len(parsed) == 3
        assert parsed[0] is None
        assert parsed[1] == "value"
        assert parsed[2] is None

    def test_missing_key_access_yaml(self) -> None:
        """Test YAML serialization when accessing non-existent dict key."""
        test_dict = pyhy.PyHydrate({"existing": "value"})
        missing = test_dict.missing_key
        result = missing("yaml")
        assert result == "NoneType: null"

    def test_missing_key_access_json(self) -> None:
        """Test JSON serialization when accessing non-existent dict key."""
        test_dict = pyhy.PyHydrate({"existing": "value"})
        missing = test_dict.missing_key
        result = missing("json")
        expected = json.dumps({"NoneType": None}, indent=3)
        assert result == expected

    def test_missing_array_index_yaml(self) -> None:
        """Test YAML serialization when accessing non-existent array index."""
        test_list = pyhy.PyHydrate(["item1", "item2"])
        missing = test_list[10]  # Out of bounds
        result = missing("yaml")
        assert result == "NoneType: null"

    def test_missing_array_index_json(self) -> None:
        """Test JSON serialization when accessing non-existent array index."""
        test_list = pyhy.PyHydrate(["item1", "item2"])
        missing = test_list[10]  # Out of bounds
        result = missing("json")
        expected = json.dumps({"NoneType": None}, indent=3)
        assert result == expected

    def test_primitive_attribute_access_yaml(self) -> None:
        """Test YAML serialization when accessing attribute on primitive."""
        test_string = pyhy.PyHydrate("hello")
        missing = test_string.some_attribute
        result = missing("yaml")
        assert result == "NoneType: null"

    def test_primitive_attribute_access_json(self) -> None:
        """Test JSON serialization when accessing attribute on primitive."""
        test_string = pyhy.PyHydrate("hello")
        missing = test_string.some_attribute
        result = missing("json")
        expected = json.dumps({"NoneType": None}, indent=3)
        assert result == expected

    def test_deeply_nested_none_yaml(self) -> None:
        """Test YAML serialization with deeply nested None values."""
        test_data = {"level1": {"level2": {"level3": None, "other": "value"}}}
        test_nested = pyhy.PyHydrate(test_data)
        result = test_nested.level1.level2.level3("yaml")
        assert result == "NoneType: null"

    def test_deeply_nested_none_json(self) -> None:
        """Test JSON serialization with deeply nested None values."""
        test_data = {"level1": {"level2": {"level3": None, "other": "value"}}}
        test_nested = pyhy.PyHydrate(test_data)
        result = test_nested.level1.level2.level3("json")
        expected = json.dumps({"NoneType": None}, indent=3)
        assert result == expected


if __name__ == "__main__":
    unittest.main()
