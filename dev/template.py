def runTemplate(*srcs, **fmt):
    src = ''.join(srcs)
    kwargs = {}
    callables = {}
    for key in fmt:
        val = fmt[key]
        if callable(val):
            if src.find('{{{key}}}'.format(key=key)) > -1:
                kwargs[key] = val()
                continue
            store = callables  
        else:
            store = kwargs
        store[key] = val
        
    for key in callables:
        
        # escape all of the callable args before passing through to traditional format
        src = src.replace('{{{key}{{'.format(key=key),'{{{{{key}{{{{'.format(key=key))
        src = src.replace('}}{key}}}'.format(key=key),'}}}}{key}}}}}'.format(key=key))
        
    print(src)
    src = src.format(**kwargs)
    return src    
