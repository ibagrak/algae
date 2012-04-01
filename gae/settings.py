import os

config = {}
config['webapp2_extras.sessions'] = {
    # Randomize cookie key with os.urandom(64). Do it offline and copy the string here. 
    'secret_key': 'l\xd5q\xa1t\x01\xbc\x9e\xf2\xfa\xaf\x1f\xfe\x06\xcey\x08\xfc\xda\xe9"\xa6@#E^}\xf3F.\xeb\xd7\x82\x1bh\xd5\xea\xcf-\x19\xdb\xa2\xd6N\xae\x11\x13\xff!\xe24\xf6\x1c\x00\x1f\xd0\xaf\xcf\xf1\xbb\x04\xe7u;',
}

if 'SERVER_SOFTWARE' in os.environ:
    DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
else:
    DEBUG = False

# List of valid APIs
APIS = frozenset({'test_api'})

# Common errors
INVALID_API_ERROR = 1
GENERAL_ERROR     = 2
SUCCESS           = 200

# Configurable URLs
ERROR_URL = '/error'

cookie = { 'pageviews' : 0, 
           'authed'    : False }
