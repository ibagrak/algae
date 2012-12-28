'''
Created on Mar 29, 2012

@author: ibagrak
'''
import logging
from datetime import datetime
from webapp2_extras import json

import settings
import utils
import re

from google.appengine.ext import ndb

class UnsupportedFieldTypeError(Exception): pass
class InvalidFieldValueError(Exception): pass

# subclass of StringProperty for more specific handling
class SpecificStringProperty(ndb.StringProperty):
    _css_class = None
    _re_prog = None
    _attributes = ndb.StringProperty._attributes + ['_css_class','_re_pattern']

    @ndb.utils.positional(1 + ndb.StringProperty._positional)
    def __init__(self, name=None, css_class=None, re_pattern=None, **kwds):
        super(ndb.StringProperty, self).__init__(name=name, **kwds)
        if re_pattern != None:
            self._re_prog = re.compile(re_pattern)
        self._css_class = css_class

    def _validate(self, value):
        if self._re_prog != None:
            if self._re_prog.match(value) == None:
                raise datastore_errors.BAdValueError('Does not match regexp')

# helper subclasses
class EmailProperty(SpecificStringProperty):
    _re_prog = re.compile('^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]+$', re.I)
    _css_class = 'email'

class LinkProperty(SpecificStringProperty):
    _re_prog = re.compile('^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$', re.I)
    _css_class = 'url'

class RESTModel(ndb.Model):
    # implemented by subclasses
    @classmethod
    def validate(cls, kvs):
        pass
    
    # returns an entity based on id
    @classmethod
    def get(cls, i):
        return cls.get_by_id(i)
    
    # creates a new entity
    @classmethod
    def put1(cls, kvs, entity = None):
        
        # prevent malicious overwriting of system attrs
        for k in kvs.keys(): 
            if not k in cls._properties:
                del kvs[k]
                continue
            
            v = cls.__dict__[k]
            
            # convert unicode values to datastore value types
            if isinstance(v, ndb.IntegerProperty): 
                kvs[k] = int(kvs[k])
            elif isinstance(v, ndb.FloatProperty):
                kvs[k] = float(kvs[k])
            elif isinstance(v, ndb.BooleanProperty):
                kvs[k] = True if kvs[k] == 'True' else False
            elif isinstance(v, ndb.TextProperty):
                kvs[k] = kvs[k]
            elif isinstance(v, ndb.DateProperty):
                kvs[k] = datetime.strptime(kvs[k], settings.DATE_FORMAT).date()
            else:
                raise UnsupportedFieldTypeError(v)
        
        # validate key/value pairs (semantic validation, assume type checking is finished)
        cls.validate(kvs)
        
        try:
            if not entity:
                entity = cls(**kvs)
            else: 
                for k in kvs.keys(): 
                    setattr(entity, k, kvs[k])

            entity.put()
        except Exception as e: 
            logging.error("Class: %s" % cls.__name__)
            logging.error("Couldn't put entity: %s" % kvs)
            logging.error(e)
            return None
        
        return entity
    
    # updates existing entity based on id
    @classmethod
    def post(cls, i, kvs):
        entity = cls.get_by_id(i)
        return cls.put1(kvs, entity = entity)
    
    # deletes an entity based on id
    @classmethod
    def delete1(cls, i):
        item = cls.get_by_id(i)
        if item: 
            item.key.delete()
            return True
        
        return False

    @property
    def str(self):
        return str(json.encode(utils.to_dict(self)))

def generate_model_form(cls, with_key = False):
    fields = filter(lambda x: issubclass(type(x[1]), ndb.Property), cls.__dict__.iteritems())
    
    #firstly, let's add key to the form and make it disabled
    form = [{'element' : 'text', 'label' : 'id', 'id' : 'id'}] if with_key else []
    
    for (k, t) in fields: 
        d = {'label' : k, 'id' : k}

        if isinstance(t, ndb.IntegerProperty) or isinstance(t, ndb.FloatProperty):
            d['element'] = 'text'
            d['class'] = 'number'
        
        elif isinstance(t, SpecificStringProperty):
            d['element'] = 'text'
            d['class'] = t._css_class

        elif isinstance(t, ndb.StringProperty):
            d['element'] = 'text'

        elif isinstance(t, ndb.TextProperty):
            d['element'] = 'textarea'
            d['class'] = 'textarea'

        elif isinstance(t, ndb.DateProperty):
            d['element'] = 'text'
            d['class'] = 'date'
            d['format'] = settings.DATE_FORMAT_HTML

        elif isinstance(t, ndb.BooleanProperty):
            d['element'] = 'checkbox'
            d['class'] = 'checkbox'

        else:
            raise UnsupportedFieldTypeError(k)
        
        form.append(d)
        
    return form

class Widget(RESTModel):
    int_field = ndb.IntegerProperty(required = True)
    boolean_field = ndb.BooleanProperty(required = True)
    string_field = ndb.StringProperty(required = True)
    text_field = ndb.TextProperty(required = True)
    email_field = EmailProperty(required = True)
    link_field = LinkProperty(required = True)
    date_field = ndb.DateProperty(required = True)

class EmailAddr(ndb.Model):
    email = EmailProperty(required = True)
