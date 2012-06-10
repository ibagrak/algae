'''
Created on Jun 9, 2012

@author: ibagrak
'''
import re
import hashlib

from google.appengine.api import mail

import settings
import connectors
import common
import model

class OathHandler(common.BaseHandler):
    def get(self, step, service, **kwargs):
        if step == 'forward':
            if service == 'twitter':
                pass #TODO
            elif service == 'facebook':
                pass #TODO
            else:
                return self.redirect(settings.ERROR_PATH)
        elif step == 'confirm':
            if service == 'twitter':
                pass #TODO
            elif service == 'facebook':
                pass #TODO
            else:
                return self.redirect(settings.ERROR_PATH)

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

# email authentication is handled through form submission
#   -> /email/action=signin_email&email=<>&pw_hash=<>           : email signin  
#   <- json response   
#   -> /email/action=signup_email&email=<>&pw_hash=<>&nick=<>   : email signup
#   <- json response
class EmailAuthHandler(common.BaseAPIHandler):

    def signin_email(self, **kwargs):
        user = model.User.get_user_from_email(kwargs['email'])
    
        if user:
            if user.confirmed and user.pw_hash == kwargs['pw_hash']:
                # regenerate id
                self.session_regenerate_id()
                self.session_login()
                
                user.sid = self.session['id'] # new session id
                user.put()
                
                # set "remember me" cookie
                self.response.set_cookie(settings.APP_ID + '_login', 
                                         value = 'provider=email&username=%s' % user.nick.encode(),
                                         max_age = 315360000, # 10 years
                                         path = '/') 
                
                return ({'code': 200, 'message' : ''})
            elif not user.confirmed:
                return ({'code': 404, 'message' : 'Email has not been confirmed. Check your inbox for email confirmation link!'})
            else:
                return ({'code': 404, 'message' : 'Invalid password.'})
        else:
            return ({'code': 404, 'message' : 'Invalid email or password.'})
        
    def signup_email(self, **kwargs):
        if re.match(email_re, kwargs['email']):
            # check if this email address is in use
            user = model.User.get_user_from_email(kwargs['email'])
            if user: 
                # there is a confirmed user
                return ({'code' : 404, 'message' : 'There is already a user with this email address.'})
            
            image_hash = hashlib.md5(kwargs['email']).hexdigest()
            
            # create user
            user = model.User(nick = kwargs['nick'], 
                              pic = ("http://www.gravatar.com/avatar/" + image_hash + "?d=http%3A%2F%2F%s.appspot.com%2Fstatic%2Fimages%2Fanonymous.png") % settings.APP_ID,
                              sid = self.session['id'],
                              email = kwargs['email'],
                              pwhash = kwargs['pw_hash'],
                              confirmed = False) 
            user.put()
            
            link = ("http://%s.appspot.com/email_confirmation/" % settings.APP_ID) + str(user.key())    
            mail.send_mail(sender = "%s Notifier <noreply@%s.appspot.com>" % (settings.APP_ID, settings.APP_ID), 
                           to = kwargs['email'],
                           subject = "%s Email Confirmation" % settings.APP_ID, 
                           body = """ 
Hello, %s!

Here is your email confirmation link: %s

Thanks 

""" % (kwargs['nick'], link))
            result = ({'code' : 200, 'message' : ''})
        else: 
            # invalid email
            result = ({'code' : 404, 'message' : 'Invalid email address. Please try again.'})
            
        return result