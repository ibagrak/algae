import traceback
import sys

import json
import logging
import settings

import common

class APIHandler(common.BaseHandler):
    
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
            result = getattr(self, action)(kvs, self.session)
        
        self.response.out.write(json.dumps(result))
        
    def handle_exception(self, exception, debug_mode):
        logging.exception(exception)

        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            result = (settings.GENERAL_ERROR, lines)
        else:
            result = (settings.GENERAL_ERROR, "Please contact application administrator for support")
            
        self.response.clear()
        self.response.out.write(json.dumps(result))
    
    @common.logapi    
    def test_api(self, session):
        return settings.SUCCESS
