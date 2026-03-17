# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
Run all tests (recommended approach):
```bash
python -m unittest discover -s tests/ -p "*_tests.py"
```

Run individual test files (if needed):
```bash
python -m unittest tests/dict_get_tests.py
python -m unittest tests/list_get_tests.py
python -m unittest tests/call_tests.py
python -m unittest tests/primitive_get_tests.py
python -m unittest tests/none_serialization_tests.py
python -m unittest tests/magic_methods_tests.py
python -m unittest tests/memory_efficiency_tests.py
python -m unittest tests/initialization_tests.py
python -m unittest tests/error_handling_tests.py
python -m unittest tests/array_edge_cases_tests.py
python -m unittest tests/repr_method_tests.py
python -m unittest tests/write_tests.py
python -m unittest tests/save_tests.py
python -m unittest tests/cloud_save_tests.py
python -m unittest tests/input_type_tests.py
python -m unittest tests/proxy_depth_tests.py
```

Run tests with verbose output:
```bash
python -m unittest discover -s tests/ -p "*_tests.py" -v
```

Run specific test class or method:
```bash
python -m unittest tests.call_tests.CallMethods.test_yaml_string
python -m unittest tests.error_handling_tests.TestErrorHandling
```

Run a single test file:
```bash
python -m unittest tests/dict_get_tests.py
```

### Code Quality
Check code style and quality:
```bash
# Linting (identify issues)
ruff check pyhydrate/ tests/

# Auto-fix issues (safe fixes only)
ruff check pyhydrate/ tests/ --fix

# Auto-fix with unsafe fixes (be careful)
ruff check pyhydrate/ tests/ --fix --unsafe-fixes

# Code formatting
ruff format pyhydrate/ tests/

# Check formatting without making changes
ruff format --check pyhydrate/ tests/

# Get linting statistics
ruff check pyhydrate/ tests/ --statistics
```

### Virtual Environment
Set up isolated development environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
# or .venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

### Building and Installation
Install in development mode (includes dev dependencies):
```bash
pip install -e ".[dev]"
```

Build the package:
```bash
python -m build
```

### Running Examples
Execute the main demo:
```bash
python demo.py
```

### Troubleshooting

**Common Development Issues:**

1. **Import Errors**: If you encounter module import errors, ensure you've installed the package in development mode:
   ```bash
   pip install -e .
   ```

2. **Test Failures**: If tests fail unexpectedly, try running them individually to isolate the issue:
   ```bash
   python -m unittest tests.specific_test_file.TestClass.test_method -v
   ```

3. **Linting Errors**: If ruff reports errors, use auto-fix for safe corrections:
   ```bash
   ruff check pyhydrate/ tests/ --fix
   ```

4. **Virtual Environment Issues**: If dependencies are not found, ensure your virtual environment is activated:
   ```bash
   source .venv/bin/activate  # Unix/macOS
   # or .venv\Scripts\activate  # Windows
   ```

5. **Debug Mode**: For troubleshooting data access issues, use debug mode:
   ```python
   from pyhydrate import PyHydrate
   data = PyHydrate(your_data, debug=True)
   result = data.some.nested.access()  # Will show detailed access logging
   ```

### TOML Support

PyHydrate supports TOML serialization via the 'toml' callable argument:

```python
from pyhydrate import PyHydrate

# Dictionary to TOML
data = PyHydrate({'database': {'host': 'localhost', 'port': 5432, 'name': 'mydb'}})
print(data('toml'))
# Output:
# [database]
# host = "localhost"
# port = 5432
# name = "mydb"

# Nested object to TOML
print(data.database('toml'))
# Output:
# host = "localhost"
# port = 5432
# name = "mydb"

# Primitive to TOML (wrapped in element format)
print(data.database.host('toml'))
# Output:
# str = "localhost"

# Lists are wrapped in a root table for TOML compatibility
list_data = PyHydrate([{'name': 'item1'}, {'name': 'item2'}])
print(list_data('toml'))
# Output:
# [[data]]
# name = "item1"
#
# [[data]]
# name = "item2"
```

**TOML Limitations:**
- None values are omitted (TOML specification requirement)
- Lists require wrapping in a root table
- Only dict-like structures can be serialized to TOML

## Project Architecture

PyHydrate is a Python library that enables dot notation access and mutation of nested data structures (dicts, lists, JSON, YAML, TOML) with graceful error handling, automatic key normalization, and file persistence.

### Architectural Principles

**Simplified Inheritance Hierarchy:**
- Single inheritance chain: `PyHydrate` → `NotationBase`
- All notation classes inherit directly from `NotationBase`
- `NotationProxy` is a standalone class (no inheritance from `NotationBase`)
- No circular inheritance or complex dependency chains

**Dependency Management:**
- Lazy imports to prevent circular dependencies
- TYPE_CHECKING guards for type hints
- Centralized type definitions in `pyhydrate/types.py`
- Forward references using string literals

**Clean Separation of Concerns:**
- `NotationBase`: Core functionality (magic methods, output formatting, key normalization, `_unwrap`, `_create_child`)
- `NotationObject`: Dictionary/object handling with lazy loading, mutation (`__setattr__`, `__delattr__`)
- `NotationArray`: List/array handling with lazy loading, mutation (`__setitem__`, `__delitem__`)
- `NotationPrimitive`: Primitive value handling
- `NotationProxy`: Lightweight proxy for deferred deep auto-creation of missing keys
- `PyHydrate`: Main entry point, orchestration, file I/O (`save`)

**Memory Efficiency Architecture:**
- Lazy loading for all nested structures (`NotationObject` and `NotationArray`)
- Memory-optimized `__slots__` in all notation classes
- On-demand computation of cleaned values via `@property`
- Smart caching with pre-computed key mappings
- Factory pattern for child object creation with parent tracking

**Write (Mutation) Architecture:**
- `__setattr__` on `NotationObject` and `PyHydrate` with internal attrs guard (`_INTERNAL_ATTRS` frozenset)
- Writes mutate `_raw_value` directly (single source of truth); `_cleaned_value` auto-reflects changes
- Key preservation: writing to a normalized key (e.g., `first_name`) updates the original-format key (e.g., `firstName`)
- `NotationProxy` enables deep auto-creation: `x.a.b.c = 1` creates intermediate dicts via proxy chain materialization
- Parent tracking (`_parent`, `_parent_key` slots) enables upward propagation from proxy to root
- Cache invalidation on write: only the specific key's `_hydrated_cache` entry is cleared

### Core Components

**Main Entry Point:**
- `pyhydrate/pyhydrate.py` - The `PyHydrate` class that serves as the main entry point, inheriting directly from `NotationBase`. Supports `save(path, output_format=, original_keys=)` for file persistence (local and cloud storage via `fsspec`) and auto-promotes to `NotationObject` on first write when constructed empty.

**Type Stubs (PEP 561):**
- `pyhydrate/pyhydrate.pyi` - Type stub declaring `__getattr__` returning `Any` so IDEs (PyCharm, VS Code) recognize dynamic dot notation access without flagging `__slots__` or unresolved attribute warnings.
- `pyhydrate/py.typed` - PEP 561 marker file signaling the package ships inline type information.
- Both files are included in the built package via `[tool.setuptools.package-data]` in `pyproject.toml`.

**Notation System Architecture:**
- `pyhydrate/notation/notation_base.py` - Unified base class providing all shared functionality including debug printing, key casting (camelCase/kebab-case to snake_case), common magic methods, representation formatting, `_unwrap()` static method, and `_create_child()` factory with parent tracking
- `pyhydrate/notation/notation_primitive.py` - Handles primitive values (str, int, float, bool, None)
- `pyhydrate/notation/notation_proxy.py` - Lightweight proxy for deep auto-creation of missing keys; records parent chain and materializes intermediate dicts on `__setattr__`; enforces configurable max chain depth (default 100, via `max_proxy_depth` kwarg) with `_proxy_depth`/`_proxy_max_depth` slots
- `pyhydrate/notation/notation_structures.py` - Contains `NotationObject` (dict wrapper with `__setattr__`/`__delattr__`) and `NotationArray` (list wrapper with `__setitem__`/`__delitem__`) classes
- `pyhydrate/notation/notation_dumper.py` - Custom YAML dumper for consistent output formatting
- `pyhydrate/types.py` - Centralized type definitions to avoid circular import dependencies

**Error Handling System:**
- `pyhydrate/exceptions/` - Custom warning classes following one-class-per-module standard
  - `pyhydrate_warning.py` - Base warning class for all PyHydrate operations
  - `type_conversion_warning.py` - Warnings for type conversion issues
  - `access_pattern_warning.py` - Warnings for invalid access attempts
  - `api_usage_warning.py` - Warnings for incorrect API usage
  - `immutable_conversion_warning.py` - Warnings when immutable types (tuple, frozenset) are converted to mutable list
  - `format_warning_message.py` - Standardized warning message formatting utility
- `pyhydrate/error_handling.py` - Centralized error handling utilities and logging setup

### Key Features

**Automatic Data Type Detection:**
- JSON/YAML/TOML string parsing in constructor
- Parsing order: JSON → TOML → YAML for string inputs
- Iterable conversion: `set`, `frozenset`, `tuple`, `range` → `list` (immutable types emit `ImmutableConversionWarning`)
- Unsupported types raise `TypeError` with actionable message
- Recursive wrapping of nested structures
- Type-specific handling for primitives vs structures

**Key Normalization:**
- Converts camelCase, PascalCase, kebab-case, and "spaced keys" to snake_case
- Uses regex pattern matching for consistent key transformation
- Maintains mapping between original and cleaned keys

**Dot Notation Access (Read):**
- `__getattr__` enables `obj.key` access
- `__getitem__` enables `obj[index]` access for arrays
- Missing keys return `NotationProxy` (behaves like None for reads, supports writes)

**Dot Notation Mutation (Write):**
- `__setattr__` on `NotationObject`/`PyHydrate` for `obj.key = value`
- `__setitem__` on `NotationArray`/`PyHydrate` for `obj[index] = value`
- `__delattr__` on `NotationObject`/`PyHydrate` for `del obj.key`
- `__delitem__` on `NotationArray`/`PyHydrate` for `del obj[index]`
- Deep auto-creation via `NotationProxy` chain: `x.a.b.c = 1`
- Auto-promotion from primitive to `NotationObject` on first write

**File Persistence:**
- `save(path=None, *, output_format=None, original_keys=False)` on `PyHydrate`
- Format detected from file extension (`.json`, `.yaml`, `.yml`, `.toml`)
- Explicit `output_format` parameter overrides extension detection
- `_source_path` stored from constructor's `path=` parameter; `save()` with no args writes back
- Cloud storage support via `fsspec`: S3 (`s3://`), GCS (`gs://`, `gcs://`), ADLS (`abfs://`, `abfss://`, `az://`)
- Remote path detection via `_is_remote_path()` and `_REMOTE_SCHEMES` frozenset
- `_write_remote()` lazy-imports `fsspec` and writes via `fsspec.open()`; raises `ImportError` with install hint if missing
- Optional extras in `pyproject.toml`: `s3`, `azure`, `gcs`, `cloud`

**Output Formats:**
- Call with no args or 'value': returns cleaned value
- Call with 'element': returns `{type: value}` dict
- Call with 'type': returns Python type
- Call with 'json'/'yaml'/'toml': returns formatted string
- Call with 'depth': returns recursion depth
- Call with 'map': returns key mapping

**Standardized Error Handling:**
- Custom warning classes for different error types (type conversion, access patterns, API usage)
- Consistent warning message formatting with suggestions for fixing issues
- Structured logging system with configurable debug levels
- Graceful error handling with informative warnings instead of crashes
- Users can filter warnings by specific types for better error management

**Debug Mode:**
- Pass `debug=True` to constructor for detailed traversal logging
- Shows recursion depth, operation type, and value access
- Structured logging replaces print statements for better control

### Data Flow (Lazy Loading Architecture)
1. Input → `PyHydrate` constructor detects type (dict/list/primitive)
2. Raw value stored → Key mappings pre-computed (snake_case normalization)
3. **Lazy hydration**: Child objects created only on first access
4. Access via dot notation triggers `__getattr__` → cache lookup or lazy creation
5. Missing keys → `NotationProxy` returned (not cached; supports write-through)
6. **Smart caching**: Subsequent access of existing keys returns cached objects
7. Cleaned values computed on-demand via `@property` when requested
8. Terminal access returns wrapped primitive or structure
9. **Writes**: `__setattr__` mutates `_raw_value` directly, invalidates cache entry
10. **Deep writes**: Proxy chain materializes intermediate dicts and delegates to root parent

**Memory Benefits:**
- ~67% memory reduction (eliminates eager hydration of all children)
- Only accessed paths consume memory for hydrated objects
- Key mappings cached separately from object instances

### Test Structure
- `tests/dict_get_tests.py` - Dictionary access patterns
- `tests/list_get_tests.py` - Array/list access patterns
- `tests/call_tests.py` - Method call functionality (yaml, json, toml, type, etc.)
- `tests/primitive_get_tests.py` - Primitive value handling
- `tests/none_serialization_tests.py` - None value serialization in YAML/JSON/TOML formats
- `tests/magic_methods_tests.py` - Magic methods (`__int__`, `__float__`, `__bool__`) functionality
- `tests/memory_efficiency_tests.py` - Lazy loading and memory optimization validation
- `tests/error_handling_tests.py` - Standardized error handling and warning system validation
- `tests/initialization_tests.py` - Comprehensive initialization tests for all supported input types (primitives, dicts, lists, JSON, YAML, TOML)
- `tests/array_edge_cases_tests.py` - Array edge cases, bounds checking, and error handling
- `tests/repr_method_tests.py` - `__repr__` method functionality and warning prevention
- `tests/write_tests.py` - Write (mutation) support: setting existing/new keys, deep auto-creation, creating from scratch, array mutation, deletion, key normalization on write, serialization after mutation
- `tests/save_tests.py` - File save/write functionality: saving to JSON/YAML/TOML, round-trip, source path save-back, format override
- `tests/cloud_save_tests.py` - Cloud storage save functionality: remote path detection, format detection from remote URIs, mocked fsspec integration, ImportError handling, local path isolation
- `tests/input_type_tests.py` - Input type validation: conversion of set/frozenset/tuple/range to list, ImmutableConversionWarning, TypeError for unsupported types, serialization and mutation after conversion, regression tests
- `tests/proxy_depth_tests.py` - Proxy chain depth limiting: default depth of 100, custom max_proxy_depth via kwargs, depth tracking through __getattr__/__getitem__, error messages, write-through within limits
- Test data located in `pyhydrate/data/` as JSON, YAML, and TOML files

**Test Discovery:** All test files follow the `*_tests.py` naming pattern and are automatically discovered by the CI system.

## Development Best Practices

### Code Quality Standards
This codebase follows modern Python development practices:

**Linting and Formatting:**
- Uses `ruff` for both linting and formatting (configured in `pyproject.toml` under `[tool.ruff]`)
- Code is automatically formatted for consistency
- **All linting issues resolved**: Zero remaining lint errors
- All functions have proper type annotations including `*args`, `**kwargs`, and return types
- Modern Python patterns: uses `pathlib.Path.read_text()`, keyword-only parameters, and proper type comparisons

**Testing Standards:**
- Comprehensive test coverage with 308 tests across 16 test files
- Uses unittest framework with modern `assert` statements
- All tests pass after linting and formatting improvements
- Test data is organized in dedicated `pyhydrate/data/` directory
- Uses `pathlib.Path.read_text()` for file operations in tests
- Automated test discovery in CI ensures all new test files are included automatically
- Memory efficiency tests validate lazy loading behavior
- Initialization tests validate all supported input formats including TOML

**Import Organization:**
- All imports are properly sorted and organized
- Explicit re-exports with `__all__` declarations in `__init__.py` files
- No unused imports (F401 errors resolved)
- Uses lazy imports and TYPE_CHECKING guards to prevent circular dependencies
- Centralized type definitions in `pyhydrate/types.py`

### Common Development Tasks

**Before Making Changes:**
1. Always run the full test suite: `python -m unittest discover -s tests/ -p "*_tests.py"`
2. Check code quality: `ruff check pyhydrate/ tests/`
3. Format code: `ruff format pyhydrate/ tests/`

**When Adding New Features:**
- Follow the existing notation class pattern in `pyhydrate/notation/` directory
- Add corresponding tests in the `tests/` directory following the `*_tests.py` naming convention
- Use the debug parameter for development: `PyHydrate(data, debug=True)`
- Ensure new code follows the established type annotation patterns
- Test data files should be placed in `pyhydrate/data/` directory for consistency
- Follow the one-class-per-module standard (see `pyhydrate/exceptions/` for example)

**When Adding New Tests:**
- Test files must end with `_tests.py` for automatic discovery
- Inherit from `unittest.TestCase` for consistency with existing tests
- Use `setUp()` and `tearDown()` methods for test fixtures when needed
- Test both positive and negative cases (valid and invalid inputs)
- Include error handling tests for new warning types or error conditions

**Key Implementation Notes:**
- None handling is properly implemented in YAML/JSON/TOML serialization
- Magic methods (`__int__`, `__float__`, `__bool__`) enable natural type conversion with proper error handling
- Debug mode provides detailed traversal logging for troubleshooting
- The `_cast_key` method handles automatic key normalization (camelCase → snake_case)
- Error handling uses a mix of warnings and graceful failures (returns proxy for missing keys)
- Type annotations are comprehensive including Union types, Any for dynamic parameters, and ClassVar for class attributes
- Uses modern Python patterns: keyword-only parameters, `is` for type comparisons, pathlib for file operations
- Simplified inheritance hierarchy: all classes inherit directly from `NotationBase` (no circular inheritance)
- `NotationProxy` is a standalone class (not inheriting from `NotationBase`) for minimal overhead
- Lazy imports prevent circular dependencies between notation classes
- Centralized type system in `types.py` for clean dependency management
- `__setattr__` uses `_INTERNAL_ATTRS` frozenset guard to distinguish slot writes from data writes
- Writes go to `_raw_value` directly; `_cleaned_value` is computed on demand so it auto-reflects changes
- `NotationProxy` is never cached in `_hydrated_cache` to ensure post-materialization access creates proper objects
- `NotationProxy` enforces max chain depth via `_proxy_depth`/`_proxy_max_depth` slots; default 100, configurable via `max_proxy_depth` kwarg
- Constructor converts `set`/`frozenset`/`tuple`/`range` to `list`; immutable types emit `ImmutableConversionWarning`; unsupported types raise `TypeError`

### Known Issues & Limitations
- TODO comments indicate areas for future enhancement

### Recently Completed Features
- ✅ **Write (Mutation) Support**: Full dot-notation write support with `__setattr__`/`__setitem__`/`__delattr__`/`__delitem__`, deep auto-creation via `NotationProxy` chain, auto-promotion from empty to dict, and file persistence via `save()` method
- ✅ **TOML Callable Argument Support**: Added 'toml' as a callable argument option with comprehensive serialization support, error handling, and tests
- ✅ **Standardized Error Handling (Issue #28)**: Implemented comprehensive error handling strategy with custom warning classes, structured logging, and consistent error patterns across the entire codebase
- ✅ **Error Handling for Invalid Call Types (Issue #25)**: Implemented proper warning system for invalid call types with comprehensive tests and updated documentation
- ✅ **Memory Efficiency (Issue #30)**: Implemented lazy loading architecture with ~67% memory reduction, `__slots__` optimization, and smart caching
- ✅ **Architecture Refactoring (Issue #29)**: Simplified inheritance hierarchy from 4 levels to 2, eliminated circular dependencies, merged NotationRepresentation into NotationBase
- ✅ **Magic Methods (Issue #24)**: Full implementation of `__int__`, `__float__`, and `__bool__` magic methods with comprehensive error handling and 35 test cases
- ✅ **Code Quality**: All linting issues resolved, code formatting standardized
- ✅ **CI Enhancement**: Added automated linting and formatting checks to GitHub Actions workflows
- ✅ **Documentation**: Added comprehensive Mermaid diagrams showing class hierarchy, data flow, and dependency management
- ✅ **PEP 561 Type Stubs**: Added `py.typed` marker and `pyhydrate.pyi` stub to resolve PyCharm/IDE `__slots__` and unresolved attribute inspections for dynamic dot notation access
- ✅ **Cloud Storage Save**: `save()` supports remote URIs (`s3://`, `gs://`, `abfss://`) via `fsspec` with optional extras (`pip install pyhydrate[cloud]`). Lazy-imports fsspec to keep the core dependency-free.
- ✅ **Input Type Validation (Issue #1)**: Constructor now accepts `set`, `frozenset`, `tuple`, and `range` (converted to `list`). Immutable types emit `ImmutableConversionWarning`. Unsupported types raise `TypeError` with actionable message. 51 tests across 10 test classes.
- ✅ **Proxy Depth Limiting (Issue #3)**: `NotationProxy` enforces configurable max chain depth (default 100) via `max_proxy_depth` kwarg, preventing unbounded memory allocation from runaway attribute access. 18 tests across 7 test classes.
- ✅ **Thread Safety Documentation (Issue #4)**: Added "Thread Safety" section to `readme.md` documenting that instances are not thread-safe, with recommended `threading.Lock` pattern for shared access.

### Continuous Integration
The project uses GitHub Actions for automated testing:

**Workflows:**
- `.github/workflows/prod-tests.yml` - Tests and linting on `main` branch pushes (production CI)
- `.github/workflows/stage-tests.yml` - Tests and linting on `stage` branch pull requests
- `.github/workflows/version-deployment.yml` - CD pipeline triggered on GitHub release publication; updates version in `pyproject.toml`, builds, and publishes to PyPI

**Quality Checks in CI:**
- `ruff check pyhydrate/ tests/` - Code quality linting
- `ruff format --check pyhydrate/ tests/` - Code formatting validation
- Both checks run before tests to ensure code quality

**Test Discovery Automation:**
- CI uses `python -m unittest discover -s tests/ -p "*_tests.py"` for automatic test file detection
- New test files following the `*_tests.py` pattern are automatically included
- No need to manually update CI configuration when adding new test files
- Runs all 308 tests across 16 test files on every push

### Ruff Configuration
The project uses a comprehensive ruff configuration in `pyproject.toml` (under `[tool.ruff]`) with:
- **Target**: Python 3.8+ compatibility
- **Line length**: 88 characters (Black-compatible)
- **Enabled rules**: Extensive rule set covering style, imports, security, performance
- **Ignored rules**: Selective ignores for project-specific needs including:
  - Print statements (T201) - allowed for debug output
  - TODO comments (FIX002) - allowed for development notes
  - unittest.assertRaises (PT027) - project uses unittest, not pytest
  - Magic value comparisons (PLR2004) - allowed in tests
- **Per-file ignores**: Test files have relaxed rules for magic values and assertions; library internals have SLF001 (private member access) suppressed for cross-module internal access; `.pyi` type stubs have UP007 suppressed to allow `Union[]` syntax for PyCharm/IDE compatibility

Current status: **All linting issues resolved** ✅

The codebase passes all ruff checks with zero linting errors.
