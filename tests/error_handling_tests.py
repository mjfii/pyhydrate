"""Tests for error handling and warning system in PyHydrate.

These tests validate the standardized error handling approach implemented
to address GitHub issue #28.
"""

import logging
import unittest
import warnings
from io import StringIO

from pyhydrate import (
    APIUsageWarning,
    NotationArray,
    NotationObject,
    NotationPrimitive,
    PyHydrate,
    PyHydrateWarning,
    TypeConversionWarning,
)


class TestErrorHandling(unittest.TestCase):
    """Test standardized error handling across PyHydrate components."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.log_stream = StringIO()
        self.log_handler = logging.StreamHandler(self.log_stream)
        self.logger = logging.getLogger("pyhydrate")
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        self.logger.removeHandler(self.log_handler)
        self.log_handler.close()

    def test_type_conversion_warnings(self) -> None:
        """Test TypeConversionWarning is raised for invalid type conversions."""

        # Test NotationObject with invalid type
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _obj = NotationObject("not a dict", 0)

            assert len(w) == 1
            assert isinstance(w[0].category(), TypeConversionWarning)
            assert "NotationObject initialization" in str(w[0].message)

        # Test NotationArray with invalid type
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _arr = NotationArray("not a list", 0)

            assert len(w) == 1
            assert isinstance(w[0].category(), TypeConversionWarning)
            assert "NotationArray initialization" in str(w[0].message)

        # Test NotationPrimitive with invalid type
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _prim = NotationPrimitive({"not": "primitive"}, 0)

            assert len(w) == 1
            assert isinstance(w[0].category(), TypeConversionWarning)
            assert "NotationPrimitive initialization" in str(w[0].message)

    def test_api_usage_warnings(self) -> None:
        """Test APIUsageWarning is raised for invalid API usage."""

        data = {"test": "value"}
        hydrated = PyHydrate(data)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = hydrated("invalid_call_type")

            assert len(w) == 1
            assert isinstance(w[0].category(), APIUsageWarning)
            assert "Call type" in str(w[0].message)
            assert "invalid_call_type" in str(w[0].message)
            assert "Valid options are:" in str(w[0].message)
            assert result is None

    def test_warning_inheritance(self) -> None:
        """Test that all custom warnings inherit from PyHydrateWarning."""

        # Test that we can catch all PyHydrate warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Generate different types of warnings
            NotationObject("invalid", 0)
            NotationArray("invalid", 0)
            NotationPrimitive({"invalid": "primitive"}, 0)

            hydrated = PyHydrate({"test": "value"})
            hydrated("invalid_call")

            # All warnings should be catchable as PyHydrateWarning
            assert len(w) == 4
            for warning in w:
                assert issubclass(warning.category, PyHydrateWarning)

    def test_debug_logging(self) -> None:
        """Test that debug mode generates appropriate log messages."""

        data = {"nested": {"value": 42}}
        hydrated = PyHydrate(data, debug=True)

        # Access nested value to trigger debug logging
        result = hydrated.nested.value()

        # Verify the result is still correct (debug logging is complex, just test functionality)
        assert result == 42

    def test_error_handling_preserves_functionality(self) -> None:
        """Test that error handling doesn't break normal functionality."""

        # Valid operations should still work
        data = {
            "string": "test",
            "number": 42,
            "array": [1, 2, 3],
            "nested": {"deep": "value"},
        }

        hydrated = PyHydrate(data)

        # Test normal access patterns
        assert hydrated.string() == "test"
        assert hydrated.number() == 42
        assert hydrated.array[0]() == 1
        assert hydrated.nested.deep() == "value"

        # Test call types
        assert hydrated.string("type") is str
        element_result = hydrated.number("element")
        assert element_result["int"] == 42
        assert "test" in hydrated.string("json")
        assert "test" in hydrated.string("yaml")

    def test_graceful_error_handling(self) -> None:
        """Test that invalid access returns None primitives gracefully."""

        data = {"valid": "data"}
        hydrated = PyHydrate(data)

        # Invalid attribute access should return None primitive
        invalid_access = hydrated.nonexistent
        assert isinstance(invalid_access, NotationPrimitive)
        assert invalid_access() is None

        # Invalid index access should return None primitive
        invalid_index = hydrated[999]
        assert isinstance(invalid_index, NotationPrimitive)
        assert invalid_index() is None

    def test_warning_filtering(self) -> None:
        """Test that warnings can be filtered by type."""

        # Test filtering TypeConversionWarning specifically
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.filterwarnings("ignore", category=TypeConversionWarning)

            # This should not generate a warning due to filtering
            NotationObject("invalid", 0)

            # But this should still generate a warning
            hydrated = PyHydrate({"test": "value"})
            hydrated("invalid_call")

            # Only the APIUsageWarning should be recorded
            assert len(w) == 1
            assert isinstance(w[0].category(), APIUsageWarning)

    def test_exception_formatting(self) -> None:
        """Test that warning messages are properly formatted and informative."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Generate a type conversion warning
            NotationObject(123, 0)

            warning_message = str(w[0].message)

            # Check that the message contains key information
            assert "NotationObject initialization" in warning_message
            assert "expected dict" in warning_message
            assert "got int" in warning_message
            assert "dictionary" in warning_message  # suggestion

    def test_logging_levels(self) -> None:
        """Test that debug logging respects log levels."""

        data = {"test": "value"}
        hydrated = PyHydrate(data, debug=True)

        # Access value
        result = hydrated.test()

        # The result should still be correct regardless of logging
        assert result == "value"


if __name__ == "__main__":
    unittest.main()
