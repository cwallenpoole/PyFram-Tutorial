__all__ = ["BasicRenderer", "HTMLRenderer"]

def _str_print(line):
    print(str(line))


class BasicRenderer:
    ''' 
    A simple way to manage output to the browser, this will be the basis of 
    all of the view classes which will be used in PyFram. The use is simple:
    renderer = BasicRenderer()
    renderer.output()
    '''
    def __init__(self, headers = None, body = None, output = _str_print):
        '''
        Constructor of a BasicRender
        
        header -- the headers part of the request (everything which 
                  is returned as an HTML header) (must have a keys method)
                  (default {})
        body -- the body part of the request (must be iterable)
                (default [])
        output -- the function used to output the value 
                (default print(str(value)))
        '''
        # if headers is not none use headers, use a new dictionary
        self.headers = headers if headers is not None else {"Content-Type","text"}
        # this is a helper to make sure that 
        assert callable(getattr(self.headers, 'keys', None)), \
            'Headers must have a keys method'
        # if body is not none use body, else use a new list
        self.body = body if body is not None else []
        assert hasattr(self.body,'__iter__'), \
            'body must be iterable'
        # pass in the default output method 
        self.output = output
        assert callable(output), 'output must be callable'
    
    def setHeader(self,name,value):
        ''' allows for easy means of setting a header '''
        self.headers[name] = value
        
    def getHeader(self,name):
        ''' allows for an easy means of getting the header set '''
        return self.headers[name]
    
    def append(self, line):
        ''' an easy means of adding data (generally a list) to the body '''
        self.body += line
            
    def render(self,output = None):
        ''' passes each line of output to the output function '''
        # make it as easy as possible to pass in a new output
        output = output if output else self.output
        if not (self.headers or self.body):
            # if neither, make sure that the script knows that it needs
            # to output *something* otherwise we'll get an error!
            output('')
            return
            
        for key in self.headers.keys():
            output("{0}: {1}".format(key, self.headers[key]))
            
        # remember, that first line after the headers needs to be empty
        # whether there have been headers output or not!
        output("")
        for ln in self.body:
            output(ln)
            


class HTMLRenderer(BasicRenderer):
    ''' class designed for specialization in HTML requestions '''
    def __init__(self, headers = None, body = None, output = _str_print):
        headers = headers if headers is not None else {"Content-Type":"text/html"} 
        super(HTMLRenderer,self).__init__(headers,body,output)
        self.body = ['<html><head>','</head><body>'] + self.body \
                  + ['</body></html>']

    def append(self,line):
        self.body = self.body[:-1] + line + self.body[-1:]
