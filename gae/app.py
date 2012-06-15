import webapp2

import settings
from handlers import index, api, common, email_auth, oauth

routes = [webapp2.Route('/',                  handler = index.Index),
          webapp2.Route('/email-confirm',     handler = email_auth.EmailConfirm),
          webapp2.Route('/email-signin',      handler = email_auth.EmailAuthHandler, handler_method="signin_email"),
          webapp2.Route('/email-signup',     handler = email_auth.EmailAuthHandler, handler_method="signup_email"),
          webapp2.Route('/oauth/<action>/<service>',handler = oauth.OauthHandler),
          webapp2.Route('/rest/<obj_t>/<id>', handler = common.BaseRESTHandler), 
          webapp2.Route('/rpc',               handler = api.RPCHandler)]                             
                                       
application = webapp2.WSGIApplication(routes,   
                                      debug = settings.DEBUG,
                                      config = settings.config)

def main():
    application.run()

if __name__ == "__main__":
    main()