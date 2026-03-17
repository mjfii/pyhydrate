# tests

Unit test suite for PyHydrate using the `unittest` framework. All test files follow the `*_tests.py` naming convention for automatic discovery by CI.

Run all tests: `python -m unittest discover -s tests/ -p "*_tests.py"`

## Files

- **`__init__.py`** - Package marker for test discovery.
- **`array_edge_cases_tests.py`** - Edge cases in array indexing, bounds checking, and error handling for robust array behavior.
- **`call_tests.py`** - `__call__` method functionality including JSON, YAML, TOML, type, element, depth, map, and value output formats.
- **`cloud_save_tests.py`** - Cloud storage save functionality: remote path detection for S3/GCS/ADLS URIs, format detection from remote paths, mocked fsspec integration, ImportError handling when fsspec is missing, and verification that local paths are unaffected.
- **`dict_get_tests.py`** - Dictionary access patterns via dot notation with nested key lookups and key normalization.
- **`error_handling_tests.py`** - Standardized error handling and warning system validation across all warning types.
- **`initialization_tests.py`** - Comprehensive initialization tests for all supported input types: primitives, dicts, lists, JSON strings, YAML strings, TOML strings, and file loading.
- **`list_get_tests.py`** - Array/list access patterns including indexing, nested list access, and negative indices.
- **`magic_methods_tests.py`** - Magic methods (`__int__`, `__float__`, `__bool__`) functionality and error handling for invalid conversions.
- **`memory_efficiency_tests.py`** - Lazy loading behavior validation and memory optimization verification.
- **`none_serialization_tests.py`** - None value serialization behavior in YAML, JSON, and TOML output formats.
- **`primitive_get_tests.py`** - Primitive value handling for str, int, float, bool, and None types.
- **`repr_method_tests.py`** - `__repr__` method functionality and verification that repr calls do not trigger spurious `APIUsageWarning` messages.
- **`save_tests.py`** - File save/write functionality: saving to JSON/YAML/TOML files, round-trip (load/modify/save/reload), source path save-back, and format override.
- **`write_tests.py`** - Write (mutation) support: setting existing/new keys, deep auto-creation of intermediate dicts via proxy chain, creating from scratch, array mutation, deletion, key normalization on write, and serialization after mutation.
