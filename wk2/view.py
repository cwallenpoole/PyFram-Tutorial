__all__ = ["BasicRenderer"]

def __str_print(line):
    print(str(line))

class BasicRenderer:
    def __init__(self, headers = None, body = None, output = None):
        '''
        Constructor of a BasicRender
        
        header -- the headers part of the request (everything which 
                  is returned as an HTML header) (must have a keys method)
                  (default {})
        body -- the body part of the request (must be iterable)
                (default [])
        output -- the function used to output the value (default print(str(value)))
        '''
        self.headers = headers if headers is not None else {}
        assert callable(getattr(self.headers, 'keys', None)), 'Headers must have a keys method'
        # if headers is not none use headers, use a new dictionary
        # if body is not none use body, else use a new list
        self.body = body if body is not None else []
        # pass in the default output method 
        self.output = output if output is not None else __str_print
    
    def setHeader(self,name,value):
        ''' allows for easy means of setting a header '''
        self.headers[name] = value
        
    def getHeader(self,name):
        ''' allows for an easy means of getting the header set '''
        return self.headers[name]
    
    def append(self, line):
        ''' an easy means of adding a line to the body '''
        self.body.append(line)
            
    def render(self,output = None):
        ''' passes each line of output to the output function '''
        # make it as easy as possible to pass in a new output
        output = output if output else self.output
        for key in self.headers.keys():
            output("{0}: {1}".format(key, self.headers[key]))
            
        if self.body:
            # remember, that first line before the body needs to be a 
            # \n or it will be an error
            output("")
        for ln in self.body:
            output(ln)
