'''
Created on Mar 29, 2012

@author: ibagrak
'''
import logging
from datetime import datetime
from webapp2_extras import json

import settings
import utils

from google.appengine.ext import ndb

class UnsupportedFieldTypeError(Exception): pass
class InvalidFieldValueError(Exception): pass

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
            elif isinstance(v, ndb.StringProperty) or isinstance(v, ndb.TextProperty):
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
    email_field = ndb.StringProperty(required = True)
    link_field = ndb.StringProperty(required = True)
    date_field = ndb.DateProperty(required = True)

class EmailAddr(ndb.Model):
    email = ndb.StringProperty(required = True)
