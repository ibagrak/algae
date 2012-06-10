import os
from google.appengine.api.app_identity import get_default_version_hostname, get_application_id

if 'SERVER_SOFTWARE' in os.environ:
    DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
    HOME_URL = 'http://localhost'
else:
    DEBUG = False
    HOME_URL = 'http://' + get_default_version_hostname()

# webapp2 config
config = {}
config['webapp2_extras.sessions'] = {
    # Randomize cookie key with os.urandom(64). Do it offline and copy the string here. 
    'secret_key': 'l\xd5q\xa1t\x01\xbc\x9e\xf2\xfa\xaf\x1f\xfe\x06\xcey\x08\xfc\xda\xe9"\xa6@#E^}\xf3F.\xeb\xd7\x82\x1bh\xd5\xea\xcf-\x19\xdb\xa2\xd6N\xae\x11\x13\xff!\xe24\xf6\x1c\x00\x1f\xd0\xaf\xcf\xf1\xbb\x04\xe7u;',
}



# List of valid APIs
APIS = frozenset({'test_api'})

# Common errors
INVALID_API_ERROR = 1
GENERAL_ERROR     = 2
SUCCESS           = 200


# URLs
ERROR_PATH = '/404.html'
APP_ID = get_application_id()

cookie = { 'id'        : 0,     #session id
           'pageviews' : 0, 
           'authed'    : False, 
           'active'    : True }
