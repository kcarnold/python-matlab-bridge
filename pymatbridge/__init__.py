###############################################
# Matlab.py
# Part of Python-MATLAB-bridge
# Max Jaderberg 2012
###############################################
from httplib import BadStatusLine
import urllib2, urllib, os, json
import uuid

MATLAB_FOLDER = '%s/matlab' % os.path.realpath(os.path.dirname(__file__))

class MatlabClient(object):
    eval_func = 'web_feval.m'

    def __init__(self, host='localhost', port=4000, id=None):
        self.host = host
        self.port = port
        self.server = 'http://%s:%s' % (self.host, self.port)
        if id is None:
            id = str(uuid.uuid1())
        self.id = id

    def stop(self):
        # Stop the MATLAB server
        try:
            self._open_page('exit_server.m', {'id': self.id})
        except BadStatusLine:
            pass
        except urllib2.URLError:
            pass
        print "MATLAB closed"
        return True

    def is_connected(self):
        try:
            resp = self._open_page('test_connect.m', {'id': self.id})
            if resp['message']:
                return True
        except urllib2.URLError:
            pass
        return False

    def is_function_processor_working(self):
        try:
            result = self.run('%s/test_functions/test_sum.m' % MATLAB_FOLDER, {'echo': 'Matlab: Function processor is working!'})
            if result['success'] == 'true':
                return True
        except urllib2.URLError:
            pass
        return False

    def run(self, func_path, func_args=None, maxtime=None):
        page_args = {
            'func_path': func_path,
        }
        if func_args:
            page_args['arguments'] = json.dumps(func_args)
        if maxtime:
            result = self._open_page(self.eval_func, page_args, maxtime)
        else:
            result = self._open_page(self.eval_func, page_args)
        return result

    def _open_page(self, page_name, arguments={}, timeout=10):
        page = urllib2.urlopen('%s/%s' % (self.server, page_name), urllib.urlencode(arguments), timeout)
        return json.loads(page.read())
