'''
Created on Mar 29, 2012

@author: ibagrak
'''

from google.appengine.ext import db

class User(db.Model):
    sid = db.StringProperty(required = True)
    
    @classmethod
    def get_user_from_session(cls, sid):
        return db.Query(User).filter("sid =", sid).get()