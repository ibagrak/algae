import webapp2

import settings
from handlers import index, api

application = webapp2.WSGIApplication([
                                       ('/',                         index.Index),
                                       ('/index.html',               index.Index),
                                       (r'/api?.*',                  api.APIHandler),
                                      ], 
                                     debug = settings.DEBUG,
                                     config = settings.config)

def main():
    application.run()

if __name__ == "__main__":
    main()