'''
Created on Nov 27, 2010

@author: ibagrak
'''

from sessions import SessionMiddleware

import settings

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=settings.COOKIE_KEY)
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app
