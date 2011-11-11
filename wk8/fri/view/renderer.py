def _str_print(line):
    print(str(line))

class BasicRenderer:
    ''' 
    A simple way to manage output to the browser, this will be the basis of 
    all of the view classes which will be used in PyFram. The use is simple:
    renderer = BasicRenderer()
    renderer.output()
    '''
    def __init__(self, body = None, output = _str_print):
        '''
        Constructor of a BasicRender
        
        body - the body part of the request (must be iterable)
                (default [])
        output - the function used to output the value 
                (default print(str(value)))
        '''
        
        # if body is not none use body, else use a new list
        self.body = body if body else []
        # assert hasattr(self.body,'__iter__'), \
        #    'body must be iterable'

        # pass in the default output method 
        self.output = output
        assert callable(output), 'output must be callable'
        
    def append(self, line):
        ''' an easy means of adding data (generally a list) to the body '''
        self.body += line
            
    def render(self,output = None):
        ''' passes each line of output to the output function '''            
        # remember, that first line after the headers needs to be empty
        # whether there have been headers output or not!
        output("")
        for ln in self.body:
            output(ln)

class RequestRenderer(BasicRenderer):
    def __init__(self, headers = None, body = None, output = None):
        '''
        Like BasicRender, only adds headers.
        
        headers - the headers part of the request (everything which 
                  is returned as an HTML header) (must have a keys method)
                  (default {})
                  
        body - the body part of the request (must be iterable)
                (default [])
        output - the function used to output the value 
                (default print(str(value)))
        '''
        
        # if headers is not none use headers, use a new dictionary
        self.headers = headers if headers else {"Content-Type":"text"}
        # this is a helper to make sure that 
        '''assert callable(getattr(self.headers, 'keys', None)), \
            'Headers must have a keys method'
           ''' 
        super(RequestRenderer, self).__init__(body,output)
        
    def setHeader(self,name,value):
        ''' allows for easy means of setting a header '''
        self.headers[name] = value
        
    def getHeader(self,name):
        ''' allows for an easy means of getting the header set '''
        return self.headers[name]
        
    def render(self,output = None):
        ''' passes each line of output to the output function '''
        # make it as easy as possible to pass in a new output
        output = output if output is not None else self.output
        if not (self.headers or self.body):
            # if neither, make sure that the script knows that it needs
            # to output *something* otherwise we'll get an error!
            output('')
            return
            
        for key,val in self.headers.items():
            output("{0}: {1}".format(key, val))
       
        output("") 
        try:
            self.body.render(output)
        except:    
            # remember, that first line after the headers needs to be empty
            # whether there have been headers output or not!
            for ln in self.body:
                output(ln)

import cgitb

class ErrorRenderer(BasicRenderer):
    ''' class which is designed for use with the cgitb.enable method (and eventually
        with the PyFram handler '''
    def __init__(self, headers = None, body = None, output = _str_print):
        super(ErrorRenderer,self).__init__(body,output)
        self.append(['<pre>'])
                  
    def write(self, line = None):
        # did we close the last pre tag? Then open a new one.
	
        if self.body[-1] == '</pre>':
            self.append(['<pre>'])
        self.append([line])
    
    def flush(self):
        self.append(['</pre>'])
        self.render()
        
    def render(self,output = None):
        tmp = []
        # this actually performs better in benchmarks 
        tmp.extend(self.body)
        
        output = output if output else self.output
        output('Content-Type: html')
        output('')
        output('<html><head/><body>')
        for ln in tmp:
            output(ln)
        output('</body></html>')