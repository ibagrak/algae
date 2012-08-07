'''
Created on Mar 29, 2012

@author: ibagrak
'''
import webapp2
from webapp2_extras import json

import settings
import utils

from google.appengine.ext import db

class UnsupportedFieldTypeError(Exception): pass

class RESTModel(db.Model):
    # implemented by subclasses
    @classmethod
    def validate(cls, kvs):
        pass
    
    @classmethod
    def get(cls, i):
        return cls.get_by_id(i)
    
    @classmethod
    def put(cls, kvs):
        
        # prevent malicious overwriting of system attrs
        for k in kvs.keys(): 
            if not hasattr(cls, k) or k == '__module__' or k == '__doc__':
                del kvs[k]
                continue
            
            v = cls.__dict__[k]
            
            # convert unicode values to datastore value types
            if isinstance(v, db.IntegerProperty): 
                kvs[k] = int(kvs[k])
            elif isinstance(v, db.StringProperty):
                pass
            elif isinstance(v, db.TextProperty):
                pass
            elif isinstance(v, db.DateProperty):
                pass
            elif isinstance(v, db.BooleanProperty):
                pass
            elif isinstance(v, db.EmailProperty):
                pass
            else:
                raise UnsupportedFieldTypeError(v)
        
        # validate key/value pairs
        cls.validate(kvs)
        
        try:
            entity = cls(**kvs)
            db.put(entity)
        except: 
            return None
        
        return entity
    
    @classmethod
    def post(cls, i, kvs):
        return cls.put(kvs)
    
    @classmethod
    def delete(cls, i):
        item = cls.get_by_id(i)
        if item: 
            del item
            return True
        
        return False

    @property
    def str(self):
        return str(json.encode(utils.to_dict(self)))

def generate_model_form(cls, with_key = False):
    fields = filter(lambda x: issubclass(type(x[1]), db.Property), cls.__dict__.iteritems())
    
    #firstly, let's add key to the form and make it disabled
    form = [{'element' : 'text', 'label' : 'id', 'id' : 'id'}] if with_key else []
    
    for v in fields: 
        if isinstance(v[1], db.IntegerProperty): 
            form.append({'element' : 'text', 'label' : v[0], 'class' : 'integer', 'id' : v[0]})
        elif isinstance(v[1], db.StringProperty):
            form.append({'element' : 'text', 'label' : v[0], 'id' : v[0]})
        elif isinstance(v[1], db.TextProperty):
            form.append({'element' : 'textarea', 'label' : v[0], 'id' : v[0]})
        elif isinstance(v[1], db.DateProperty):
            form.append({'element' : 'text', 'label' : v[0], 'class' : 'date', 'id' : v[0]})
        elif isinstance(v[1], db.BooleanProperty):
            form.append({'element' : 'checkbox', 'label' : v[0], 'id' : v[0]})
        elif isinstance(v[1], db.EmailProperty):
            form.append({'element' : 'text', 'label' : v[0], 'id' : v[0]})
        else:
            raise UnsupportedFieldTypeError(v)
    
    return form
        
class Widget(RESTModel):
    int_field = db.IntegerProperty(verbose_name = "Integer field", required = True, default = 0)
    

    
    