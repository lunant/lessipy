import less.tree.cssable


class Expression(less.tree.cssable.CSSable):
    """A css value expression. It just chaning elements."""

    def __init__(self, *elements):
        for el in elements:
            if not isinstance(el, less.tree.cssable.CSSable):
               raise ValueError("only `CSSable` instance is allowed,"
                                "passed " + repr(el))
        self.elements = elements

    def to_css(self):
        
