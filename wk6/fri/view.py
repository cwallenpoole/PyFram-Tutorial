__all__ = ["BasicRenderer", "HTMLRenderer", "HTMLCleaner"]

################################################################################
#
#       Cleaner
#
################################################################################
import html.parser as hparse

DEFAULT_ALLOWED_TAGS = ['b','strong','em','i','u','a']

class HTMLCleaner(hparse.HTMLParser):

    def __init__(self, strict = True, failSilently = True, allowed = DEFAULT_ALLOWED_TAGS):
        self.allowedTags = allowed
        self.failSilently = failSilently
        
        super(HTMLCleaner, self).__init__(strict)
    
    def _assertValidTag(self,tag):
        if not tag in self.allowedTags:
            if self.failSilently:
                return False
            self.error('{0} is not in the list of allowed tags: {1}'.\
                       format(tag,self.allowedTags))
        return True
    
    def _formatAtts(self, attrs):
        result = ['{0}="{1}"'.format(*x) if len(x) == 2 else x for x in attrs]
        return ' '.join(result)
        
    def _handle_disallowed_type(self,data):
        if self.failSilently:
            return
        self.error('{0} is not allowed'.format(data))

    def reset(self):
        self._openTags  = []
        self.source = ""
        self.result = ""
        super(HTMLCleaner, self).reset()

    def feed(self,data):
        self.source = data
        super(HTMLCleaner,self).feed(data)
        
    def handle_data(self, data):
        # passthrough... no need to do anything here.
        self.result += data
        
    def handle_startendtag(self,tag,attrs):
        if self._assertValidTag(tag):
            self.result += '<{0} {1}/>'.format(tag, self._formatAttrs(attrs))
        
    def handle_starttag(self,tag,attrs):
        if not self._assertValidTag(tag):
            return
        self._openTags.append(tag)
        self.result += '<{0} {1}>'.format(tag, self._formatAttrs(attrs))
        
    def handle_endtag(self,tag):
        if not tag in self.allowedTags:
            return
        if self.strict and self._openTags[-1] != tag:
            self.error("The end tag {0} does not match the latest start tag {1}".\
                        format(tag, self._openTags[-1]))
        self.result += '</{0}>'.format(self._openTags.pop())
    
    def handle_charref(self, name):
        self.handle_entityref("#"+name)

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        self.handle_data("&"+name)

    # Overridable -- handle comment
    def handle_comment(self, data):
        _handle_disallowed_type(data)

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        _handle_disallowed_type(decl)

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        _handle_disallowed_type(data)

    def unknown_decl(self, data):
        _handle_disallowed_type(data)

################################################################################
#
#       Renderer
#
################################################################################
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

import cgitb

class ErrorRenderer(HTMLRenderer):
    ''' class which is designed for use with the cgitb.enable method (and eventually
        with the PyFram handler '''
    def __init__(self, headers = None, body = None, output = _str_print):
        super(ErrorRenderer,self).__init__(headers,body,output)
        self.append(['<pre>'])
                  
    def write(self, line = None):
        # did we close the last pre tag? Then open a new one.
        if self.body[-1] == '</pre>':
            self.append(['<pre>'])
        self.append([line])
    
    def flush(self):
        self.append(['</pre>'])
        self.render()
