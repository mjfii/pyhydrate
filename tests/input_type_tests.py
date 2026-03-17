"""
Test cases for PyHydrate handling of unsupported and convertible input types (Issue #1).

Covers:
- Conversion of set, frozenset, tuple, range to list
- ImmutableConversionWarning for tuple and frozenset
- TypeError for truly unsupported types (bytes, complex, custom classes, etc.)
- Edge cases: empty collections, nested structures, serialization, mutation
"""

import json
import unittest
import warnings

from pyhydrate import PyHydrate
from pyhydrate.exceptions import ImmutableConversionWarning


class TestSetConversion(unittest.TestCase):
    """Test that set inputs are converted to lists."""

    def test_set_converted_to_list(self) -> None:
        """Test that a set is converted to a list."""
        data = PyHydrate({1, 2, 3})
        result = data()
        assert isinstance(result, list)
        assert sorted(result) == [1, 2, 3]

    def test_empty_set_converted_to_empty_list(self) -> None:
        """Test that an empty set becomes an empty list."""
        data = PyHydrate(set())
        result = data()
        assert isinstance(result, list)
        assert result == []

    def test_set_with_mixed_types(self) -> None:
        """Test set with mixed hashable types."""
        data = PyHydrate({1, "two", 3.5, None})
        result = data()
        assert isinstance(result, list)
        assert len(result) == 4
        assert 1 in result
        assert "two" in result
        assert 3.5 in result
        assert None in result

    def test_set_no_immutable_warning(self) -> None:
        """Test that mutable set does NOT trigger ImmutableConversionWarning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate({1, 2, 3})
            immutable_warnings = [
                x for x in w if issubclass(x.category, ImmutableConversionWarning)
            ]
            assert len(immutable_warnings) == 0

    def test_set_elements_accessible_by_index(self) -> None:
        """Test that converted set elements are accessible via bracket notation."""
        data = PyHydrate({"only"})
        assert data[0]() == "only"


class TestFrozensetConversion(unittest.TestCase):
    """Test that frozenset inputs are converted to lists with a warning."""

    def test_frozenset_converted_to_list(self) -> None:
        """Test that a frozenset is converted to a list."""
        data = PyHydrate(frozenset(["a", "b", "c"]))
        result = data()
        assert isinstance(result, list)
        assert sorted(result) == ["a", "b", "c"]

    def test_empty_frozenset_converted_to_empty_list(self) -> None:
        """Test that an empty frozenset becomes an empty list."""
        data = PyHydrate(frozenset())
        result = data()
        assert isinstance(result, list)
        assert result == []

    def test_frozenset_warns_immutable(self) -> None:
        """Test that frozenset input triggers ImmutableConversionWarning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate(frozenset([1, 2]))
            immutable_warnings = [
                x for x in w if issubclass(x.category, ImmutableConversionWarning)
            ]
            assert len(immutable_warnings) == 1
            assert "frozenset" in str(immutable_warnings[0].message)
            assert "mutable" in str(immutable_warnings[0].message)

    def test_frozenset_warning_message_content(self) -> None:
        """Test the full frozenset warning message is informative."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate(frozenset([1]))
            msg = str(w[0].message)
            assert "Immutable type" in msg
            assert "'frozenset'" in msg
            assert "converted to a mutable list" in msg


class TestTupleConversion(unittest.TestCase):
    """Test that tuple inputs are converted to lists with a warning."""

    def test_tuple_converted_to_list(self) -> None:
        """Test that a tuple is converted to a list."""
        data = PyHydrate((1, "two", 3.0))
        result = data()
        assert isinstance(result, list)
        assert result == [1, "two", 3.0]

    def test_empty_tuple_converted_to_empty_list(self) -> None:
        """Test that an empty tuple becomes an empty list."""
        data = PyHydrate(())
        result = data()
        assert isinstance(result, list)
        assert result == []

    def test_tuple_preserves_order(self) -> None:
        """Test that tuple conversion preserves element order."""
        data = PyHydrate(("z", "a", "m"))
        assert data[0]() == "z"
        assert data[1]() == "a"
        assert data[2]() == "m"

    def test_tuple_warns_immutable(self) -> None:
        """Test that tuple input triggers ImmutableConversionWarning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate((1, 2, 3))
            immutable_warnings = [
                x for x in w if issubclass(x.category, ImmutableConversionWarning)
            ]
            assert len(immutable_warnings) == 1
            assert "tuple" in str(immutable_warnings[0].message)
            assert "mutable" in str(immutable_warnings[0].message)

    def test_tuple_warning_message_content(self) -> None:
        """Test the full tuple warning message is informative."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate((1, 2))
            msg = str(w[0].message)
            assert "Immutable type" in msg
            assert "'tuple'" in msg
            assert "converted to a mutable list" in msg

    def test_nested_dicts_in_tuple(self) -> None:
        """Test that tuples containing dicts are properly hydrated."""
        data = PyHydrate(({"name": "Alice"}, {"name": "Bob"}))
        assert data[0].name() == "Alice"
        assert data[1].name() == "Bob"

    def test_nested_lists_in_tuple(self) -> None:
        """Test that tuples containing lists are properly hydrated."""
        data = PyHydrate(([1, 2], [3, 4]))
        assert data[0][0]() == 1
        assert data[1][1]() == 4

    def test_single_element_tuple(self) -> None:
        """Test that a single-element tuple is converted properly."""
        data = PyHydrate((42,))
        result = data()
        assert isinstance(result, list)
        assert result == [42]
        assert data[0]() == 42


class TestRangeConversion(unittest.TestCase):
    """Test that range inputs are converted to lists."""

    def test_range_converted_to_list(self) -> None:
        """Test that a range is converted to a list."""
        data = PyHydrate(range(5))
        result = data()
        assert isinstance(result, list)
        assert result == [0, 1, 2, 3, 4]

    def test_empty_range_converted_to_empty_list(self) -> None:
        """Test that an empty range becomes an empty list."""
        data = PyHydrate(range(0))
        result = data()
        assert isinstance(result, list)
        assert result == []

    def test_range_with_start_stop(self) -> None:
        """Test range with start and stop arguments."""
        data = PyHydrate(range(2, 6))
        assert data() == [2, 3, 4, 5]

    def test_range_with_step(self) -> None:
        """Test range with step argument."""
        data = PyHydrate(range(0, 10, 3))
        assert data() == [0, 3, 6, 9]

    def test_range_no_immutable_warning(self) -> None:
        """Test that range does NOT trigger ImmutableConversionWarning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate(range(3))
            immutable_warnings = [
                x for x in w if issubclass(x.category, ImmutableConversionWarning)
            ]
            assert len(immutable_warnings) == 0

    def test_range_elements_accessible_by_index(self) -> None:
        """Test that converted range elements are accessible via bracket notation."""
        data = PyHydrate(range(3))
        assert data[0]() == 0
        assert data[1]() == 1
        assert data[2]() == 2


class TestConvertedTypeSerialization(unittest.TestCase):
    """Test that converted types serialize correctly to JSON and YAML."""

    def test_tuple_to_json(self) -> None:
        """Test JSON serialization of a converted tuple."""
        data = PyHydrate((1, 2, 3))
        result = data("json")
        parsed = json.loads(result)
        assert parsed == [1, 2, 3]

    def test_tuple_to_yaml(self) -> None:
        """Test YAML serialization of a converted tuple."""
        data = PyHydrate(("a", "b"))
        result = data("yaml")
        assert "a" in result
        assert "b" in result

    def test_set_to_json(self) -> None:
        """Test JSON serialization of a converted set."""
        data = PyHydrate({"only"})
        result = data("json")
        parsed = json.loads(result)
        assert parsed == ["only"]

    def test_range_to_json(self) -> None:
        """Test JSON serialization of a converted range."""
        data = PyHydrate(range(3))
        result = data("json")
        parsed = json.loads(result)
        assert parsed == [0, 1, 2]

    def test_frozenset_to_json(self) -> None:
        """Test JSON serialization of a converted frozenset."""
        data = PyHydrate(frozenset([42]))
        result = data("json")
        parsed = json.loads(result)
        assert parsed == [42]


class TestConvertedTypeMutation(unittest.TestCase):
    """Test that converted types support mutation after conversion."""

    def test_tuple_mutation_via_setitem(self) -> None:
        """Test that a converted tuple supports element assignment."""
        data = PyHydrate((10, 20, 30))
        data[1] = 99
        assert data[1]() == 99

    def test_tuple_deletion_via_delitem(self) -> None:
        """Test that a converted tuple supports element deletion."""
        data = PyHydrate((10, 20, 30))
        del data[1]
        result = data()
        assert result == [10, 30]

    def test_range_mutation_via_setitem(self) -> None:
        """Test that a converted range supports element assignment."""
        data = PyHydrate(range(3))
        data[0] = 100
        assert data[0]() == 100


class TestWarningFilterability(unittest.TestCase):
    """Test that ImmutableConversionWarning can be filtered by category."""

    def test_warning_is_subclass_of_pyhydrate_warning(self) -> None:
        """Test warning class hierarchy for filtering."""
        from pyhydrate.exceptions import PyHydrateWarning

        assert issubclass(ImmutableConversionWarning, PyHydrateWarning)
        assert issubclass(ImmutableConversionWarning, UserWarning)

    def test_warning_can_be_suppressed(self) -> None:
        """Test that users can suppress the warning via standard warnings filter."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("ignore", ImmutableConversionWarning)
            PyHydrate((1, 2, 3))
            assert len(w) == 0

    def test_warning_stacklevel_points_to_caller(self) -> None:
        """Test that the warning points to the caller's code, not internals."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            PyHydrate((1,))
            assert len(w) == 1
            # The warning filename should be this test file, not pyhydrate.py
            assert "input_type_tests.py" in w[0].filename


class TestUnsupportedInputTypes(unittest.TestCase):
    """Test that unsupported types raise TypeError."""

    def test_custom_class_raises_type_error(self) -> None:
        """Test that a custom class instance raises TypeError."""

        class MyClass:
            pass

        with self.assertRaises(TypeError) as ctx:
            PyHydrate(MyClass())
        assert "MyClass" in str(ctx.exception)
        assert "does not support" in str(ctx.exception)

    def test_bytes_raises_type_error(self) -> None:
        """Test that bytes raises TypeError."""
        with self.assertRaises(TypeError) as ctx:
            PyHydrate(b"hello")
        assert "bytes" in str(ctx.exception)

    def test_bytearray_raises_type_error(self) -> None:
        """Test that bytearray raises TypeError."""
        with self.assertRaises(TypeError) as ctx:
            PyHydrate(bytearray(b"hello"))
        assert "bytearray" in str(ctx.exception)

    def test_complex_raises_type_error(self) -> None:
        """Test that complex numbers raise TypeError."""
        with self.assertRaises(TypeError) as ctx:
            PyHydrate(complex(1, 2))
        assert "complex" in str(ctx.exception)

    def test_lambda_raises_type_error(self) -> None:
        """Test that a lambda/function raises TypeError."""
        with self.assertRaises(TypeError):
            PyHydrate(lambda x: x)

    def test_generator_raises_type_error(self) -> None:
        """Test that a generator raises TypeError."""
        gen = (x for x in range(3))
        with self.assertRaises(TypeError) as ctx:
            PyHydrate(gen)
        assert "generator" in str(ctx.exception)

    def test_module_raises_type_error(self) -> None:
        """Test that a module raises TypeError."""
        import sys

        with self.assertRaises(TypeError):
            PyHydrate(sys)

    def test_type_error_message_lists_supported_types(self) -> None:
        """Test that TypeError message includes supported types."""
        with self.assertRaises(TypeError) as ctx:
            PyHydrate(object())
        msg = str(ctx.exception)
        assert "dict" in msg
        assert "list" in msg
        assert "tuple" in msg
        assert "set" in msg
        assert "frozenset" in msg
        assert "range" in msg

    def test_type_error_includes_actual_type_name(self) -> None:
        """Test that TypeError message includes the actual type passed."""
        with self.assertRaises(TypeError) as ctx:
            PyHydrate(object())
        assert "object" in str(ctx.exception)


class TestExistingTypesBehaviorUnchanged(unittest.TestCase):
    """Regression tests: ensure dict, list, primitives, None still work."""

    def test_dict_still_works(self) -> None:
        """Test that dict input is unaffected."""
        data = PyHydrate({"key": "value"})
        assert data.key() == "value"

    def test_list_still_works(self) -> None:
        """Test that list input is unaffected."""
        data = PyHydrate([1, 2, 3])
        assert data[0]() == 1

    def test_str_still_works(self) -> None:
        """Test that str input is unaffected."""
        data = PyHydrate("hello")
        assert data() == "hello"

    def test_int_still_works(self) -> None:
        """Test that int input is unaffected."""
        data = PyHydrate(42)
        assert data() == 42

    def test_float_still_works(self) -> None:
        """Test that float input is unaffected."""
        data = PyHydrate(3.14)
        assert data() == 3.14

    def test_bool_still_works(self) -> None:
        """Test that bool input is unaffected."""
        data = PyHydrate(True)
        assert data() is True

    def test_none_still_works(self) -> None:
        """Test that None input is unaffected."""
        data = PyHydrate(None)
        assert data() is None

    def test_json_string_still_works(self) -> None:
        """Test that JSON string input is unaffected."""
        data = PyHydrate('{"a": 1}')
        assert data.a() == 1


if __name__ == "__main__":
    unittest.main()
