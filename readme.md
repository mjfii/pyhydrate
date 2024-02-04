## PyHydrate
[![license](https://img.shields.io/github/license/mjfii/pyhydrate.svg)](https://github.com/mjdii/pyhydrate/blob/main/license)
[![pypi](https://img.shields.io/pypi/v/pyhydrate.svg)](https://pypi.python.org/pypi/pyhtdrate)
[![deploy](https://github.com/mjfii/pyhydrate/workflows/deploy-prod/badge.svg?event=push)](https://github.com/mjfii/pyhydrate/actions?query=workflow%3Adeploy-prod+event%3Apush+branch%3Amain)
[![downloads](https://static.pepy.tech/badge/pyhydrate/month)](https://pepy.tech/project/pyhydrate)
[![versions](https://img.shields.io/pypi/pyversions/pyhydrate.svg)](https://github.com/mjfii/pyhydrate)

Easily access your json, yaml, dicts, and/or list with dot notation.

`PyHydrate` is a JFDI approach to interrogating common data structures without worrying about `.get()`
methods or array slicing.  It is easy to use and errors are handled gracefully when trying to drill
to data elements that may not exist.  Additionally, data types are inferred, recursive depths are tracked, 
and key casting to snake case is mapped and managed.

### Installation
Install using `pip`
```bash
pip install pyhydrate
# or, if you would like to upgrade the library
pip install -U pyhydrate
```

### A Simple Example
```python
import pyhydrate as pyhy

_payload = {
    'queryStringParameters': {
        'someStringValue': 'string value 1',
        'aLogicalValue': True,
        'myValue': 12345.6
    },
    'requestContext': {
        'http': {
            'method': 'GET'
        }
    }
}

y = pyhy.PyHydrate(_payload)
x = y.request_context.http()
print(x)

z = y.request_context.http.method()
print(z)

idk = y.request_context.http.method.x()
print(idk)
```

### Nomenclature
- Structure: 
  - Object: 
  - Array: 
- Primitive:
  - String:
  - Integer:
  - Float:
  - None:
- Values:
  - Source:
  - Cleaned:
  - Hydrated:
- Element:
- Type:
- Map:

### Documentation
Coming Soon!

### Contributing
For guidance on setting up a development environment and how to make a
contribution to `PyHydrate`, see [CONTRIBUTING.md](./.github/CONTRIBUTING.md).
