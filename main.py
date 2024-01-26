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
