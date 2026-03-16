# notation

Notation system classes that wrap Python data types with dot notation access, lazy loading, and multiple output formats.

## Files

- **`__init__.py`** - Package entry point; re-exports `NotationPrimitive`, `NotationArray`, and `NotationObject`.
- **`notation_base.py`** - `NotationBase` - Unified base class providing shared functionality: debug logging, key normalization (`_cast_key` converts camelCase/kebab-case/spaced keys to snake_case), magic methods (`__int__`, `__float__`, `__bool__`, `__repr__`, `__str__`), and output formatting (`__call__` with format arguments).
- **`notation_primitive.py`** - `NotationPrimitive(NotationBase)` - Wraps primitive values (str, int, float, bool, None). Returns the raw value on `__call__()` and supports serialization to JSON/YAML/TOML element format.
- **`notation_structures.py`** - Contains `NotationObject(NotationBase)` for dict/object wrapping and `NotationArray(NotationBase)` for list/array wrapping. Both use lazy loading with smart caching - child objects are created on first access and cached for subsequent lookups.
- **`notation_dumper.py`** - `NotationDumper(yaml.Dumper)` - Custom YAML dumper that formats output consistently, handling None values, multiline strings, and ordered dict output.
