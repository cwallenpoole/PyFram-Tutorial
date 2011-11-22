class _Unstrict:
    def is_valid_property(self,attr):
        return True
    
    def _initial_validation(self,valid):
        return
        
class Tag:
    def __init__(self, tag_name, contents = None, attrs = None, *, valid = None, **kwargs):
        attrs = attrs or {}
        contents = contents if not contents is None else []
        __dict__ = {
        'valid_keys': valid,
        'tag_name': tag_name,
        'contents': contents,
        'attrs': dict(list(zip(valid,[None]*len(valid))) + \
                      list(attrs.items()) + list(kwargs.items()))}
        
        for k,v in __dict__.items():
            self.__dict__[k]=v
        self._initial_validation(valid)
        
    def _initial_validation(self,valid):
        for attr in self.attrs:
            if not attr in valid:
                self.trigger_keyerror(attr)
        
    def is_valid_property(self,attr):
        return attr in self.attrs
        
    def __setattr__(self,key,value):
        print(key)
        if key in self.__dict__:
            self.__dict__[key] = value
        elif self.is_valid_property(key):
            self.attrs[key] = value

    def __getattr__(self,key):        
        if key in self.__dict__['attrs']:
            return self.__dict__['attrs'][key]
        return self.__dict__[key]
    
    def trigger_keyerror(self,key):
        raise KeyError('"{0}" is not a valid attribute for a {1} tag.'.format(key, self.tag_name))
        
    def get_open_tag(self, self_closing = False):
        close = ' />' if self_closing else ' >'
        
        return '<' + self.tag_name + ' ' + \
                ' '.join(['{0}="{1}"'.format(key,val or "") for key, val in self.attrs.items() if val is not None]) + \
                close;
                
    def get_close_tag(self):
        return '</{0}>'.format(self.tag_name)
        
    def __str__(self):
        if not self.contents:
            return self.get_open_tag(True)
        return self.get_open_tag() + ''.join([str(i) for i in self.contents]) + self.get_close_tag()
        
    __repr__ = __str__
    
class UnstrictTag(_Unstrict, Tag):
    pass
