"""
Test cases for PyHydrate initialization with different data types.
"""

import unittest
from pathlib import Path

from pyhydrate import PyHydrate


class InitializationTests(unittest.TestCase):
    """Test PyHydrate initialization with various data types."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_data_path = Path(__file__).parent.parent / "pyhydrate" / "data"

        # Expected data structure for all format tests
        self.expected_data = {
            "name": "John Doe",
            "age": 30,
            "city": "New York",
            "isActive": True,
            "balance": 1234.56,
            "settings": {"theme": "dark", "notifications": True, "privacy_level": 2},
            "hobbies": ["reading", "swimming", "coding"],
        }

    def test_init_with_dict(self) -> None:
        """Test initialization with a Python dict."""
        data = PyHydrate(self.expected_data)

        assert data.name() == "John Doe"
        assert data.age() == 30
        assert data.settings.theme() == "dark"
        assert data.hobbies[0]() == "reading"

    def test_init_with_list(self) -> None:
        """Test initialization with a Python list."""
        test_list = ["apple", "banana", "cherry", 42, True]
        data = PyHydrate(test_list)

        assert data[0]() == "apple"
        assert data[1]() == "banana"
        assert data[3]() == 42
        assert data[4]() is True

    def test_init_with_string_primitive(self) -> None:
        """Test initialization with a string primitive."""
        data = PyHydrate("hello world")

        assert data() == "hello world"
        assert data("type") is str

    def test_init_with_int_primitive(self) -> None:
        """Test initialization with an integer primitive."""
        data = PyHydrate(42)

        assert data() == 42
        assert data("type") is int

    def test_init_with_float_primitive(self) -> None:
        """Test initialization with a float primitive."""
        data = PyHydrate(3.14159)

        assert data() == 3.14159
        assert data("type") is float

    def test_init_with_bool_primitive(self) -> None:
        """Test initialization with a boolean primitive."""
        data = PyHydrate(True)

        assert data() is True
        assert data("type") is bool

    def test_init_with_none_primitive(self) -> None:
        """Test initialization with None."""
        data = PyHydrate(None)

        assert data() is None
        assert data("type") is type(None)

    def test_init_with_json_string(self) -> None:
        """Test initialization with a JSON string."""
        json_data = self.test_data_path / "init-test-data.json"
        json_string = json_data.read_text()
        data = PyHydrate(json_string)

        assert data.name() == "John Doe"
        assert data.age() == 30
        assert data.settings.theme() == "dark"
        assert data.hobbies[0]() == "reading"

    def test_init_with_yaml_string(self) -> None:
        """Test initialization with a YAML string."""
        yaml_data = self.test_data_path / "init-test-data.yaml"
        yaml_string = yaml_data.read_text()
        data = PyHydrate(yaml_string)

        assert data.name() == "John Doe"
        assert data.age() == 30
        assert data.settings.theme() == "dark"
        assert data.hobbies[0]() == "reading"

    def test_init_with_toml_string(self) -> None:
        """Test initialization with a TOML string."""
        toml_data = self.test_data_path / "init-test-data.toml"
        toml_string = toml_data.read_text()
        data = PyHydrate(toml_string)

        assert data.name() == "John Doe"
        assert data.age() == 30
        assert data.settings.theme() == "dark"
        assert data.hobbies[0]() == "reading"

    def test_json_yaml_toml_equivalence(self) -> None:
        """Test that JSON, YAML, and TOML strings produce equivalent data structures."""
        json_data = self.test_data_path / "init-test-data.json"
        yaml_data = self.test_data_path / "init-test-data.yaml"
        toml_data = self.test_data_path / "init-test-data.toml"

        json_hydrate = PyHydrate(json_data.read_text())
        yaml_hydrate = PyHydrate(yaml_data.read_text())
        toml_hydrate = PyHydrate(toml_data.read_text())

        # Test key fields for equivalence
        assert json_hydrate.name() == yaml_hydrate.name()
        assert yaml_hydrate.name() == toml_hydrate.name()

        assert json_hydrate.age() == yaml_hydrate.age()
        assert yaml_hydrate.age() == toml_hydrate.age()

        assert json_hydrate.settings.theme() == yaml_hydrate.settings.theme()
        assert yaml_hydrate.settings.theme() == toml_hydrate.settings.theme()

    def test_invalid_json_fallback_to_yaml(self) -> None:
        """Test that invalid JSON falls back to YAML parsing."""
        # This is valid YAML but invalid JSON
        yaml_only_string = """
        name: John
        age: 30
        active: yes
        """
        data = PyHydrate(yaml_only_string)

        assert data.name() == "John"
        assert data.age() == 30
        assert data.active() is True  # YAML 'yes' -> True

    def test_invalid_formats_remain_string(self) -> None:
        """Test that strings that aren't valid JSON, TOML, or YAML remain as strings."""
        invalid_string = "This is just a plain string with no format"
        data = PyHydrate(invalid_string)

        assert data() == invalid_string
        assert data("type") is str

    def test_complex_nested_structure(self) -> None:
        """Test initialization with deeply nested structures."""
        complex_data = {
            "level-one": {
                "level-two": {
                    "level-three": {
                        "items": [
                            {"name": "item1", "value": 100},
                            {"name": "item2", "value": 200},
                        ]
                    }
                }
            }
        }
        data = PyHydrate(complex_data)

        assert data.level_one.level_two.level_three.items[0].name() == "item1"
        assert data.level_one.level_two.level_three.items[1].value() == 200

    def test_mixed_data_types_in_list(self) -> None:
        """Test initialization with lists containing mixed data types."""
        mixed_list = [
            "string",
            42,
            3.14,
            True,
            None,
            {"nested": "dict"},
            ["nested", "list"],
        ]
        data = PyHydrate(mixed_list)

        assert data[0]() == "string"
        assert data[1]() == 42
        assert data[2]() == 3.14
        assert data[3]() is True
        assert data[4]() is None
        assert data[5].nested() == "dict"
        assert data[6][0]() == "nested"


if __name__ == "__main__":
    unittest.main()
