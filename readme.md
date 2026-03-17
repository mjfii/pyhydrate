# PyHydrate

[![license](https://img.shields.io/github/license/mjfii/pyhydrate.svg)](https://github.com/mjfii/pyhydrate/blob/main/license)
[![pypi](https://img.shields.io/pypi/v/pyhydrate.svg)](https://pypi.python.org/pypi/pyhydrate)
[![ci](https://github.com/mjfii/pyhydrate/actions/workflows/prod-tests.yml/badge.svg)](https://github.com/mjfii/pyhydrate/actions/workflows/prod-tests.yml)
[![downloads](https://static.pepy.tech/badge/pyhydrate/month)](https://pepy.tech/project/pyhydrate)
[![versions](https://img.shields.io/pypi/pyversions/pyhydrate.svg)](https://github.com/mjfii/pyhydrate)

Easily access and mutate your JSON, YAML, TOML, dicts, and lists with dot notation.

`PyHydrate` provides a simple way to read and write nested data structures without worrying about `.get()` methods, defaults, or array slicing. It handles errors gracefully when accessing data elements that may not exist, with automatic key normalization and type inference. You can also create structures from scratch, mutate existing ones, and save them back to files.

## Repository Structure

```
pyhydrate/
├── .github/
│   ├── CODEOWNERS
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── CONTRIBUTORS.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── documentation_need.md
│   │   └── feature_request.md
│   └── workflows/
│       ├── prod-tests.yml
│       ├── stage-tests.yml
│       └── version-deployment.yml
├── pyhydrate/
│   ├── __init__.py
│   ├── pyhydrate.py
│   ├── pyhydrate.pyi
│   ├── py.typed
│   ├── error_handling.py
│   ├── types.py
│   ├── data/
│   │   ├── basic-dict-get.json
│   │   ├── basic-list-get.json
│   │   ├── init-test-data.json
│   │   ├── init-test-data.toml
│   │   └── init-test-data.yaml
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── pyhydrate_warning.py
│   │   ├── type_conversion_warning.py
│   │   ├── access_pattern_warning.py
│   │   ├── api_usage_warning.py
│   │   └── format_warning_message.py
│   └── notation/
│       ├── __init__.py
│       ├── notation_base.py
│       ├── notation_primitive.py
│       ├── notation_proxy.py
│       ├── notation_structures.py
│       └── notation_dumper.py
├── tests/
│   ├── __init__.py
│   ├── array_edge_cases_tests.py
│   ├── call_tests.py
│   ├── cloud_save_tests.py
│   ├── dict_get_tests.py
│   ├── error_handling_tests.py
│   ├── initialization_tests.py
│   ├── list_get_tests.py
│   ├── magic_methods_tests.py
│   ├── memory_efficiency_tests.py
│   ├── none_serialization_tests.py
│   ├── primitive_get_tests.py
│   ├── repr_method_tests.py
│   ├── save_tests.py
│   └── write_tests.py
├── claude.md
├── demo.py
├── license
├── pyproject.toml
└── readme.md
```

## Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)

Optional (for development):

- **ruff** for linting and formatting: `pip install ruff`
- **gh CLI** for GitHub operations: `brew install gh` (macOS) or see [cli.github.com](https://cli.github.com)

## Installation

```bash
pip install pyhydrate
```

**Optional cloud storage support** (for saving to S3, GCS, or Azure Data Lake):

```bash
pip install pyhydrate[s3]      # Amazon S3
pip install pyhydrate[gcs]     # Google Cloud Storage
pip install pyhydrate[azure]   # Azure Data Lake Storage
pip install pyhydrate[cloud]   # All cloud providers
```

**Dependencies**: PyHydrate automatically handles TOML support:
- **Python 3.11+**: Uses built-in `tomllib`
- **Python < 3.11**: Automatically installs `tomli` for TOML support

### Development Setup

```bash
git clone https://github.com/mjfii/pyhydrate.git
cd pyhydrate
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
# or .venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

## Quick Start

```python
from pyhydrate import PyHydrate

# Works with nested dictionaries
data = {
    "user-info": {
        "firstName": "John",
        "contact_details": {
            "email": "john@example.com",
            "phone": "555-0123"
        }
    }
}

py_data = PyHydrate(data)

# Access with dot notation - keys are automatically normalized
print(py_data.user_info.first_name())  # "John"
print(py_data.user_info.contact_details.email())  # "john@example.com"

# Graceful handling of missing data
print(py_data.user_info.missing_field())  # None
```

## Features

### Automatic Format Detection
Load data from JSON, YAML, or TOML strings - format is detected automatically:

```python
# JSON string
json_config = '{"database": {"host": "localhost", "port": 5432}}'
config = PyHydrate(json_config)

# TOML string
toml_config = '''
[database]
host = "localhost"
port = 5432
'''
config = PyHydrate(toml_config)

# YAML string
yaml_config = '''
database:
  host: localhost
  port: 5432
'''
config = PyHydrate(yaml_config)

print(config.database.host())  # "localhost" (works with all formats)
```

### File Loading
Load data directly from files:

```python
# Supports .json, .yaml, .yml, and .toml files
config = PyHydrate(path="config.json")
settings = PyHydrate(path="settings.yaml")
project = PyHydrate(path="pyproject.toml")
```

### Key Normalization
Automatically converts different key formats to snake_case:

```python
data = {
    "firstName": "John",
    "last-name": "Doe",
    "Email Address": "john@example.com"
}

py_data = PyHydrate(data)
print(py_data.first_name())      # "John"
print(py_data.last_name())       # "Doe"
print(py_data.email_address())   # "john@example.com"
```

### Multiple Output Formats

```python
py_data = PyHydrate({"user": {"name": "John", "age": 30}})

# Different output formats
print(py_data.user())           # Returns the cleaned Python object
print(py_data.user('json'))     # Returns JSON string
print(py_data.user('yaml'))     # Returns YAML string
print(py_data.user('toml'))     # Returns TOML string
print(py_data.user('type'))     # Returns Python type
print(py_data.user('element'))  # Returns {"dict": {...}}
```

### Array Access
Handle lists and nested arrays easily:

```python
data = {
    "users": [
        {"name": "John", "age": 30},
        {"name": "Jane", "age": 25}
    ]
}

py_data = PyHydrate(data)
print(py_data.users[0].name())  # "John"
print(py_data.users[1].age())   # 25
```

### Write Support (Mutation)

Set values via dot notation, create structures from scratch, and save to files:

```python
# Modify existing data
data = PyHydrate({"name": "Alice", "age": 25})
data.name = "Bob"
data.email = "bob@example.com"
print(data())  # {"name": "Bob", "age": 25, "email": "bob@example.com"}

# Create from scratch with deep auto-creation
config = PyHydrate()
config.database.host = "localhost"
config.database.port = 5432
print(config('json'))
# {"database": {"host": "localhost", "port": 5432}}

# Delete keys
del data.age
print(data())  # {"name": "Bob", "email": "bob@example.com"}

# Mutate arrays
items = PyHydrate([1, 2, 3])
items[1] = 99
del items[0]
print(items())  # [99, 3]

# Save to file (format detected from extension)
data.save("output.json")
data.save("output.yaml")
data.save("output.toml")

# Save to cloud storage (requires optional extras)
data.save("s3://my-bucket/config.json")
data.save("gs://my-bucket/config.yaml")
data.save("abfss://container@account.dfs.core.windows.net/config.json")

# Round-trip: load, modify, save back
config = PyHydrate(path="config.json")
config.database.port = 3306
config.save()  # Saves back to the original file
```

### Debug Mode
Get detailed access logging:

```python
data = {"level1": {"level2": {"value": "test"}}}
py_data = PyHydrate(data, debug=True)

print(py_data.level1.level2.value())
# Debug output shows the access path and depth
```

## Error Handling

PyHydrate uses graceful error handling - invalid access returns None instead of raising exceptions:

```python
from pyhydrate import PyHydrate

# Invalid access returns None instead of failing
data = PyHydrate({"valid": "data"})
result = data.invalid.deeply.nested.access()  # Returns None, no exception
print(result)  # None

# Works with arrays too
data = PyHydrate({"items": [1, 2, 3]})
result = data.items[10]()  # Index out of range - returns None
print(result)  # None
```

For advanced error handling with warnings:

```python
import warnings
from pyhydrate import PyHydrate, PyHydrateWarning

# This will generate a PyHydrateWarning for invalid API usage
data = PyHydrate({"test": "value"})
result = data("invalid_format")  # APIUsageWarning: Call type 'invalid_format' not supported
print(result)  # None

# Filter warnings to suppress them
warnings.filterwarnings("ignore", category=PyHydrateWarning)
result = data("invalid_format")  # Same call, but no warning shown
print(result)  # None (still works, just silent)
```

## Type Conversion

Convert PyHydrate objects to Python primitives:

```python
data = PyHydrate({"count": "42", "price": "19.99", "active": "true"})

# Use Python's built-in type conversion
count = int(data.count())      # 42
price = float(data.price())    # 19.99
is_active = bool(data.active()) # True
```

## License

This project is licensed under the MIT License - see the [LICENSE](license) file for details.

## Demo

See a comprehensive demonstration of all PyHydrate features:

```bash
python demo.py
```

This interactive demo showcases:
- Complex data structures with mixed key formats
- All output formats (JSON, YAML, TOML, element, type, map, depth)
- Array access and negative indexing
- String format detection and file loading
- Graceful error handling and warning system
- Magic methods and type conversion
- Write/mutation via dot notation (set, delete, deep auto-creation)
- File save/persistence with round-trip support
- Lazy loading performance with actual proof
- Complete feature overview

## Contributing

For development setup, testing guidelines, and contribution instructions, see [CONTRIBUTING.md](.github/CONTRIBUTING.md).
