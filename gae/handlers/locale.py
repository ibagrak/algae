'''
Created on Aug 31, 2012

@author: helmuthb
'''
import settings
import common

class SetLocale(common.BaseHandler):
    """ Set the locale in the session (if locale is valid)
        then redirect back to referer
        copied from fishwebby @ stackoverflow
    """
    def get(self, locale):
        if locale in settings.AVAILABLE_LOCALES:
            self.session["locale"] = locale
        self.redirect(self.request.headers.get('Referer','/'))
