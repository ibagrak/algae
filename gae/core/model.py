'''
Created on Mar 29, 2012

@author: ibagrak
'''
import logging
from datetime import datetime
from webapp2_extras import json

import settings
import utils

from google.appengine.ext import db

class UnsupportedFieldTypeError(Exception): pass
class InvalidFieldValueError(Exception): pass

class RESTModel(db.Model):
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
    def put(cls, kvs, entity = None):
        
        # prevent malicious overwriting of system attrs
        for k in kvs.keys(): 
            if not k in cls.properties():
                del kvs[k]
                continue
            
            v = cls.__dict__[k]
            
            # convert unicode values to datastore value types
            if isinstance(v, db.IntegerProperty): 
                kvs[k] = int(kvs[k])
            elif isinstance(v, db.FloatProperty):
                kvs[k] = float(kvs[k])
            elif isinstance(v, db.BooleanProperty):
                kvs[k] = True if kvs[k] == 'True' else False
            elif isinstance(v, db.StringProperty) or isinstance(v, db.TextProperty):
                kvs[k] = kvs[k]
            elif isinstance(v, db.DateProperty):
                kvs[k] = datetime.strptime(kvs[k], settings.DATE_FORMAT).date()
            elif isinstance(v, db.LinkProperty):
                kvs[k] = kvs[k] #TODO: verify URL
            elif isinstance(v, db.EmailProperty):
                kvs[k] = kvs[k] #TODO: verify email address
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

            db.put(entity)
        except Exception as e: 
            logging.error("Couldn't put entity: %s" % kvs)
            logging.error(e)
            return None
        
        return entity
    
    # updates existing entity based on id
    @classmethod
    def post(cls, i, kvs):
        entity = cls.get_by_id(i)
        return cls.put(kvs, entity = entity)
    
    # deletes an entity based on id
    @classmethod
    def delete1(cls, i):
        item = cls.get_by_id(i)
        if item: 
            item.delete()
            return True
        
        return False

    @property
    def str(self):
        return str(json.encode(utils.to_dict(self)))

def generate_model_form(cls, with_key = False):
    fields = filter(lambda x: issubclass(type(x[1]), db.Property), cls.__dict__.iteritems())
    
    #firstly, let's add key to the form and make it disabled
    form = [{'element' : 'text', 'label' : 'id', 'id' : 'id'}] if with_key else []
    
    for (k, t) in fields: 
        d = {'label' : k, 'id' : k}

        if isinstance(t, db.IntegerProperty) or isinstance(t, db.FloatProperty):
            d['element'] = 'text'
            d['class'] = 'number'
        
        elif isinstance(t, db.StringProperty):
            d['element'] = 'text'

        elif isinstance(t, db.TextProperty):
            d['element'] = 'textarea'
            d['class'] = 'textarea'

        elif isinstance(t, db.DateProperty):
            d['element'] = 'text'
            d['class'] = 'date'
            d['format'] = settings.DATE_FORMAT_HTML

        elif isinstance(t, db.BooleanProperty):
            d['element'] = 'checkbox'
            d['class'] = 'checkbox'

        elif isinstance(t, db.EmailProperty):
            d['element'] = 'text'
            d['class'] = 'email'

        elif isinstance(t, db.LinkProperty):
            d['element'] = 'text'
            d['class'] = 'url'

        else:
            raise UnsupportedFieldTypeError(k)
        
        form.append(d)
        
    return form
        
class Widget(RESTModel):
    int_field = db.IntegerProperty(required = True)
    boolean_field = db.BooleanProperty(required = True)
    string_field = db.StringProperty(required = True)
    text_field = db.TextProperty(required = True)
    email_field = db.EmailProperty(required = True)
    link_field = db.LinkProperty(required = True)
    date_field = db.DateProperty(required = True)

class EmailAddr(db.Model):
    email = db.EmailProperty(required = True)
