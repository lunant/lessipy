import less.tree.cssable


class Declaration(less.tree.cssable.CSSable):
    """A declaration has a key-value pair(e.g k : v). `Property`:class could
    be a key and `Expression`:class could be a value.

    For example, like this::

        >>> Declaration([(Property("text-align"), Keyword("center"))]).to_css()
        'text-align: center;'
    
    """

    def __init__(self, *args):
        if args[0] isinstance Property:
            return PropertyDeclaration(args[0], 
