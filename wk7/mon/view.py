import warnings

__all__ = ["BasicRenderer", "HTMLRenderer", "RequestRenderer", "HTMLDocumentRenderer", "ErrorRender", "HTMLCleaner"]


################################################################################
#
#       Cleaner
#
################################################################################
import html.parser as hparse

DEFAULT_ALLOWED_TAGS = ['b','strong','em','i','u','a']
import re
attrfind_tolerant = re.compile(
    r',?\s*([a-zA-Z_][-.:a-zA-Z_0-9]*)(\s*=\s*'
    r'(\'[^\']*\'|"[^"]*"|[^>\s]*))?')
class HTMLCleaner(hparse.HTMLParser):
    '''This class is specifically designed to prevent XSS insertion and inputs which 
    could otherwise break the DOM. It is meant to parallel the strip_tags function
    that is in PHP.
    '''
    
    # We don't want anything to get escaped like CDATA in this class. Everything 
    # should be fair game
    CDATA_CONTENT_ELEMENTS = (None,)
    
    def __init__(self, strict = False, escape = True, 
                 allowed = DEFAULT_ALLOWED_TAGS, feed = None):
        '''Constructor
        Keyword arguments:
        strict -- whether this is strict mode (see html.parser.HTMLParser) ***NOTE***
                  the default has been set to False as that seems like it would be 
                  better for the use-case.
        allowed -- The list of allowed tags.  
        escape -- should this escape invalid tags or cause an error? (only usable in
                  non-strict mode)
	feed -- if not None, this will be fed directly into self.feed.
        '''
        self.allowed_tags = allowed
        self.escape = escape
        
        super(HTMLCleaner, self).__init__(strict)    
        if feed is not None:
            self.feed(feed)

    def __str__(self):
        return self.cleaned_data
 
    def _assert_valid_tag(self,tag):
        '''
        Tests to see if the provided tag is in the allowed tag set. If in strict mode
        it will cause an error if it isn't. Otherwise it will return True if it is,
        False if it isn't.
        '''
        if not (tag in self.allowed_tags):
            if not self.strict:
                return False
            self.error('{0} is not in the list of allowed tags: {1}'.\
                       format(tag,self.allowed_tags))
        return True
    
    def _format_attrs(self, attrs):
        '''
        This converts the provided attributes to HTML valid attributes. It is used
        in the starttag and startendtag methods.
        
        Attributes come in the form [(key, value)...]. If there is no value, then it is
        a boolean, so it does not get an ="", but it simply is declared.
        '''
        result = ['{0}="{1}"'.format(*x) if len(x) == 2 else x for x in attrs]
        return ' '.join(result)
                
    def reset(self):
        self.open_tags  = []
        self.source = ""
        self.cleaned_data = ""
        super(HTMLCleaner, self).reset()

    def feed(self,data):
        data = data.strip()
        self.source = data
        super(HTMLCleaner,self).feed(data)
        if self.open_tags and self.strict:
            self.error("The following tag(s) remain unclosed: {0}".\
                        format(', '.join(self.open_tags)))
    
            
    def handle_invalid_startendtag(self,tag,attr):
        self.cleaned_data += '&lt;{0} {1}/&gt;'.format(tag, self._format_attrs(attrs))\
                        if attrs else '<{0}>'.format(tag)
             
    def handle_invalid_end(self,tag):
        self.cleaned_data += '&lt;/{0}&gt;'.format(tag)
        
    def handle_invalid_starttag(self,tag,attrs):
        self.cleaned_data += '&lt;{0} {1}&gt;'.format(tag, self._format_attrs(attrs))\
                        if attrs else '&lt;{0}&gt;'.format(tag)
                        
    def handle_data(self, data):
        # passthrough... no need to do anything here.
        self.cleaned_data += data
        
    def handle_startendtag(self,tag,attrs):
        if self._assert_valid_tag(tag):
            self.cleaned_data += '<{0} {1}/>'.format(tag, self._format_attrs(attrs))
        elif self.escape: 
            self.handle_invalid_startendtag(tag,attrs)
        
    def handle_starttag(self,tag,attrs):
        if not self._assert_valid_tag(tag):
            if self.escape: 
                self.handle_invalid_starttag(tag,attrs)
            return
        self.open_tags.append(tag)
        self.cleaned_data += '<{0} {1}>'.format(tag, self._format_attrs(attrs))\
                        if attrs else '<{0}>'.format(tag)
                        
    def handle_endtag(self,tag):
        if not self._assert_valid_tag(tag):
            if self.escape: 
                self.handle_invalid_end(tag)
            return
        if self.strict and (not self.open_tags or self.open_tags[-1] != tag):
            self.error("The end tag {0} does not match the latest start tag {1}".\
                        format(tag, self.open_tags[-1]))
        self.cleaned_data += '</{0}>'.format(self.open_tags.pop() if self.open_tags else tag)
    
    def handle_charref(self, name):
        self.handle_entityref("#"+name)

    def handle_entityref(self, name):
        self.handle_data("&"+name)

    def handle_comment(self, data):
        '''
        handle comment
        Overridden to hook into handle_disallowed_type 
        '''
        self.handle_disallowed_type(data)

    def handle_decl(self, decl):
        '''
        handle declaration
        Overridden to hook into handle_disallowed_type
        '''
        self.handle_disallowed_type(decl)

    def handle_pi(self, data):
        '''
        handle processing instruction
        Overridden to hook into handle_disallowed_type
        '''
        self.handle_disallowed_type(data)

    def unknown_decl(self, data):
        '''
        handle unknown declaration
        Overridden to hook into handle_disallowed_type
        '''
        self.handle_disallowed_type(data)
        
    def handle_disallowed_type(self,val):
        '''
        Comment, pi, decl, and unknown decl all route into this function.
        By design, it does nothing. It is meant to be overridden in a 
        descendant class if necessary.
        '''
        pass

    # This has to be included to handle http://bugs.python.org/issue13273
    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = hparse.tagfind.match(rawdata, i+1)
        assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        self.lasttag = tag = rawdata[i+1:k].lower()

        while k < endpos:
            if self.strict:
                m = hparse.attrfind.match(rawdata, k)
            else:
                # bug fix... sigh...
                m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                 attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
                attrvalue = self.unescape(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            k = m.end()
            
        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            if self.strict:
                self.error("junk characters in start tag: %r"
                           % (rawdata[k:endpos][:20],))
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith('/>'):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode()
        return endpos

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

class HTMLDocumentRenderer(BasicRenderer):
    def __init__(self, head = None, body = None, doctype = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">''', output = _str_print):
        self.doctype = doctype
        self.body = body if body is not None else []
        self.head = head if head is not None else []
    
    def append(self, line):
        # issue a warning, something which is annoying to look at, but
        # does not prevent action
        warnings.warn("HTMLDocumentRenderer should not have append " +
        "called on it directly")
        self.appendBody(line)
        
    def appendBody(self, line):
        self.body += line
        
    def appendHead(self, line):
        self.head += line
        
    def render(self,output = None):
        tmp = []
        # this actually performs better in benchmarks 
        tmp.append(self.doctype + '<html><head>')
        tmp.extend(self.head)
        tmp.append('</head><body>')
        tmp.extend(self.body)
        tmp.append('</body></html>')
        
        output = output if output else self.output
        for ln in tmp:
            output(ln)

class HTMLRenderer(RequestRenderer):
    ''' class designed for specialization in HTML requestions '''
    def __init__(self, headers = None, head = None, body = None, output = _str_print):
        body = body if body else HTMLDocumentRenderer(head,body)
        super(HTMLRenderer, self).__init__(headers,body,output)
        self.document = self.body
        
    def append(self, line):
        self.document.appendBody(line)

    def render(self, output=None):
        output = output if output else self.output
        if not (self.headers or self.body):
            # if neither, make sure that the script knows that it needs
            # to output *something* otherwise we'll get an error!
            output('')
            return

        for key,val in self.headers.items():
            output("{0}: {1}".format(key, val))

        output('');
        self.document.render(output)
        
import cgitb

class ErrorRenderer(HTMLRenderer):
    ''' class which is designed for use with the cgitb.enable method (and eventually
        with the PyFram handler '''
    def __init__(self, headers = None, body = None, output = _str_print):
        super(ErrorRenderer,self).__init__(headers,None,body,output)
        self.append(['<pre>'])
                  
    def write(self, line = None):
        # did we close the last pre tag? Then open a new one.
	
        if self.body[-1] == '</pre>':
            self.append(['<pre>'])
        self.append([line])
    
    def flush(self):
        self.append(['</pre>'])
        self.render()
