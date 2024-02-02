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

y = pyhy.PyHydrate(_payload, debug=False)
x = y.request_context('element')

print(y)

# print(x, '\n')
#
# z = y.request_context.http.method('type')
# print(z, '\n')
#
# idk = y.query_string_parameters
# print(idk, '\n')


# TODO: move required items to note_rep
# TODO: build out the map logic
