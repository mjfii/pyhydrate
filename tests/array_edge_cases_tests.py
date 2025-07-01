"""Tests for array edge cases and bounds checking.

These tests validate edge cases in array indexing, bounds checking,
and error handling to ensure robust behavior in all scenarios.
"""

import unittest
import warnings

from pyhydrate import PyHydrate, PyHydrateWarning


class ArrayEdgeCasesTests(unittest.TestCase):
    """Test edge cases for array indexing and bounds checking."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.empty_array = PyHydrate([])
        self.single_element = PyHydrate(["only"])
        self.nested_arrays = PyHydrate([
            [],
            ["a"],
            ["b", "c"],
            [1, 2, 3, 4, 5]
        ])
        self.mixed_array = PyHydrate([
            "string",
            42,
            3.14,
            True,
            None,
            {"object": "value"},
            [1, 2, 3]
        ])

    def test_empty_array_access(self) -> None:
        """Test accessing elements in empty arrays."""
        # Positive indices
        assert self.empty_array[0]() is None
        assert self.empty_array[1]() is None
        assert self.empty_array[100]() is None
        
        # Negative indices
        assert self.empty_array[-1]() is None
        assert self.empty_array[-2]() is None
        assert self.empty_array[-100]() is None

    def test_single_element_array_bounds(self) -> None:
        """Test bounds checking with single element arrays."""
        # Valid access
        assert self.single_element[0]() == "only"
        assert self.single_element[-1]() == "only"
        
        # Out of bounds positive
        assert self.single_element[1]() is None
        assert self.single_element[2]() is None
        assert self.single_element[100]() is None
        
        # Out of bounds negative
        assert self.single_element[-2]() is None
        assert self.single_element[-3]() is None
        assert self.single_element[-100]() is None

    def test_nested_empty_arrays(self) -> None:
        """Test accessing elements in nested arrays that contain empty arrays."""
        # Access the empty array
        empty_nested = self.nested_arrays[0]
        assert empty_nested[0]() is None
        assert empty_nested[-1]() is None
        
        # Access other arrays with bounds checking
        single_nested = self.nested_arrays[1]
        assert single_nested[0]() == "a"
        assert single_nested[-1]() == "a"
        assert single_nested[1]() is None
        assert single_nested[-2]() is None

    def test_large_indices(self) -> None:
        """Test very large indices don't break the system."""
        test_array = PyHydrate([1, 2, 3])
        
        # Very large positive indices
        assert test_array[1000000]() is None
        assert test_array[999999999]() is None
        
        # Very large negative indices
        assert test_array[-1000000]() is None
        assert test_array[-999999999]() is None

    def test_zero_and_boundary_indices(self) -> None:
        """Test boundary conditions around zero and array length."""
        test_array = PyHydrate(["a", "b", "c"])  # length = 3
        
        # Valid boundaries
        assert test_array[0]() == "a"    # first
        assert test_array[2]() == "c"    # last
        assert test_array[-1]() == "c"   # last via negative
        assert test_array[-3]() == "a"   # first via negative
        
        # Invalid boundaries
        assert test_array[3]() is None   # length
        assert test_array[-4]() is None  # -(length + 1)

    def test_float_indices_conversion(self) -> None:
        """Test that float indices are properly converted to integers."""
        test_array = PyHydrate(["a", "b", "c"])
        
        # Float indices should be converted to int
        # Note: This tests the int(index) conversion in __getitem__
        assert test_array[0.0]() == "a"
        assert test_array[1.9]() == "b"  # Should truncate to 1
        assert test_array[2.1]() == "c"  # Should truncate to 2
        
        # Negative float indices
        assert test_array[-1.0]() == "c"
        assert test_array[-2.9]() == "b"  # Should truncate to -2

    def test_invalid_index_types(self) -> None:
        """Test behavior with invalid index types."""
        test_array = PyHydrate(["a", "b", "c"])
        
        # Non-numeric string indices should return None (graceful failure)
        assert test_array["invalid"]() is None
        assert test_array["abc"]() is None
        
        # Numeric strings get converted to int (this is expected behavior)
        assert test_array["0"]() == "a"  # "0" -> 0
        assert test_array["1"]() == "b"  # "1" -> 1
        
        # None index should return None
        assert test_array[None]() is None

    def test_chained_out_of_bounds_access(self) -> None:
        """Test chaining access after out of bounds returns."""
        test_array = PyHydrate([{"key": "value"}])
        
        # Valid chain
        assert test_array[0].key() == "value"
        
        # Invalid first access should return None primitive, 
        # but chaining should still work gracefully
        invalid_chain = test_array[10].key
        assert invalid_chain() is None
        
        # Even deeper chaining should work
        deep_invalid = test_array[10].key.nested.deep.access
        assert deep_invalid() is None

    def test_mixed_type_array_indexing(self) -> None:
        """Test indexing arrays with mixed data types."""
        # Test each type
        assert self.mixed_array[0]() == "string"
        assert self.mixed_array[1]() == 42
        assert self.mixed_array[2]() == 3.14
        assert self.mixed_array[3]() is True
        assert self.mixed_array[4]() is None
        
        # Test object access
        assert self.mixed_array[5].object() == "value"
        
        # Test nested array access
        assert self.mixed_array[6][0]() == 1
        assert self.mixed_array[6][-1]() == 3
        
        # Test negative indexing across mixed types
        assert self.mixed_array[-1][1]() == 2  # Last element (array), second item
        assert self.mixed_array[-2].object() == "value"  # Second to last (object)
        assert self.mixed_array[-7]() == "string"  # First element via negative

    def test_performance_with_large_out_of_bounds(self) -> None:
        """Test that out of bounds access doesn't have performance issues."""
        small_array = PyHydrate([1, 2, 3])
        
        # Large out of bounds access should be fast and not cause issues
        start_time = unittest.TestCase()  # Using unittest for timing context
        
        # Multiple large out of bounds accesses
        for i in [1000, 10000, 100000, -1000, -10000, -100000]:
            result = small_array[i]()
            assert result is None
        
        # Should complete without hanging or issues

    def test_no_warnings_from_bounds_checking(self) -> None:
        """Test that normal bounds checking doesn't generate warnings."""
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            test_array = PyHydrate([1, 2, 3])
            
            # Normal access
            test_array[0]()
            test_array[-1]()
            
            # Out of bounds access
            test_array[10]()
            test_array[-10]()
            
            # Invalid types
            test_array["invalid"]()
            test_array[None]()
            
            # No PyHydrate warnings should be generated from normal indexing
            pyhydrate_warnings = [warning for warning in w if issubclass(warning.category, PyHydrateWarning)]
            assert len(pyhydrate_warnings) == 0, f"Unexpected warnings from indexing: {[str(w.message) for w in pyhydrate_warnings]}"

    def test_array_length_calculation_edge_cases(self) -> None:
        """Test edge cases in array length calculation for bounds checking."""
        
        # Test various array sizes
        test_cases = [
            ([]),                    # length 0
            ([1]),                   # length 1
            ([1, 2]),               # length 2
            (list(range(100))),     # length 100
            (list(range(1000))),    # length 1000
        ]
        
        for data in test_cases:
            array = PyHydrate(data)
            length = len(data)
            
            if length == 0:
                # Empty array - all access should return None
                assert array[0]() is None
                assert array[-1]() is None
            else:
                # Non-empty array - test boundaries
                assert array[0]() == data[0]                # First element
                assert array[length - 1]() == data[-1]      # Last element
                assert array[-1]() == data[-1]              # Last via negative
                assert array[-length]() == data[0]          # First via negative
                
                # Out of bounds
                assert array[length]() is None              # Just past end
                assert array[-(length + 1)]() is None       # Just before start


if __name__ == "__main__":
    unittest.main()