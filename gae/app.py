import webapp2

import settings
from handlers import index, api, common, auth

application = webapp2.WSGIApplication([
                                       ('/',                         index.Index),
                                       ('/email?.*',                 auth.EmailAuthHandler),
                                       (r'/oauth/(\w+)/(\w+)',       auth.OathHandler),
                                       (r'/rest-api/(\w+)/(\d+)',    common.BaseRESTHandler),
                                       (r'/api?.*',                  api.APIHandler),
                                      ], 
                                     debug = settings.DEBUG,
                                     config = settings.config)

def main():
    application.run()

if __name__ == "__main__":
    main()