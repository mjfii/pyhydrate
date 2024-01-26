## PyHydrate

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

### Contributing

For guidance on setting up a development environment and how to make a
contribution to `pyhydrate`, see []().
