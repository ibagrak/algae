'''
Created on Aug 6, 2012

@author: ibagrak
'''
import datetime, re
import hashlib
import urllib
from google.appengine.ext import ndb

import settings

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
    output = {}

    for key, prop in model._properties.iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to ms-since-epoch ("new Date()").
            output[key] = value.strftime(settings.DATE_FORMAT)
            #ms = time.mktime(value.utctimetuple())
            #ms += getattr(value, 'microseconds', 0) / 1000
            #output[key] = int(ms)
        elif isinstance(value, ndb.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, ndb.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    output['id'] = model.key.integer_id()
    return output

def to_gravatar_url(email): 
    return "http://www.gravatar.com/avatar/" + hashlib.md5(email).hexdigest() + "?d=" + urllib.quote(settings.HOME_URL + '/img/algae.png')

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE) # domain

