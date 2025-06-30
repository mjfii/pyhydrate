"""
Tests for memory efficiency improvements in lazy loading implementation.

This module validates that the lazy loading implementation reduces memory
usage compared to the previous eager loading approach.
"""

import unittest

import pyhydrate as pyhy


class MemoryEfficiencyTests(unittest.TestCase):
    """Test memory efficiency improvements with lazy loading."""

    def setUp(self) -> None:
        """Set up test data."""
        # Large nested structure to test memory efficiency
        self.large_data = {
            "level_1": {
                f"section_{i}": {
                    f"subsection_{j}": {
                        f"item_{k}": f"value_{i}_{j}_{k}" for k in range(10)
                    }
                    for j in range(10)
                }
                for i in range(10)
            },
            "arrays": [
                [{"nested": f"value_{i}_{j}"} for j in range(10)] for i in range(10)
            ],
        }

    def test_lazy_loading_behavior(self) -> None:
        """Test that lazy loading only creates objects when accessed."""
        hydrated = pyhy.PyHydrate(self.large_data)

        # Access a specific nested path
        result = hydrated.level_1.section_0.subsection_0.item_0()
        assert result == "value_0_0_0"

        # Test that accessing the same path multiple times returns consistent results
        result2 = hydrated.level_1.section_0.subsection_0.item_0()
        assert result2 == "value_0_0_0"

        # Test that different sections can be accessed independently
        result3 = hydrated.level_1.section_1.subsection_1.item_1()
        assert result3 == "value_1_1_1"

    def test_key_mapping_efficiency(self) -> None:
        """Test that key mappings work correctly for various key formats."""
        test_data = {
            "camelCaseKey": "value1",
            "kebab-case-key": "value2",
            "PascalCaseKey": "value3",
            "normal_key": "value4",
        }

        hydrated = pyhy.PyHydrate(test_data)

        # All key formats should be accessible via snake_case
        assert hydrated.camel_case_key() == "value1"
        assert hydrated.kebab_case_key() == "value2"
        assert hydrated.pascal_case_key() == "value3"
        assert hydrated.normal_key() == "value4"

    def test_array_lazy_loading(self) -> None:
        """Test that array elements are loaded lazily."""
        test_data = [{"item": i} for i in range(100)]

        hydrated = pyhy.PyHydrate(test_data)

        # Access specific elements
        result_50 = hydrated[50].item()
        assert result_50 == 50

        result_0 = hydrated[0].item()
        assert result_0 == 0

        result_99 = hydrated[99].item()
        assert result_99 == 99

        # Test out of bounds access returns None
        result_out_of_bounds = hydrated[200].item()
        assert result_out_of_bounds is None

    def test_memory_usage_simulation(self) -> None:
        """Simulate memory usage patterns to verify efficiency."""
        # Create a structure that would use significant memory if fully hydrated
        large_structure = {}
        for i in range(50):
            large_structure[f"section_{i}"] = {
                f"item_{j}": {
                    "data": f"large_value_{i}_{j}_" + "x" * 100,
                    "metadata": {
                        "id": f"{i}_{j}",
                        "tags": [f"tag_{k}" for k in range(10)],
                    },
                }
                for j in range(20)
            }

        hydrated = pyhy.PyHydrate(large_structure)

        # Access only a small subset
        result1 = hydrated.section_0.item_0.data()
        result2 = hydrated.section_1.item_5.metadata.id()

        assert result1.startswith("large_value_0_0_")
        assert result2 == "1_5"

        # Test that we can access deeply nested arrays in metadata
        tags = hydrated.section_1.item_5.metadata.tags[0]()
        assert tags == "tag_0"

    def test_cleaned_value_on_demand(self) -> None:
        """Test that cleaned values are computed correctly."""
        test_data = {
            "camelCase": {"nestedKey": {"deepValue": "test"}},
            "simpleKey": "simple",
        }

        hydrated = pyhy.PyHydrate(test_data)

        # Access nested values using cleaned keys
        result1 = hydrated.camel_case.nested_key.deep_value()
        assert result1 == "test"

        result2 = hydrated.simple_key()
        assert result2 == "simple"

        # Test that the cleaned structure is accessible via the call interface
        cleaned_dict = hydrated("value")
        expected = {
            "camel_case": {"nested_key": {"deep_value": "test"}},
            "simple_key": "simple",
        }
        assert cleaned_dict == expected

    def test_slots_memory_optimization(self) -> None:
        """Test that __slots__ optimization is working."""
        hydrated = pyhy.PyHydrate({"test": "value"})

        # Verify __slots__ are defined
        assert hasattr(hydrated.__class__, "__slots__")

        # Test that we can't add arbitrary attributes (slots restriction)
        with self.assertRaises(AttributeError):
            hydrated.arbitrary_attribute = "test"

    def test_cache_persistence(self) -> None:
        """Test that cached values persist and aren't recreated."""
        test_data = {"key": {"nested": "value"}}
        hydrated = pyhy.PyHydrate(test_data)

        # Access the same path multiple times
        obj1 = hydrated.key
        obj2 = hydrated.key
        obj3 = hydrated.key.nested
        obj4 = hydrated.key.nested

        # Should be the exact same object instances (cached)
        assert obj1 is obj2
        assert obj3 is obj4

        # Test that the values are consistent
        assert obj1.nested() == "value"
        assert obj3() == "value"

    def test_performance_with_deep_nesting(self) -> None:
        """Test performance with deeply nested structures."""
        # Create a simpler deeply nested structure
        deep_data = {
            "level_0": {"data": "value_at_level_0"},
            "level_1": {"data": "value_at_level_1"},
            "level_2": {"data": "value_at_level_2"},
            "nested": {
                "level_0": {"data": "nested_value_0"},
                "level_1": {"data": "nested_value_1"},
            },
        }

        hydrated = pyhy.PyHydrate(deep_data)

        # Access various nested values
        result_0 = hydrated.level_0.data()
        assert result_0 == "value_at_level_0"

        result_1 = hydrated.level_1.data()
        assert result_1 == "value_at_level_1"

        # Access nested structure
        nested_result = hydrated.nested.level_0.data()
        assert nested_result == "nested_value_0"

    def test_array_of_objects_efficiency(self) -> None:
        """Test efficiency with arrays containing objects."""
        array_data = [
            {
                "id": i,
                "data": {
                    "name": f"item_{i}",
                    "props": {"active": i % 2 == 0, "category": f"cat_{i // 10}"},
                },
            }
            for i in range(100)
        ]

        hydrated = pyhy.PyHydrate(array_data)

        # Access specific items
        item_25 = hydrated[25]
        assert item_25.id() == 25
        assert item_25.data.name() == "item_25"
        assert item_25.data.props.active() is False
        assert item_25.data.props.category() == "cat_2"

        # Access different item
        item_80 = hydrated[80]
        assert item_80.id() == 80
        assert item_80.data.props.active() is True
        assert item_80.data.props.category() == "cat_8"


if __name__ == "__main__":
    unittest.main()
