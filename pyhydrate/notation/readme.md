# notation

Notation system classes that wrap Python data types with dot notation access, lazy loading, write support, and multiple output formats.

## Files

- **`__init__.py`** - Package entry point; re-exports `NotationPrimitive`, `NotationArray`, `NotationObject`, and `NotationProxy`.
- **`notation_base.py`** - `NotationBase` - Unified base class providing shared functionality: debug logging, key normalization (`_cast_key` converts camelCase/kebab-case/spaced keys to snake_case), magic methods (`__int__`, `__float__`, `__bool__`, `__repr__`, `__str__`), output formatting (`__call__` with format arguments), `_create_child` factory method with parent tracking, and the `_unwrap` static method for converting notation objects back to raw Python values.
- **`notation_primitive.py`** - `NotationPrimitive(NotationBase)` - Wraps primitive values (str, int, float, bool, None). Returns the raw value on `__call__()` and supports serialization to JSON/YAML/TOML element format.
- **`notation_proxy.py`** - `NotationProxy` - Lightweight proxy object returned when accessing missing keys on a `NotationObject`. Records parent chains and materializes intermediate dicts on assignment, enabling deep auto-creation patterns like `x.a.b.c = 1`. Behaves like `NotationPrimitive(None)` for read operations (returns `None` on call, is falsy).
- **`notation_structures.py`** - Contains `NotationObject(NotationBase)` for dict/object wrapping and `NotationArray(NotationBase)` for list/array wrapping. Both use lazy loading with smart caching. `NotationObject` supports `__setattr__`/`__delattr__` for mutation and returns `NotationProxy` for missing keys. `NotationArray` supports `__setitem__`/`__delitem__` for element mutation.
- **`notation_dumper.py`** - `NotationDumper(yaml.Dumper)` - Custom YAML dumper that formats output consistently, handling None values, multiline strings, and ordered dict output.
