import os
from google.appengine.api.app_identity import get_default_version_hostname, get_application_id

from secrets import SESSION_KEY

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG = True
    HOME_URL = 'http://localhost' + ':8085'
else:
    DEBUG = False
    HOME_URL = 'http://' + get_default_version_hostname()

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
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
                      'unsupported' : 'Unsupported API', 
                      'missing'     : 'Not all parameter present'}, 
               401 : 'Unauthorized', 
               402 : {'unconfirmed' : 'Email has not been confirmed.', 
                      'duplicate'   : 'User already exists.'},
               404 : 'Does not exist', 
               500 : {'generic'        : 'Server error', 
                      'admin_required' : 'Please contact application administrator for support'}}

# URLs
APP_ID = get_application_id()

COOKIE_TEMPLATE = { 'id'        : 0,     #session id
                    'pageviews' : 0, 
                    'authed'    : False, 
                    'active'    : True }

# Model that will be used to demo ReSTful APIs
SAMPLE_ENTITY = 'Widget'

DATE_FORMAT_HTML = "dd-mm-yyyy"
DATE_FORMAT = "%d-%m-%Y"

# Email Authentication
EMAIL_CONFIRM_BODY = """ 
Hello, %s!

Please click the link below to confirm your email address: 

%s

Thank you. 

""" 

EMAIL_SENDER = "ilya.bagrak@gmail.com"