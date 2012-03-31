import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
import index
import api

application = webapp.WSGIApplication([
                                      ('/',                                 index.MainPage),
                                      ('/api?*',                            api.APIHandler),
                                      ], debug = settings.DEBUG)

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()