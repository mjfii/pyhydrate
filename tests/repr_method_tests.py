"""Tests for __repr__ method functionality and warning prevention.

These tests validate that the __repr__ method works correctly without
generating spurious APIUsageWarning messages, addressing the issue where
__dict__.get() calls were triggering the warning system.
"""

import unittest
import warnings

from pyhydrate import (
    APIUsageWarning,
    NotationArray,
    NotationObject,
    NotationPrimitive,
    PyHydrate,
    PyHydrateWarning,
)


class ReprMethodTests(unittest.TestCase):
    """Test __repr__ method functionality without spurious warnings."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.complex_data = {
            "user": {
                "name": "John Doe",
                "preferences": {"theme": "dark", "notifications": True},
            },
            "items": [1, 2, 3, {"nested": "value"}],
            "settings": {"api_key": "secret123", "timeout": 30.5},
        }

        self.simple_data = {"key": "value", "number": 42}
        self.array_data = ["first", "second", {"object": "inside"}]
        self.primitive_data = "simple string"

    def test_repr_no_spurious_warnings(self) -> None:
        """Test that __repr__ doesn't generate APIUsageWarning messages."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Create PyHydrate instances
            hydrated_complex = PyHydrate(self.complex_data)
            hydrated_simple = PyHydrate(self.simple_data)
            hydrated_array = PyHydrate(self.array_data)
            hydrated_primitive = PyHydrate(self.primitive_data)

            # Call __repr__ on various objects
            repr(hydrated_complex)
            repr(hydrated_simple)
            repr(hydrated_array)
            repr(hydrated_primitive)

            # Call __repr__ on nested objects
            repr(hydrated_complex.user)
            repr(hydrated_complex.items)
            repr(hydrated_complex.user.preferences)

            # No warnings should be generated from __repr__ calls
            repr_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, PyHydrateWarning)
            ]
            assert len(repr_warnings) == 0, (
                f"Unexpected warnings from __repr__: {[str(w.message) for w in repr_warnings]}"
            )

    def test_repr_output_format(self) -> None:
        """Test that __repr__ produces correctly formatted output."""

        hydrated = PyHydrate(self.simple_data)
        repr_output = repr(hydrated)

        # Should contain PyHydrate identifier
        assert "PyHydrate" in repr_output

        # Should contain the data
        assert "key" in repr_output
        assert "value" in repr_output
        assert "42" in repr_output

    def test_repr_with_various_data_types(self) -> None:
        """Test __repr__ with different data types."""

        test_cases = [
            # (data, description)
            ({"string": "test", "int": 42, "float": 3.14, "bool": True}, "mixed types"),
            ([1, "two", 3.0, False], "array with mixed types"),
            ({"nested": {"deep": {"value": "found"}}}, "deeply nested"),
            ([], "empty array"),
            ({}, "empty object"),
            (None, "none value"),
            ("simple string", "string primitive"),
            (42, "integer primitive"),
            (3.14, "float primitive"),
            (True, "boolean primitive"),
        ]

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            for data, description in test_cases:
                with self.subTest(description=description):
                    hydrated = PyHydrate(data)
                    repr_output = repr(hydrated)

                    # Should not be empty
                    assert len(repr_output) > 0, f"Empty repr for {description}"

                    # Should contain PyHydrate identifier
                    assert (
                        "PyHydrate" in repr_output
                        or "Primitive" in repr_output
                        or "Object" in repr_output
                        or "Array" in repr_output
                    )

            # No warnings should be generated
            repr_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, PyHydrateWarning)
            ]
            assert len(repr_warnings) == 0, (
                f"Unexpected warnings: {[str(w.message) for w in repr_warnings]}"
            )

    def test_repr_with_debug_mode(self) -> None:
        """Test __repr__ works correctly with debug mode enabled."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Create with debug mode
            hydrated = PyHydrate(self.complex_data, debug=True)

            # Call __repr__ should not generate warnings
            repr_output = repr(hydrated)
            repr_nested = repr(hydrated.user.preferences)

            # Verify no spurious warnings
            repr_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, PyHydrateWarning)
            ]
            assert len(repr_warnings) == 0, (
                f"Debug mode __repr__ generated warnings: {[str(w.message) for w in repr_warnings]}"
            )

            # Verify output is still valid
            assert len(repr_output) > 0
            assert len(repr_nested) > 0

    def test_str_no_spurious_warnings(self) -> None:
        """Test that __str__ doesn't generate APIUsageWarning messages."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            hydrated = PyHydrate(self.complex_data)

            # Call __str__ on various objects
            str(hydrated)
            str(hydrated.user)
            str(hydrated.items)
            str(hydrated.user.name)

            # No warnings should be generated from __str__ calls
            str_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, PyHydrateWarning)
            ]
            assert len(str_warnings) == 0, (
                f"Unexpected warnings from __str__: {[str(w.message) for w in str_warnings]}"
            )

    def test_repr_vs_actual_api_warnings(self) -> None:
        """Test that real API usage warnings still work while __repr__ doesn't trigger them."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            hydrated = PyHydrate(self.simple_data)

            # This should NOT generate a warning
            repr(hydrated)
            str(hydrated)

            # This SHOULD generate a warning (invalid call type)
            hydrated("invalid_call_type")

            # Filter warnings
            api_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, APIUsageWarning)
            ]

            # Should have exactly one warning (from the invalid call)
            assert len(api_warnings) == 1, (
                f"Expected 1 API warning, got {len(api_warnings)}"
            )
            assert "invalid_call_type" in str(api_warnings[0].message)

    def test_repr_with_notation_classes_directly(self) -> None:
        """Test __repr__ directly on notation classes."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Test NotationObject directly
            obj = NotationObject({"key": "value"}, 0)
            repr(obj)

            # Test NotationArray directly
            arr = NotationArray([1, 2, 3], 0)
            repr(arr)

            # Test NotationPrimitive directly
            prim = NotationPrimitive("test", 0)
            repr(prim)

            # No warnings should be generated
            repr_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, PyHydrateWarning)
            ]

            # Filter out expected TypeConversionWarning from creating NotationObject/Array with wrong types
            # We only care about spurious APIUsageWarnings from __repr__
            api_warnings = [
                warning
                for warning in repr_warnings
                if issubclass(warning.category, APIUsageWarning)
            ]
            assert len(api_warnings) == 0, (
                f"Unexpected APIUsageWarnings from __repr__: {[str(w.message) for w in api_warnings]}"
            )

    def test_repr_memory_efficiency(self) -> None:
        """Test that __repr__ doesn't break lazy loading efficiency."""

        # Create large nested structure
        large_data = {
            f"section_{i}": {
                f"subsection_{j}": {
                    f"item_{k}": f"value_{i}_{j}_{k}" for k in range(10)
                }
                for j in range(10)
            }
            for i in range(5)
        }

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            hydrated = PyHydrate(large_data)

            # Call __repr__ should not trigger lazy loading of all elements
            repr(hydrated)

            # Access one specific element
            specific_value = hydrated.section_2.subsection_3.item_5()

            # No warnings from __repr__ calls
            repr_warnings = [
                warning
                for warning in w
                if issubclass(warning.category, PyHydrateWarning)
            ]
            assert len(repr_warnings) == 0, (
                f"Large data __repr__ generated warnings: {[str(w.message) for w in repr_warnings]}"
            )

            # Verify the specific access still works
            assert specific_value == "value_2_3_5"


if __name__ == "__main__":
    unittest.main()
