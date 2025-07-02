import json
import unittest
from pathlib import Path

import pyhydrate as pyhy


class DictReadMethods(unittest.TestCase):
    _data = pyhy.PyHydrate(
        json.loads(Path("./pyhydrate/data/basic-list-get.json").read_text()), debug=True
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


class NegativeIndexingTests(unittest.TestCase):
    """Test negative indexing functionality for arrays."""

    def setUp(self) -> None:
        """Set up test data for negative indexing tests."""
        self.test_data = ["first", "second", "third", "fourth", "last"]
        self.nested_data = [
            ["a", "b", "c"],
            [1, 2, 3, 4],
            [{"key": "value1"}, {"key": "value2"}],
        ]

        self.simple_array = pyhy.PyHydrate(self.test_data)
        self.nested_array = pyhy.PyHydrate(self.nested_data)

    def test_negative_indexing_simple_array(self) -> None:
        """Test negative indexing with simple array."""
        # Test last element
        assert self.simple_array[-1]() == "last"

        # Test second to last element
        assert self.simple_array[-2]() == "fourth"

        # Test first element via negative indexing
        assert self.simple_array[-5]() == "first"

        # Test all elements via negative indexing
        assert self.simple_array[-3]() == "third"
        assert self.simple_array[-4]() == "second"

    def test_negative_indexing_nested_arrays(self) -> None:
        """Test negative indexing with nested arrays."""
        # Test last sub-array
        last_subarray = self.nested_array[-1]
        assert last_subarray[0].key() == "value1"
        assert last_subarray[-1].key() == "value2"

        # Test middle sub-array with negative indexing
        middle_subarray = self.nested_array[-2]
        assert middle_subarray[-1]() == 4
        assert middle_subarray[-4]() == 1

        # Test first sub-array via negative indexing
        first_subarray = self.nested_array[-3]
        assert first_subarray[-1]() == "c"
        assert first_subarray[-3]() == "a"

    def test_negative_indexing_out_of_bounds(self) -> None:
        """Test negative indexing with out of bounds indices."""
        # Test indices that are too negative
        assert self.simple_array[-10]() is None
        assert self.simple_array[-100]() is None

        # Test with nested arrays
        assert self.nested_array[-10]() is None

        # Test accessing out of bounds on valid sub-array
        valid_subarray = self.nested_array[0]
        assert valid_subarray[-10]() is None

    def test_negative_indexing_edge_cases(self) -> None:
        """Test edge cases for negative indexing."""
        # Test with single element array
        single_element = pyhy.PyHydrate(["only"])
        assert single_element[-1]() == "only"
        assert single_element[-2]() is None

        # Test with empty array access (should gracefully fail)
        empty_array = pyhy.PyHydrate([])
        assert empty_array[-1]() is None
        assert empty_array[0]() is None

    def test_negative_vs_positive_indexing_equivalence(self) -> None:
        """Test that negative and positive indexing return the same elements."""
        length = len(self.test_data)

        for i in range(length):
            positive_result = self.simple_array[i]()
            negative_result = self.simple_array[i - length]()
            assert positive_result == negative_result, (
                f"Mismatch at index {i}: {positive_result} != {negative_result}"
            )

    def test_negative_indexing_with_chaining(self) -> None:
        """Test negative indexing works with method chaining."""
        # Create data with objects that have methods
        complex_data = [
            {"items": [1, 2, 3]},
            {"items": [4, 5, 6]},
            {"items": [7, 8, 9]},
        ]

        complex_array = pyhy.PyHydrate(complex_data)

        # Test chaining with negative indexing
        assert complex_array[-1].items[-1]() == 9
        assert complex_array[-2].items[-3]() == 4
        assert complex_array[-3].items[-2]() == 2


if __name__ == "__main__":
    unittest.main()
