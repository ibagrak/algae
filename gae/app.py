import webapp2

import settings
from handlers import index, api, common, auth

routes = [webapp2.Route('/',                  handler = index.Index),
          webapp2.Route('/email-signup',      handler = auth.EmailAuthHandler, handler_method="signup_email"),
          webapp2.Route('/email-signin',      handler = auth.EmailAuthHandler, handler_method="signin_email"),
          webapp2.Route('/oauth/<action>/<service>',handler = auth.OauthHandler),
          webapp2.Route('/rest/<obj_t>/<id>', handler = common.BaseRESTHandler), 
          webapp2.Route('/rpc',               handler = api.RPCHandler)]                             
                                       
application = webapp2.WSGIApplication(routes,   
                                      debug = settings.DEBUG,
                                      config = settings.config)

def main():
    application.run()

if __name__ == "__main__":
    main()