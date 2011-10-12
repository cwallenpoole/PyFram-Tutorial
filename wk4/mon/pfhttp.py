import os
import xml.sax.saxutils as saxutils
_request = None
_foo = ["f","f"

def getRequest(*, d = os.environ):
    ''' returns the default request object, initialized by the values in os.environ '''
    global _request
    if not _request:
        # because os.environ will not let us add keys, we need to create a 
        # temporary value to store all of the values. It does not make sense
        # to have it has part of a generic request object.
        val = {}
        for k in d:
            val[k]=d[k]
        _request = Request(val)
    return _request

class Request:
    ''' Data object which is responsible for retrieving information about
        the http request '''
    def __init__(self, src):
        self._segs = None # for segments
        self.__src = src
        try:
            if 'PATH_INFO' not in src:
                ruri = src['REQUEST_URI'], 
                path = os.path.dirname(src['SCRIPT_NAME'])
                src['PATH_INFO'] = src['REQUEST_URI'][len(path):]
        except:
            src['PATH_INFO']  = src['REQUEST_URI']
    
    def uri_segments(self, ind = None, end = None):
        ''' Assuming the URL 
            http://www.example.com/&lt;your-script-dir&gt;foo/bar/baz/quux
            This will return:<ul>
                <li>foo if ind = 0, bar if 1, baz if 2...</li>
                <li>['foo','bar','baz', 'quux'] if None</li>
                <li>['foo','bar'] if [0,1] or (0,1), ['bar','baz','quux'] if (1,3)</li>
            </ul>'''
            
        if self._segs is None:
            # cache this, no sense in calling it more than once.
            self._segs = self.path_info[1:].split('/')
            
        # is it an interable? use the first and second indexes as boundaries
        if ind is not None and end is None:
            return self._segs[ind]
            
        # is it a number? return that index
        elif ind is not None:
            return self._segs[ind:end]
            
        # is ind missing? Then just return everything
        else:
            return self._segs
    
    def __getattr__(self, prop, o = None):
        return self.__src[prop.upper()]
        
    def __str__(self):
        l = list(self.__src.keys())
        l.sort()
        s = '{'
        for k in l:
            val = saxutils.escape(self.__src[k])
            val = val.replace('\n', '\\n ')
            s += "'{0}':\t'{1}',".format(k, val)
        return s + '}'
