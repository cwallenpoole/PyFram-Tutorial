class HTML5:
    events = ('onabort', 'onblur', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'oncontextmenu', 'oncuechange', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter',\
              'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'oninput', 'oninvalid', 'onkeydown',\
              'onkeypress', 'onkeyup', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup',\
              'onmousewheel', 'onpause', 'onplay', 'onplaying', 'onprogress', 'onratechange', 'onreset', 'onscroll', 'onseeked', 'onseeking', 'onselect', 'onshow',\
              'onstalled', 'onsubmit', 'onsuspend', 'ontimeupdate', 'onvolumechange', 'onwaiting')

    globalAttributes = ('accesskey', 'class', 'contenteditable', 'contextmenu', 'dir', 'draggable', 'dropzone', 'hidden', 'id', 'lang', 'spellcheck', 'style', 'tabindex', 'title')
    
    class tags:
        html = ('manifest')
        
        base = ('href', 'target')
        link = ('href', 'rel', 'media', 'hreflang', 'type', 'sizes')
        meta = ('name', 'http-equiv', 'content', 'charset')
        style = ('media', 'type', 'scoped')
        script = ('src', 'async', 'defer', 'type', 'charset')
        body = ('onafterprint', 'onbeforeprint', 'onbeforeunload', 'onblur', 'onerror', 'onfocus', 'onhashchange', 'onload', 'onmessage', 'onoffline', 'ononline', 'onpagehide', \
                'onpageshow', 'onpopstate', 'onresize', 'onscroll', 'onstorage', 'onunload')
        blockquote = ('cite')
        ol = ('reversed', 'start', 'type')
        a = ('href', 'target', 'rel', 'media', 'hreflang', 'type')
        q = ('cite')
        time = ('datetime', 'pubdate')
        ins = ('cite', 'datetime')
        # because del is a keyword in Python, an underscore is needed. It needs to be accounted for when looking up this tag.
        _del = ('cite', 'datetime')
        img = ('alt', 'src', 'crossorigin', 'usemap', 'ismap', 'width', 'height')
        iframe = ('src', 'srcdoc', 'name', 'sandbox', 'seamless', 'width', 'height')
        embed = ('src', 'type', 'width', 'height')
        # sim to del
        _object = ('data', 'type', 'typemustmatch', 'name', 'usemap', 'form', 'width', 'height')
        param = ('name', 'value')
        video = ('src', 'crossorigin', 'poster', 'preload', 'autoplay', 'mediagroup', 'loop', 'muted', 'controls', 'width', 'height')
        audio = ('src', 'crossorigin', 'preload', 'autoplay', 'mediagroup', 'loop', 'muted', 'controls')
        source = ('src', 'type', 'media')
        track = ('kind', 'src', 'srclang', 'label', 'default')
        canvas = ('width', 'height')
        _map = ('name')
        area = ('alt', 'coords', 'shape', 'href', 'target', 'rel', 'media', 'hreflang', 'type')
        table = ('border')
        colgroup = ('span')
        col = ('span')
        td = ('colspan', 'rowspan', 'headers')
        th = ('colspan', 'rowspan', 'headers', 'scope')
        form = ('accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate', 'target')
        fieldset = ('disabled', 'form', 'name')
        label = ('form', 'for')
        input = ('accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget',\
                 'height', 'list', 'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly', 'required', 'size', 'src', 'step', 'type', 'value', 'width')
        button = ('autofocus', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'name', 'type', 'value')
        select = ('autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size')
        optgroup = ('disabled', 'label')
        option = ('disabled', 'label', 'selected', 'value')
        textarea = ('autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name', 'placeholder', 'readonly', 'required', 'rows', 'wrap')
        keygen = ('autofocus', 'challenge', 'disabled', 'form', 'keytype', 'name')
        output = ('for', 'form', 'name')
        progress = ('value', 'max')
        meter = ('value', 'min', 'max', 'low', 'high', 'optimum')
        details = ('open')
        command = ('type', 'label', 'icon', 'disabled', 'checked', 'radiogroup')
        menu = ('type', 'label')
        
def get_attributes(tagName, version = HTML5, unique = False):
    ret = version.globalAttributes + getattr(version.tags,tagName,getattr(version.tags,'_'+tagName,tuple()))
    if not unique:
        ret += version.events
    return ret
