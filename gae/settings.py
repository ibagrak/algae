import os

if 'SERVER_SOFTWARE' in os.environ:
    DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
else:
    DEBUG = False
    
COOKIE_KEY = 'randomize_me' # os.urandom(64)

APIS = {'test_api'} 
INVALID_API_ERROR = 1
GENERAL_ERROR     = 2
SUCCESS           = 200

ERROR_URL = '/error'
