# pyhydrate

Core library package for PyHydrate. Contains the main entry point, notation system, error handling, and type definitions.

## Files

- **`__init__.py`** - Package entry point; re-exports `PyHydrate`, warning classes (`PyHydrateWarning`, `APIUsageWarning`, `AccessPatternWarning`, `TypeConversionWarning`), and notation classes (`NotationPrimitive`, `NotationArray`, `NotationObject`).
- **`pyhydrate.py`** - The `PyHydrate` class. Main entry point that accepts dicts, lists, JSON/YAML/TOML strings, or file paths and wraps them for dot notation access. Inherits from `NotationBase`.
- **`error_handling.py`** - Centralized error handling utilities including `log_and_warn()` for structured logging and warning dispatch, and `setup_logger()` for configurable debug logging.
- **`types.py`** - Centralized type definitions (`NotationType`, `RawValue`, `CleanedValue`) used across the package to avoid circular import dependencies.

## Subdirectories

- **`data/`** - Test data files in JSON, YAML, and TOML formats.
- **`exceptions/`** - Custom warning classes following one-class-per-module standard.
- **`notation/`** - Notation system classes for wrapping primitives, dicts, and lists with dot notation access.
