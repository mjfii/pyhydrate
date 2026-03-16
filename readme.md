# PyHydrate

[![license](https://img.shields.io/github/license/mjfii/pyhydrate.svg)](https://github.com/mjfii/pyhydrate/blob/main/license)
[![pypi](https://img.shields.io/pypi/v/pyhydrate.svg)](https://pypi.python.org/pypi/pyhydrate)
[![ci](https://github.com/mjfii/pyhydrate/actions/workflows/prod-tests.yml/badge.svg)](https://github.com/mjfii/pyhydrate/actions/workflows/prod-tests.yml)
[![downloads](https://static.pepy.tech/badge/pyhydrate/month)](https://pepy.tech/project/pyhydrate)
[![versions](https://img.shields.io/pypi/pyversions/pyhydrate.svg)](https://github.com/mjfii/pyhydrate)

Easily access your JSON, YAML, TOML, dicts, and lists with dot notation.

`PyHydrate` provides a simple way to access nested data structures without worrying about `.get()` methods, defaults, or array slicing. It handles errors gracefully when accessing data elements that may not exist, with automatic key normalization and type inference.

## Installation

```bash
pip install pyhydrate
```

**Dependencies**: PyHydrate automatically handles TOML support:
- **Python 3.11+**: Uses built-in `tomllib` 
- **Python < 3.11**: Automatically installs `tomli` for TOML support

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
- All output formats (JSON, YAML, TOML, element, type)
- Array access and negative indexing
- String format detection and file loading
- Graceful error handling and warning system
- Magic methods and type conversion
- Lazy loading performance with actual proof
- Complete feature overview

## Contributing

For development setup, testing guidelines, and contribution instructions, see [CONTRIBUTING.md](.github/CONTRIBUTING.md).