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


#200 OK - Everything worked as expected.
#400 Bad Request - Often missing a required parameter.
#401 Unauthorized - No valid API key provided.
#402 Request Failed - Parameters were valid but request failed.
#404 Not Found - The requested item doesn't exist.
#500, 502, 503, 504 Server errors - something went wrong on Stripe's end.

API_CODES  = { 200 : 'Success', 
               400 : {'email'       : 'Invalid email address', 
                      'password'    : 'Invalid password', 
                      'email_password' : 'Invalid email or password', 
                      'unsupported' : 'Unsupported API'}, 
               401 : 'Unauthorized', 
               402 : {'unconfirmed' : 'Email has not been confirmed.', 
                      'duplicate'   : 'User already exists.'},
               404 : 'Does not exist', 
               500 : {'generic'        : 'Server error', 
                      'admin_required' : 'Please contact application administrator for support'}}

# URLs
ERROR_PATH = '/404.html'
APP_ID = get_application_id()

COOKIE_TEMPLATE = { 'id'        : 0,     #session id
                    'pageviews' : 0, 
                    'authed'    : False, 
                    'active'    : True }
