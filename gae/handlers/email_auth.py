'''
Created on Jun 9, 2012

@author: ibagrak
'''
import re
import hashlib
import urllib
import logging

from google.appengine.api import mail
from google.appengine.ext import db

from handlers import jinja_environment

import settings
import connectors
import common
import model

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

class EmailConfirm(common.BaseHandler):
    def get(self, *args, **kwargs):
        kwargs = self.request.GET
        
        user = model.User.get(db.Key(kwargs['key']))
        if user: 
            user.confirmed = True
            user.put()
            t_args = { 'confirm_status' : 'Email confirmed.'}
        else: 
            t_args = { 'confirm_status' : 'Email not confirmed.'}
            
        self.session_inc_pageviews()
        t_args.update({ 'pageviews' : self.session['pageviews']})
        
        template = jinja_environment.get_template("email_confirm.html")
        self.response.out.write(template.render(t_args))
        
# email authentication is handled through form submission
#   -> /email/action=signin_email&email=<>&pw_hash=<>           : email signin  
#   <- json response   
#   -> /email/action=signup_email&email=<>&pw_hash=<>&nick=<>   : email signup
#   <- json response
class EmailAuthHandler(common.BaseAPIHandler):
        
    def signin_email(self, *args):
        kwargs = self.request.GET
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
                
                return self.prep_response(200)
            elif not user.confirmed:
                return self.prep_response(402, key = 'unconfirmed')
            else:
                return self.prep_response(400, key = 'password')
        else:
            return self.prep_response(400, key = 'email_password')
    
    @common.loghandler    
    def signup_email(self, *args):
        kwargs = self.request.GET
        if re.match(email_re, kwargs['email']):
            # check if this email address is in use
            user = model.User.get_user_from_email(kwargs['email'])
            if user: 
                self.prep_response(402, key = 'duplicate')
                return
            
            image_hash = hashlib.md5(kwargs['email']).hexdigest()
            
            # create user
            user = model.User(nick = kwargs['username'], 
                              pic = "http://www.gravatar.com/avatar/" + image_hash + "?d=" + urllib.quote(settings.HOME_URL + '/static/images/anonymous.png'),
                              sid = self.session['id'],
                              email = kwargs['email'],
                              pwhash = kwargs['password'],
                              confirmed = False) 
            user.put()
            
            link = "http://%s.appspot.com/email-confirm?key=%s" % (settings.APP_ID, str(user.key()))  
            mail.send_mail(sender = "%s Notifier <noreply@%s.appspot.com>" % (settings.APP_ID, settings.APP_ID), 
                           to = kwargs['email'],
                           subject = "%s Email Confirmation" % settings.APP_ID, 
                           body = """ 
Hello, %s!

Here is your email confirmation link: %s

Thanks 

""" % (kwargs['username'], link))
            logging.info("sending out confirm link: %s", link)
            self.prep_response(200)
        else: 
            # invalid email
            self.prep_response(400, key = 'email')
            