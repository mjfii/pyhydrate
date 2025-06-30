import unittest

import pytest

import pyhydrate as pyhy


class MagicMethodsTests(unittest.TestCase):
    """Test magic methods (__int__, __float__, __bool__) implementation."""

    def test_int_conversion_from_int(self) -> None:
        """Test __int__ conversion from integer value."""
        test_int = pyhy.PyHydrate(42)
        result = int(test_int)
        assert result == 42
        assert isinstance(result, int)

    def test_int_conversion_from_float(self) -> None:
        """Test __int__ conversion from float value."""
        test_float = pyhy.PyHydrate(3.14)
        result = int(test_float)
        assert result == 3
        assert isinstance(result, int)

    def test_int_conversion_from_bool_true(self) -> None:
        """Test __int__ conversion from boolean True value."""
        test_bool = pyhy.PyHydrate(True)
        result = int(test_bool)
        assert result == 1
        assert isinstance(result, int)

    def test_int_conversion_from_bool_false(self) -> None:
        """Test __int__ conversion from boolean False value."""
        test_bool = pyhy.PyHydrate(False)
        result = int(test_bool)
        assert result == 0
        assert isinstance(result, int)

    def test_int_conversion_from_string_number(self) -> None:
        """Test __int__ conversion from string containing number."""
        test_string = pyhy.PyHydrate("123")
        result = int(test_string)
        assert result == 123
        assert isinstance(result, int)

    def test_int_conversion_from_string_float(self) -> None:
        """Test __int__ conversion from string containing float."""
        # Note: PyHydrate auto-converts valid numbers via YAML parsing
        # So we test with a string that contains a decimal but isn't auto-converted
        test_string = pyhy.PyHydrate("45.67abc")  # This won't be converted to float
        with pytest.raises(ValueError) as cm:
            int(test_string)
        assert "Cannot convert '45.67abc' to int" in str(cm.exception)

    def test_int_conversion_from_string_invalid(self) -> None:
        """Test __int__ conversion from string with invalid content."""
        test_string = pyhy.PyHydrate("not_a_number")
        with pytest.raises(ValueError) as cm:
            int(test_string)
        assert "Cannot convert 'not_a_number' to int" in str(cm.exception)

    def test_int_conversion_from_none(self) -> None:
        """Test __int__ conversion from None value."""
        test_none = pyhy.PyHydrate(None)
        with pytest.raises(TypeError) as cm:
            int(test_none)
        assert "Cannot convert NoneType to int" in str(cm.exception)

    def test_int_conversion_from_dict(self) -> None:
        """Test __int__ conversion from dict value (should fail)."""
        test_dict = pyhy.PyHydrate({"key": "value"})
        with pytest.raises(TypeError) as cm:
            int(test_dict)
        assert "Cannot convert dict to int" in str(cm.exception)

    def test_int_conversion_from_list(self) -> None:
        """Test __int__ conversion from list value (should fail)."""
        test_list = pyhy.PyHydrate([1, 2, 3])
        with pytest.raises(TypeError) as cm:
            int(test_list)
        assert "Cannot convert list to int" in str(cm.exception)

    def test_float_conversion_from_int(self) -> None:
        """Test __float__ conversion from integer value."""
        test_int = pyhy.PyHydrate(42)
        result = float(test_int)
        assert result == 42.0
        assert isinstance(result, float)

    def test_float_conversion_from_float(self) -> None:
        """Test __float__ conversion from float value."""
        test_float = pyhy.PyHydrate(3.14)
        result = float(test_float)
        assert result == 3.14
        assert isinstance(result, float)

    def test_float_conversion_from_bool_true(self) -> None:
        """Test __float__ conversion from boolean True value."""
        test_bool = pyhy.PyHydrate(True)
        result = float(test_bool)
        assert result == 1.0
        assert isinstance(result, float)

    def test_float_conversion_from_bool_false(self) -> None:
        """Test __float__ conversion from boolean False value."""
        test_bool = pyhy.PyHydrate(False)
        result = float(test_bool)
        assert result == 0.0
        assert isinstance(result, float)

    def test_float_conversion_from_string_number(self) -> None:
        """Test __float__ conversion from string containing number."""
        test_string = pyhy.PyHydrate("123")
        result = float(test_string)
        assert result == 123.0
        assert isinstance(result, float)

    def test_float_conversion_from_string_float(self) -> None:
        """Test __float__ conversion from string containing float."""
        test_string = pyhy.PyHydrate("45.67")
        result = float(test_string)
        assert result == 45.67
        assert isinstance(result, float)

    def test_float_conversion_from_string_invalid(self) -> None:
        """Test __float__ conversion from string with invalid content."""
        test_string = pyhy.PyHydrate("not_a_number")
        with pytest.raises(ValueError) as cm:
            float(test_string)
        assert "Cannot convert 'not_a_number' to float" in str(cm.exception)

    def test_float_conversion_from_none(self) -> None:
        """Test __float__ conversion from None value."""
        test_none = pyhy.PyHydrate(None)
        with pytest.raises(TypeError) as cm:
            float(test_none)
        assert "Cannot convert NoneType to float" in str(cm.exception)

    def test_float_conversion_from_dict(self) -> None:
        """Test __float__ conversion from dict value (should fail)."""
        test_dict = pyhy.PyHydrate({"key": "value"})
        with pytest.raises(TypeError) as cm:
            float(test_dict)
        assert "Cannot convert dict to float" in str(cm.exception)

    def test_float_conversion_from_list(self) -> None:
        """Test __float__ conversion from list value (should fail)."""
        test_list = pyhy.PyHydrate([1, 2, 3])
        with pytest.raises(TypeError) as cm:
            float(test_list)
        assert "Cannot convert list to float" in str(cm.exception)

    def test_bool_conversion_from_true(self) -> None:
        """Test __bool__ conversion from True value."""
        test_bool = pyhy.PyHydrate(True)
        result = bool(test_bool)
        assert result is True

    def test_bool_conversion_from_false(self) -> None:
        """Test __bool__ conversion from False value."""
        test_bool = pyhy.PyHydrate(False)
        result = bool(test_bool)
        assert result is False

    def test_bool_conversion_from_none(self) -> None:
        """Test __bool__ conversion from None value."""
        test_none = pyhy.PyHydrate(None)
        result = bool(test_none)
        assert result is False

    def test_bool_conversion_from_zero_int(self) -> None:
        """Test __bool__ conversion from zero integer."""
        test_int = pyhy.PyHydrate(0)
        result = bool(test_int)
        assert result is False

    def test_bool_conversion_from_nonzero_int(self) -> None:
        """Test __bool__ conversion from non-zero integer."""
        test_int = pyhy.PyHydrate(42)
        result = bool(test_int)
        assert result is True

    def test_bool_conversion_from_zero_float(self) -> None:
        """Test __bool__ conversion from zero float."""
        test_float = pyhy.PyHydrate(0.0)
        result = bool(test_float)
        assert result is False

    def test_bool_conversion_from_nonzero_float(self) -> None:
        """Test __bool__ conversion from non-zero float."""
        test_float = pyhy.PyHydrate(3.14)
        result = bool(test_float)
        assert result is True

    def test_bool_conversion_from_empty_string(self) -> None:
        """Test __bool__ conversion from empty string."""
        test_string = pyhy.PyHydrate("")
        result = bool(test_string)
        assert result is False

    def test_bool_conversion_from_nonempty_string(self) -> None:
        """Test __bool__ conversion from non-empty string."""
        test_string = pyhy.PyHydrate("hello")
        result = bool(test_string)
        assert result is True

    def test_bool_conversion_from_empty_dict(self) -> None:
        """Test __bool__ conversion from empty dict."""
        test_dict = pyhy.PyHydrate({})
        result = bool(test_dict)
        assert result is False

    def test_bool_conversion_from_nonempty_dict(self) -> None:
        """Test __bool__ conversion from non-empty dict."""
        test_dict = pyhy.PyHydrate({"key": "value"})
        result = bool(test_dict)
        assert result is True

    def test_bool_conversion_from_empty_list(self) -> None:
        """Test __bool__ conversion from empty list."""
        test_list = pyhy.PyHydrate([])
        result = bool(test_list)
        assert result is False

    def test_bool_conversion_from_nonempty_list(self) -> None:
        """Test __bool__ conversion from non-empty list."""
        test_list = pyhy.PyHydrate([1, 2, 3])
        result = bool(test_list)
        assert result is True

    def test_magic_methods_with_nested_access(self) -> None:
        """Test magic methods work with nested object access."""
        test_data = {"numbers": {"int": 42, "float": 3.14, "str": "123"}}
        test_obj = pyhy.PyHydrate(test_data)
        
        # Test int conversion on nested access
        result_int = int(test_obj.numbers.int)
        assert result_int == 42
        
        # Test float conversion on nested access
        result_float = float(test_obj.numbers.float)
        assert result_float == 3.14
        
        # Test bool conversion on nested access
        result_bool = bool(test_obj.numbers.str)
        assert result_bool is True

    def test_magic_methods_with_array_access(self) -> None:
        """Test magic methods work with array element access."""
        test_data = [42, 3.14, "123", False]
        test_obj = pyhy.PyHydrate(test_data)
        
        # Test conversions on array elements
        assert int(test_obj[0]) == 42
        assert float(test_obj[1]) == 3.14
        assert int(test_obj[2]) == 123
        assert bool(test_obj[3]) is False


if __name__ == "__main__":
    unittest.main()
