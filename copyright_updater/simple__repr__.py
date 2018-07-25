def simple__repr__(obj):
    """ A mixin implementing a simple __repr__

    :source: Inspired from https://stackoverflow.com/a/44595303
    """

    attrs = list()
    indent = 0

    for k, v in obj.__dict__.items():
        attr = "{}={!r}".format(k, v)
        if ('<' in str(v)):
            indent = 3
        else:
            indent = 0
        attrs.append(_reindent(attr, indent))

    return "<{klass} @{id:x}\n{attrs}>".format(
        klass=obj.__class__.__name__,
        id=id(obj) & 0xFFFFFF,
        #attrs="\n".join("{}={!r}".format(k, v) for k, v in obj.__dict__.items())
        attrs="\n".join(attrs)
    )

def _reindent(s, num_spaces):
    leading_space = num_spaces * ' '
    lines = [ leading_space + line.strip( )
              for line in s.splitlines( ) ]
    return '\n'.join(lines).replace(leading_space, '', 1)