'''
Created on Jun 14, 2012

@author: ibagrak
'''
import settings
import common 

class OauthHandler(common.BaseHandler):
    def get(self, step, service, **kwargs):
        if step == 'forward':
            if service == 'twitter':
                pass #TODO
            elif service == 'facebook':
                pass #TODO
            else:
                return self.redirect(settings.ERROR_PATH)
        elif step == 'confirm':
            if service == 'twitter':
                pass #TODO
            elif service == 'facebook':
                pass #TODO
            else:
                return self.redirect(settings.ERROR_PATH)