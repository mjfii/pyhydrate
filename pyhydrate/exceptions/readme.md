# exceptions

Custom warning classes for PyHydrate's error handling system. Follows a one-class-per-module standard for organization and maintainability.

## Files

- **`__init__.py`** - Package entry point; re-exports all warning classes and the `format_warning_message` utility.
- **`pyhydrate_warning.py`** - `PyHydrateWarning(UserWarning)` - Base warning class for all PyHydrate operations. Users can filter all PyHydrate warnings by catching this type.
- **`type_conversion_warning.py`** - `TypeConversionWarning(PyHydrateWarning)` - Issued when type conversion fails (e.g., `int()` on a non-numeric value).
- **`access_pattern_warning.py`** - `AccessPatternWarning(PyHydrateWarning)` - Issued when accessing invalid keys or out-of-bounds indices.
- **`api_usage_warning.py`** - `APIUsageWarning(PyHydrateWarning)` - Issued when an unsupported call type is passed (e.g., `data('invalid_format')`).
- **`immutable_conversion_warning.py`** - `ImmutableConversionWarning(PyHydrateWarning)` - Issued when an immutable input type (`tuple`, `frozenset`) is converted to a mutable list during `PyHydrate` initialization.
- **`format_warning_message.py`** - `format_warning_message(message, suggestion, context)` utility function for consistent warning message formatting across the codebase.
