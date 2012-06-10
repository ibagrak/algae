'''
Created on Mar 29, 2012

@author: ibagrak
'''

from google.appengine.ext import db
 
class User(db.Model):
    sid = db.StringProperty(required = True)
    nick = db.StringProperty(required = True)
    pic = db.URLProperty(required = True)
    
    # for email-authenticated accounts 
    confirmed = db.BooleanProperty(default = False) # set to false for email-authenticated accounts until email is confirmed
    pwhash = db.StringProperty()                   # password hash
    email = db.EmailProperty()
    
    @classmethod
    def get_user_from_session(cls, sid):
        return db.Query(User).filter("sid =", sid).get()
    
    @classmethod
    def get_user_from_email(cls, email):
        return db.Query(User).filter("email =", email).get()
    
class Widget(db.Model):
    field = db.IntegerProperty(required = True, default = 0)

    @classmethod
    def get(cls, i):
        return cls.get_by_id(i)
    
    @classmethod
    def put(cls, i, kvs):
        item = cls.get_by_id(i)
        if not item:
            item = Widget(field = kvs['field']) # TODO: modify to be generic
            item.put()
        else:
            for k, v in kvs:
                item[k] = v
            item.put()
    
        return item
    
    @classmethod
    def post(cls, i, kvs):
        return cls.put(id, kvs)
    
    @classmethod
    def delete(cls, i):
        item = cls.get_by_id(id)
        if item: 
            del item
            return True
        
        return False
    