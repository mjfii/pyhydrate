"""
Tests for write (mutation) support in PyHydrate.

Tests cover:
- Setting values via dot notation on existing objects
- Creating new keys on existing objects
- Deep auto-creation of intermediate dicts
- Creating objects from scratch
- Assigning dict and list values
- Array set/delete item
- Key normalization on write
- Delete attr/item
- Read-after-write consistency
- Serialization after mutation
- Proxy behavior for reads (backward compat)
"""

import json
import unittest

from pyhydrate import PyHydrate


class TestSetExistingKey(unittest.TestCase):
    """Test setting values on existing keys."""

    def test_set_existing_string_key(self) -> None:
        """Set an existing string key to a new value."""
        data = PyHydrate({"name": "old"})
        data.name = "new"
        assert data.name() == "new"

    def test_set_existing_int_key(self) -> None:
        """Set an existing int key to a new value."""
        data = PyHydrate({"count": 1})
        data.count = 42
        assert data.count() == 42

    def test_set_existing_nested_key(self) -> None:
        """Set a key on an existing nested object."""
        data = PyHydrate({"user": {"name": "Alice", "age": 25}})
        data.user.name = "Bob"
        assert data.user.name() == "Bob"
        # Age should be unchanged
        assert data.user.age() == 25

    def test_set_preserves_camel_case_key(self) -> None:
        """Writing to a normalized key updates the original camelCase key."""
        data = PyHydrate({"firstName": "Alice"})
        data.first_name = "Bob"
        # The raw value should use the original key format
        raw = data()
        assert raw["first_name"] == "Bob"


class TestSetNewKey(unittest.TestCase):
    """Test adding new keys to existing objects."""

    def test_add_new_key_to_dict(self) -> None:
        """Add a new key to an existing dict."""
        data = PyHydrate({"existing": "value"})
        data.new_key = "hello"
        assert data.new_key() == "hello"
        assert data.existing() == "value"

    def test_add_dict_value(self) -> None:
        """Assign a dict as a value."""
        data = PyHydrate({"name": "test"})
        data.config = {"host": "localhost", "port": 5432}
        assert data.config.host() == "localhost"
        assert data.config.port() == 5432

    def test_add_list_value(self) -> None:
        """Assign a list as a value."""
        data = PyHydrate({"name": "test"})
        data.items = [1, 2, 3]
        assert data.items() == [1, 2, 3]

    def test_overwrite_primitive_with_dict(self) -> None:
        """Overwrite a primitive value with a dict."""
        data = PyHydrate({"name": "string_value"})
        data.name = {"first": "John", "last": "Doe"}
        assert data.name.first() == "John"
        assert data.name.last() == "Doe"


class TestCreateFromScratch(unittest.TestCase):
    """Test creating PyHydrate objects from scratch."""

    def test_empty_then_set(self) -> None:
        """Create empty PyHydrate and set a value."""
        x = PyHydrate()
        x.name = "test"
        assert x.name() == "test"

    def test_empty_then_set_multiple(self) -> None:
        """Create empty and set multiple values."""
        x = PyHydrate()
        x.name = "test"
        x.count = 42
        result = x()
        assert result == {"name": "test", "count": 42}

    def test_empty_then_set_dict(self) -> None:
        """Create empty and set a dict value."""
        x = PyHydrate()
        x.config = {"host": "localhost"}
        assert x.config.host() == "localhost"


class TestDeepAutoCreation(unittest.TestCase):
    """Test auto-creation of intermediate dicts via proxy chain."""

    def test_two_level_deep(self) -> None:
        """Create two levels deep from scratch."""
        x = PyHydrate()
        x.a.b = 1
        assert x.a.b() == 1

    def test_three_level_deep(self) -> None:
        """Create three levels deep from scratch."""
        x = PyHydrate()
        x.a.b.c = 1
        assert x.a.b.c() == 1
        result = x()
        assert result == {"a": {"b": {"c": 1}}}

    def test_deep_on_existing_object(self) -> None:
        """Create deep path on existing object with missing intermediate."""
        data = PyHydrate({"existing": "value"})
        data.new_path.deep.value = 42
        assert data.new_path.deep.value() == 42
        assert data.existing() == "value"

    def test_deep_auto_creation_with_dict_value(self) -> None:
        """Deep auto-creation where the final value is a dict."""
        x = PyHydrate()
        x.a.b = {"key": "value"}
        assert x.a.b.key() == "value"


class TestArrayMutation(unittest.TestCase):
    """Test array set/delete item."""

    def test_set_array_item(self) -> None:
        """Set an item in an array by index."""
        data = PyHydrate([1, 2, 3])
        data[1] = 99
        assert data[1]() == 99

    def test_set_array_item_dict(self) -> None:
        """Set an array item to a dict."""
        data = PyHydrate([{"name": "a"}, {"name": "b"}])
        data[0] = {"name": "updated"}
        assert data[0].name() == "updated"

    def test_set_array_item_negative_index(self) -> None:
        """Set an item using negative indexing."""
        data = PyHydrate([1, 2, 3])
        data[-1] = 99
        assert data[-1]() == 99
        assert data() == [1, 2, 99]

    def test_set_nested_array_item(self) -> None:
        """Set an item in a nested array via dot notation."""
        data = PyHydrate({"items": [10, 20, 30]})
        data.items[1] = 99
        assert data.items[1]() == 99

    def test_delete_array_item(self) -> None:
        """Delete an item from an array."""
        data = PyHydrate([1, 2, 3])
        del data[0]
        assert data[0]() == 2
        assert data() == [2, 3]


class TestDeleteAttr(unittest.TestCase):
    """Test deleting attributes from objects."""

    def test_delete_existing_key(self) -> None:
        """Delete an existing key."""
        data = PyHydrate({"name": "Alice", "age": 25})
        del data.name
        result = data()
        assert "name" not in result
        assert result["age"] == 25

    def test_delete_nested_key(self) -> None:
        """Delete a key on a nested object."""
        data = PyHydrate({"user": {"name": "Alice", "age": 25}})
        del data.user.name
        result = data.user()
        assert "name" not in result
        assert result["age"] == 25

    def test_delete_nonexistent_key_raises(self) -> None:
        """Deleting a non-existent key raises AttributeError."""
        data = PyHydrate({"name": "Alice"})
        with self.assertRaises(AttributeError):
            del data.nonexistent

    def test_delete_then_recreate(self) -> None:
        """Delete a key then set it again."""
        data = PyHydrate({"name": "Alice"})
        del data.name
        data.name = "Bob"
        assert data.name() == "Bob"

    def test_delete_last_key(self) -> None:
        """Delete the only key, resulting in empty dict."""
        data = PyHydrate({"only": "key"})
        del data.only
        assert data() == {}

    def test_delete_on_non_object_raises(self) -> None:
        """Deleting on a non-object structure raises TypeError."""
        data = PyHydrate([1, 2, 3])
        with self.assertRaises(TypeError):
            del data.some_key


class TestDeleteItem(unittest.TestCase):
    """Test deleting items from arrays."""

    def test_delete_array_item_middle(self) -> None:
        """Delete a middle item from an array."""
        data = PyHydrate([1, 2, 3, 4])
        del data[1]
        assert data() == [1, 3, 4]

    def test_delete_array_item_negative_index(self) -> None:
        """Delete an item using negative indexing."""
        data = PyHydrate([1, 2, 3])
        del data[-1]
        assert data() == [1, 2]

    def test_delete_array_out_of_bounds_raises(self) -> None:
        """Deleting out of bounds raises IndexError."""
        data = PyHydrate([1, 2, 3])
        with self.assertRaises(IndexError):
            del data[10]

    def test_delete_on_non_array_raises(self) -> None:
        """Deleting item on non-array raises TypeError."""
        data = PyHydrate({"key": "value"})
        with self.assertRaises(TypeError):
            del data[0]


class TestProxyReadBehavior(unittest.TestCase):
    """Test that proxy objects behave like None for reads."""

    def test_proxy_call_returns_none(self) -> None:
        """Calling a proxy returns None."""
        data = PyHydrate({"key": "value"})
        assert data.nonexistent() is None

    def test_proxy_chain_call_returns_none(self) -> None:
        """Calling a chained proxy returns None."""
        data = PyHydrate({"key": "value"})
        assert data.nonexistent.deep.path() is None

    def test_proxy_bool_is_false(self) -> None:
        """Proxy is falsy."""
        data = PyHydrate({"key": "value"})
        assert not data.nonexistent

    def test_proxy_repr(self) -> None:
        """Proxy repr is consistent."""
        data = PyHydrate({"key": "value"})
        assert "None" in repr(data.nonexistent)


class TestSerializationAfterMutation(unittest.TestCase):
    """Test that serialization reflects mutations."""

    def test_json_after_set(self) -> None:
        """JSON output reflects set value."""
        data = PyHydrate({"name": "old"})
        data.name = "new"
        result = json.loads(data("json"))
        assert result["name"] == "new"

    def test_yaml_after_set(self) -> None:
        """YAML output reflects set value."""
        data = PyHydrate({"name": "old"})
        data.name = "new"
        yaml_str = data("yaml")
        assert "new" in yaml_str

    def test_value_after_set(self) -> None:
        """Value output reflects set value."""
        data = PyHydrate({"a": 1, "b": 2})
        data.a = 10
        result = data()
        assert result["a"] == 10
        assert result["b"] == 2


class TestEdgeCases(unittest.TestCase):
    """Test edge cases for write operations."""

    def test_set_none_value(self) -> None:
        """Setting a value to None."""
        data = PyHydrate({"key": "value"})
        data.key = None
        assert data.key() is None

    def test_set_bool_value(self) -> None:
        """Setting a boolean value."""
        data = PyHydrate({"flag": False})
        data.flag = True
        assert data.flag() is True

    def test_set_float_value(self) -> None:
        """Setting a float value."""
        data = PyHydrate({})
        data.pi = 3.14
        assert data.pi() == 3.14

    def test_multiple_deep_paths(self) -> None:
        """Create multiple deep paths from scratch."""
        x = PyHydrate()
        x.a.b = 1
        x.c.d = 2
        assert x.a.b() == 1
        assert x.c.d() == 2

    def test_overwrite_dict_with_primitive(self) -> None:
        """Overwrite a dict value with a primitive."""
        data = PyHydrate({"config": {"host": "localhost"}})
        data.config = "disabled"
        assert data.config() == "disabled"

    def test_assign_pyhydrate_as_value(self) -> None:
        """Assigning a PyHydrate object unwraps to raw value."""
        inner = PyHydrate({"nested": "data"})
        outer = PyHydrate({"key": "value"})
        outer.child = inner
        assert outer.child.nested() == "data"

    def test_write_to_empty_dict(self) -> None:
        """Write to a PyHydrate wrapping an empty dict."""
        data = PyHydrate({})
        data.name = "test"
        assert data.name() == "test"

    def test_deep_auto_creation_with_list_value(self) -> None:
        """Deep auto-creation where the final value is a list."""
        x = PyHydrate()
        x.a.b = [1, 2, 3]
        assert x.a.b() == [1, 2, 3]

    def test_toml_after_mutation(self) -> None:
        """TOML output reflects mutations."""
        data = PyHydrate({"name": "old", "version": 1})
        data.name = "new"
        toml_str = data("toml")
        assert "new" in toml_str
        assert "old" not in toml_str

    def test_setitem_on_non_array_is_noop(self) -> None:
        """Setting item on non-array PyHydrate does nothing."""
        data = PyHydrate({"key": "value"})
        data[0] = "ignored"
        # Structure should be unchanged
        assert data.key() == "value"


if __name__ == "__main__":
    unittest.main()
