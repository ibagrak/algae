'''
Created on Jun 9, 2012

@author: ibagrak
'''
import re
import hashlib
import urllib
import logging

from google.appengine.api import mail

import settings
import common
import utils
            
class EmailConfirm(common.BaseHandler):
    def get(self, *args):
        kwargs = self.request.GET
        
        if not ('email' in kwargs and 'token' in kwargs):
            return self.prep_html_response('email_confirm.html', { 'confirm_status' : 'Invalid confirmation link.'})
        
        auth_id = '%s:%s' % ("own", kwargs['email'])
        
        if self.auth.store.user_model.validate_signup_token(kwargs['email'], kwargs['token']):     
            self.auth.store.user_model.delete_signup_token(kwargs['email'], kwargs['token'])
            user = self.auth.store.user_model.get_by_auth_id(auth_id)
            
            # confirm email by removing token field from user (hackish, need ability to check token existence) 
            if hasattr(user, 'token'):
                del user.token
                user.put()
            
            tvars = { 'confirm_status' : 'Email confirmed.'}
        else: 
            tvars = { 'confirm_status' : 'Email not confirmed.'}
        
        self.prep_html_response('email_confirm.html', tvars)

        
# email authentication is handled through form submission
#   -> /email/action=signin_email&email=<>&pw_hash=<>           : email signin  
#   <- json response   
#   -> /email/action=signup_email&email=<>&pw_hash=<>&nick=<>   : email signup
#   <- json response
class EmailAuthHandler(common.BaseAPIHandler):
    
    def signin_email(self, *args):
        kwargs = self.request.GET
        
        if not ('email' in kwargs and 'password' in kwargs):
            return self.prep_json_response(400, key = 'missing')
        
        auth_id = '%s:%s' % ("own", kwargs['email'])
        
        try: 
            user = self.auth.store.user_model.get_by_auth_password(auth_id, kwargs['password'])

            logging.info('Found existing user to log in')
            logging.info('user: %s' % user)
            
            # check if there is a signup token (we delete token when user confirms)
            if hasattr(user, 'token'):
                return self.prep_json_response(402, key = 'unconfirmed')
            
            logging.info('user: %s' % user)
            
            # set "remember me" cookie
            self.response.set_cookie(settings.APP_ID + '_login', 
                                     value = 'provider=email&username=%s' % user.username.encode(),
                                     max_age = 315360000, # 10 years
                                     path = '/') 
                
            # existing user. just log them in.
            self.auth.set_session(
              self.auth.store.user_to_dict(user)
            )
            
            return self.prep_json_response(200)
        except Exception as e:
            logging.info(type(e))
            return self.prep_json_response(400, key = 'email_password')
              
    def signup_email(self, *args):
        kwargs = self.request.GET
        
        if not ('email' in kwargs and 'username' in kwargs and 'password_raw' in kwargs):
            return self.prep_json_response(400, key = 'missing')
            
        if re.match(utils.email_re, kwargs['email']):
            auth_id = '%s:%s' % ("own", kwargs['email'])
            kwargs['pic'] = utils.to_gravatar_url(kwargs['email'])
            kwargs['profile'] = 'mailto:' + kwargs['email']
            
            logging.info('Creating a brand new user')

            # try to create a new user
            ok, user = self.auth.store.user_model.create_user(auth_id, **kwargs)
                
            logging.info('user: %s' % user)
                
            if ok:
                token = self.auth.store.user_model.create_signup_token(kwargs['email'])
                # there is no way to check if toekn still exists for a given email (i.e. email hasn't been
                # confirmed) without having the token to we cheat here and temporarily store it in user
                user.token = token
                user.put()
                
                link = "http://%s.appspot.com/email-confirm?token=%s&email=%s" % (settings.APP_ID, token, kwargs['email']) 
                mail.send_mail(sender = "%s Notifier <%s>" % (settings.APP_ID, settings.EMAIL_SENDER), 
                               to = kwargs['email'],
                               subject = "%s Email Confirmation" % settings.APP_ID, 
                               body = settings.EMAIL_CONFIRM_BODY % (kwargs['username'], link))
                logging.info("sending out confirm link: %s", link)
                return self.prep_json_response(200)
            else:
                return self.prep_json_response(402, key = 'duplicate')
        else:
            # invalid email
            return self.prep_json_response(400, key = 'email')
