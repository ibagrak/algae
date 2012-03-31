import traceback
import sys

from django.utils import simplejson

import settings
from handlers import common

class APIHandler(common.AbstractRequestHandler):
    
    @common.withuser
    def get(self, *args, **kwargs):
        action = self.request.get('action')
        args = self.request.arguments()
        args.remove('action')
        kvs = {}
    
        for arg in args:
            kvs[arg] = self.request.get(arg)
        
        if not action in settings.APIS:
            result = (settings.INVALID_API_ERROR, 0)
        else:    
            result = getattr(self, action)(kvs, kwargs['session'], kwargs['user'])
        
        self.response.out.write(simplejson.dumps(result))
        
    def handle_exception(self, exception, debug_mode):
        self.logger.exception(exception)

        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            result = (settings.GENERAL_ERROR, lines)
        else:
            result = (settings.GENERAL_ERROR, "Please contact application administrator for support")
            
        self.response.clear()
        self.response.out.write(simplejson.dumps(result))
    
    @common.logapi    
    def test_api(self):
        return settings.SUCCESS
        
        return settings.SUCCESS