# pyhydrate

Core library package for PyHydrate. Contains the main entry point, notation system, error handling, and type definitions.

## Files

- **`__init__.py`** - Package entry point; re-exports `PyHydrate`, warning classes (`PyHydrateWarning`, `APIUsageWarning`, `AccessPatternWarning`, `TypeConversionWarning`), and notation classes (`NotationPrimitive`, `NotationArray`, `NotationObject`).
- **`pyhydrate.py`** - The `PyHydrate` class. Main entry point that accepts dicts, lists, JSON/YAML/TOML strings, or file paths and wraps them for dot notation access. Supports mutation via `__setattr__`/`__setitem__`, deletion via `__delattr__`/`__delitem__`, and file persistence via `save(path, output_format=, original_keys=)`. Supports saving to local files and remote cloud storage (S3, GCS, ADLS) via `fsspec`. Auto-promotes to `NotationObject` on first write when constructed empty. Inherits from `NotationBase`.
- **`pyhydrate.pyi`** - PEP 484 type stub for the `PyHydrate` class. Declares `__getattr__` returning `Any` so IDEs (PyCharm, VS Code) recognize dynamic dot notation access instead of flagging unresolved attributes or `__slots__` violations.
- **`py.typed`** - PEP 561 marker file (empty). Signals to type checkers and IDEs that the package ships inline type information.
- **`error_handling.py`** - Centralized error handling utilities including `log_and_warn()` for structured logging and warning dispatch, and `setup_logger()` for configurable debug logging.
- **`types.py`** - Centralized type definitions (`NotationTypes`, `StructureTypes`, `WrappableTypes`) used across the package to avoid circular import dependencies.

## Subdirectories

- **`data/`** - Test data files in JSON, YAML, and TOML formats.
- **`exceptions/`** - Custom warning classes following one-class-per-module standard.
- **`notation/`** - Notation system classes for wrapping primitives, dicts, and lists with dot notation access and write support.
