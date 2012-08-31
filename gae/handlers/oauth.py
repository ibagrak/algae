'''
Created on Jun 14, 2012

@author: ibagrak
'''
import logging

from libs import simpleauth
import secrets
import common

class AuthHandler(common.BaseHandler, simpleauth.SimpleAuthHandler):
    """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

    USER_ATTRS = {
       'google'   : {
         'picture': 'pic',
         'name'   : 'username',
         'link'   : 'profile'
       },
      'facebook' : {
        'id'     : lambda id: ('pic', 'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
        'name'   : 'username',
        'link'   : 'profile'
      },
#      'windows_live': {
#        'avatar_url': 'avatar_url',
#        'name'      : 'name',
#        'link'      : 'link'
#      },
      'twitter'  : {
                    'profile_image_url': 'pic',
                    'screen_name'      : 'username',
                    'link'             : 'profile'
                    },
#      'linkedin' : {
#        'picture-url'       : 'avatar_url',
#        'first-name'        : 'name',
#        'public-profile-url': 'link'
#      },
#      'openid'   : {
#        'id'      : lambda id: ('avatar_url', '/img/missing-avatar.png'),
#        'nickname': 'name',
#        'email'   : 'link'
#      }
    }

    def _on_signin(self, data, auth_info, provider):
        """Callback whenever a new or existing user is logging in.
         data is a user info dictionary.
         auth_info contains access token or oauth token and secret.
        """
        auth_id = '%s:%s' % (provider, data['id'])
        logging.info('Looking for a user with id %s' % auth_id)

        user = self.auth.store.user_model.get_by_auth_id(auth_id)
        if user:
            logging.info('Found existing user to log in')
            # existing user. just log them in.
            self.auth.set_session(
              self.auth.store.user_to_dict(user)
            )

        else:
            # check whether there's a user currently logged in
            # then, create a new user if nobody's signed in,
            # otherwise add this auth_id to currently logged in user.
            if self.logged_in:
                logging.info('Updating currently logged in user')

                u = self.current_user
                u.auth_ids.append(auth_id)
                u.populate(**self._to_user_model_attrs(data, self.USER_ATTRS[provider]))
                u.put()

            else:
                logging.info('Creating a brand new user')

                ok, user = self.auth.store.user_model.create_user(
                  auth_id, **self._to_user_model_attrs(data, self.USER_ATTRS[provider])
                )
                
                logging.info('user: %s' % user)
                
                if ok:
                    self.auth.set_session(
                      self.auth.store.user_to_dict(user)
                    )

        self.redirect('/')

    def logout(self):
        self.auth.unset_session()
        self.redirect('/')

    def _callback_uri_for(self, provider):
        return self.uri_for('auth_callback', provider=provider, _full=True)

    def _get_consumer_info_for(self, provider):
        """Returns a tuple (key, secret) for auth init requests."""
        return secrets.AUTH_CONFIG[provider]

    def _to_user_model_attrs(self, data, attrs_map):
        user_attrs = {}
        for k, v in data.iteritems():
            if k in attrs_map:
                key = attrs_map[k]
                if isinstance(key, str):
                    user_attrs.setdefault(key, v)
                else:
                    user_attrs.setdefault(*key(v))

        return user_attrs
